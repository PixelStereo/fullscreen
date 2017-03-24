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
    """docstring for Display"""
    def __init__(self, name=None, active=True, source=None):
        super(Display, self).__init__()
        self.name = name
        self._freeze = False
        self._source = None
        self.source = source
        self._width = 320
        self._height = 180
        self.setMinimumSize(320, 180)
        #self.setFixedSize(1280, 720)
        #self.video_frame = QLabel()
        #self.layout = QVBoxLayout()
        #self.layout.addWidget(self.video_frame)
        #self.setLayout(self.layout)
        #self.video_frame.setAlignment(Qt.AlignCenter)
        #self.video_frame.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self._fullscreen = False
        self.setAlignment(Qt.AlignCenter)
        self.active = active

    @property
    def source(self):
        return self._source
    @source.setter
    def source(self, source):
        if self._source:
            self._source.new_frame.disconnect(self.new_frame)
            self._source.clear.disconnect(self.clear)
        self._source = source
        self.source_changed.emit(source)
        if source:
            self._source.new_frame.connect(self.new_frame)
            self._source.clear.connect(self.clear)
        else:
            self.clear()

    def new_frame(self, pix):
        if not self.freeze:
            pix = pix.scaled(self.size(), Qt.KeepAspectRatio)
            self.setPixmap(pix)

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

    def clear(self):
        self.setPixmap(QPixmap())

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