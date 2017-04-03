#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Display Class
"""

from PyQt5.QtWidgets import (QApplication, QGraphicsAnchorLayout,
        QGraphicsProxyWidget, QGraphicsScene, QGraphicsView, QGraphicsWidget,
        QPushButton, QSizePolicy, QWidget, QVBoxLayout, QLabel, QSizePolicy, 
        QGraphicsOpacityEffect)

from PyQt5.QtGui import QPixmap, QColor, QSurface
from PyQt5.Qt import *
from PyQt5.QtCore import QSize, QEasingCurve, QSizeF, Qt

from svp.GL.widget import GLWidget


class Window(QWidget):
    """
    QLabel pimped to display video
    """
    # signals emited by this class instances
    size_changed = pyqtSignal(QSize)
    active_changed = pyqtSignal(bool)
    fullscreen_changed = pyqtSignal(bool)
    freeze_changed = pyqtSignal(bool)
    source_changed = pyqtSignal(int)
    # create a list for all displays
    __windows__ = []
    # initialisation of each instances
    def __init__(self, name=None, active=True, layers=None):
        super(Window, self).__init__()

        self.name = name
        if active:
            self.active = active
        else:
            self.active = True
        if not layers:
            self._layers = []
        else:
            self._layers = layers
        self._freeze = False
        self._size = [640, 480]
        """
        #self.setMinimumSize(320, 180)
        #self.resize(self._size[0], self._size[1])
        #self.setAlignment(Qt.AlignCenter)
        #self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        #self._fullscreen = False
        #self.setAlignment(Qt.AlignCenter)
        self.__windows__.append(self)
        pos = len(self.__windows__)
        pos = pos - 1
        #self.move(0, abs(pos*self.geometry().height()))
        # Display Properties
        self._display_name = True
        """


        self.__windows__.append(self)
        self.glWidgets = []

        mainLayout = QGridLayout()

        clearColor = QColor()

        self.glwidget = GLWidget()
        self.glwidget.setClearColor(clearColor)
        mainLayout.addWidget(self.glwidget)
        self.setLayout(mainLayout)

        timer = QTimer(self)
        timer.start(20)
        self.setWindowTitle(name)

    def makeObject(self, image):
        self.glwidget.makeObject(image)

    def clear(self):
        self.setPixmap(QPixmap())

    @property
    def display_name(self):
        """
        display the name of the display on it
        """
        return self.__display_name
    @display_name.setter
    def display_name(self, state):
        self._display_name = state

    @property
    def layers(self):
        return self._layers
    @layers.setter
    def layers(self, layers):
        if layers:
            for layer in layers:
                createItem(layer)
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
