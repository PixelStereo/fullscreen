#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Display Class
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy

from PyQt5.QtGui import QPixmap
from PyQt5.Qt import *

class Display(QWidget):
    """docstring for Display"""
    def __init__(self, name, active):
        super(Display, self).__init__()
        self.active = active
        self.name = name
        self.setFixedSize(640, 360)
        self.video_frame = QLabel()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.video_frame)
        self.setLayout(self.layout)
        self._available = True
        self.video_frame.setAlignment(Qt.AlignCenter)
        self.video_frame.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self._fullscreen = False
        if self.active:
            self.show()

    @property
    def fullscreen(self):
        return self._fullscreen
    @fullscreen.setter
    def fullscreen(self, state):
        self._fullscreen = state

    def clear(self):
        self.video_frame.setPixmap(QPixmap())

    def mute(self, state):
        if state:
            self.available = False
            self.video_frame.setPixmap(QPixmap())
            #self.video_frame.hide()
        else:
            #self.video_frame.show()
            self.available = True

    @property
    def available(self):
        return self._available
    @available.setter
    def available(self, state):
        self._available = state
