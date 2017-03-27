#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Display Class
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy

from PyQt5.QtGui import QPixmap
from PyQt5.Qt import *
from PyQt5.QtCore import QSize


class Display(QLabel):
    size_changed = pyqtSignal(QSize)
    active_changed = pyqtSignal(bool)
    fullscreen_changed = pyqtSignal(bool)
    freeze_changed = pyqtSignal(bool)
    source_changed = pyqtSignal(int)
    # create a list for all displays
    __displays__ = []
    """
    QLabel pimped to display video
    """
    def __init__(self, name=None, active=True, source=None):
        super(Display, self).__init__()
        self.name = name
        self._freeze = False
        self._source = None
        self.source = source
        self._size = [320, 180]
        self.setMinimumSize(320, 180)
        self.setAlignment(Qt.AlignCenter)
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self._fullscreen = False
        self.setAlignment(Qt.AlignCenter)
        self.active = active
        self.__displays__.append(self)
        pos = len(self.__displays__)
        self.move(0, pos*300)

    def clear(self):
        self.setPixmap(QPixmap())

    def new_frame(self, pix):
        if not self.freeze:
            # scale the QPixmap to the display size (pixels)
            # todo : give  modes for fillin / keep ratio etc…
            pix = pix.scaled(self.size(), Qt.KeepAspectRatio)
            #self.setPixmap(pix)
            painter = QPainter(pix)
            rect = painter.viewport()
            painter.setOpacity(0.5)
            #painter.setPen(Qt.NoPen)
            #Qt.TransparentMode
            #painter.setBrush(QColor(0, 222, 0, 222))
            #size = pix.size()
            #size.scale(rect.size(), Qt.KeepAspectRatio)
            painter.setViewport(0, 222, 322, 123)
            #painter.setWindow(self.rect())
            #painter.drawPixmap(0, 0, 222, 333, self.pixmap())
            painter.drawPixmap(0, 0, 222, 333, pix)
            painter.end()


    @property
    def source(self):
        return self._source
    @source.setter
    def source(self, source):
        if self._source:
            try:
                self._source.new_frame.disconnect(self.new_frame)
                self._source.clear.disconnect(self.clear)
            except:
                pass
            if source:
                self._source.new_frame.connect(self.new_frame)
                self._source.clear.connect(self.clear)
            else:
                self.clear()
        self._source = source
        self.source_changed.emit(source)

    @property
    def fullscreen(self):
        return self._fullscreen
    @fullscreen.setter
    def fullscreen(self, state):
        if self.active:
            if state:
                self.showFullScreen()
            else:
                self.showNormal()
            self._fullscreen = state
            self.fullscreen_changed.emit(state)
            return True
        return False

    @property
    def freeze(self):
        return self._freeze
    @freeze.setter
    def freeze(self, state):
        self._freeze = state
        self.freeze_changed.emit(state)

    @property
    def active(self):
        return self.isVisible()
    @active.setter
    def active(self, state):
        if state:
            self.show()
        else:
            self.hide()
        self.active_changed.emit(state)
