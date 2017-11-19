#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Display UI Class
"""

from PyQt5.QtWidgets import QListWidget, QWidget, QLabel, QPushButton, QGridLayout, QGroupBox, QHBoxLayout, QListWidgetItem, QSpinBox, QCheckBox, QComboBox
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap, QStandardItemModel
import os
from PyQt5.Qt import *

from svp import get_layers

class WindowUI(QWidget):
    """
    """
    def __init__(self, window):
        super(WindowUI, self).__init__()
        # initalise selection
        self.selected = None
        # the window model connected to
        self._window = window
        # active parameter
        self.active = QCheckBox('active')
        self.active.stateChanged.connect(self.active_changed)
        #self.active.setChecked(self._window.active)
        self._window.active_changed.connect(self.active.setChecked)
        # which source to window
        self.layers = QListWidget()
        for layer in get_layers():
            self.layers.addItem(layer.name)
        # freeze
        self.freeze = QCheckBox('freeze')
        self.freeze.stateChanged.connect(self.freeze_changed)
        self.freeze.setChecked(self._window.freeze)
        self._window.freeze_changed.connect(self.freeze.setChecked)
        # fullscreen mode
        self.fullscreen = QCheckBox('Fullscreen')
        self.fullscreen.stateChanged.connect(self.fullscreen_changed)
        #self.fullscreen.setChecked(self._window.fullscreen)
        self._window.fullscreen_changed.connect(self.fullscreen.setChecked)
        # width
        self.width = QSpinBox()
        self.width.valueChanged.connect(self.width_changed)
        self.width.setMaximum(4096)
        #self.width.setValue(self._window.size().width())
        self._window.size_changed.connect(self.set_size)
        # height
        self.height = QSpinBox()
        self.height.setMaximum(4096)
        #self.height.setValue(self._window.size().height())
        self.height.valueChanged.connect(self.height_changed)
        # set layout
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.active)
        #self.layout.addWidget(self.sources)
        self.layout.addWidget(self.freeze)
        self.layout.addWidget(self.width)
        self.layout.addWidget(self.height)
        self.layout.addWidget(self.fullscreen)


    def set_size(self, qsize):
        self.width.setValue(qsize.width())
        self.height.setValue(qsize.height())

    def active_changed(self, state):
        self._window.active = state

    def width_changed(self, width):
        self._window.resize(width, self._window.size().height())

    def height_changed(self, height):
        self._window.resize(self._window.size().width(), height)

    def freeze_changed(self, state):
        self._window.freeze = state

    def fullscreen_changed(self, state):
        self._window.fullscreen = state

    def source_changed(self, index):
        print('source changed : ', self._window.name, index)
        if index in [0, -1]:
            source = None
        else:
            index -= 1
            source = get_players()[index]
        print('source changed LAST : ', source)
        self._window.source = source
