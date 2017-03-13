#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Display Class
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy

from PyQt5.QtGui import QPixmap
from PyQt5.Qt import *

class Display(QLabel):
    """docstring for Display"""
    def __init__(self, name=None, active=True, source=None):
        super(Display, self).__init__()
        self.name = name
        self._source = None
        self.source = source
        self.setFixedSize(640, 360)
        #self.video_frame = QLabel()
        #self.layout = QVBoxLayout()
        #self.layout.addWidget(self.video_frame)
        #self.setLayout(self.layout)
        #self.video_frame.setAlignment(Qt.AlignCenter)
        #self.video_frame.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self._fullscreen = False
        self._active = self.isEnabled()
        if self.active:
            self.show()

    @property
    def source(self):
        return self._source
    @source.setter
    def source(self, source):
        if self._source:
            self._source.new_frame.disconnect(self.setPixmap(pix))
        self._source = source
        if source:
            self._source.new_frame.connect(self.new_frame)

    def new_frame(self, pix):
        self.setPixmap(pix)

    @property
    def fullscreen(self):
        return self._fullscreen
    @fullscreen.setter
    def fullscreen(self, state):
        self._fullscreen = state

    def clear(self):
        self.setPixmap(QPixmap())

    def mute(self, state):
        if state:
            self.available = False
            self.setPixmap(QPixmap())
        else:
            self.available = True

    @property
    def active(self):
        return self.isEnabled()
    @active.setter
    def active(self, state):
        self.setEnabled(state)
