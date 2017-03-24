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

from svp.api import new_display, get_players
from svp.RangeSlider import QHSpinBoxRangeSlider

class DisplayUI(QWidget):
    """
    """
    def __init__(self, display):
        super(DisplayUI, self).__init__()
        # initalise selection
        self.selected = None
        # the display model connected to
        self._display = display
        # active parameter
        self.active = QCheckBox('active')
        self.active.stateChanged.connect(self.activation)
        self.active.setChecked(self._display.active)
        self._display.active_changed.connect(self.active.setChecked)
        # which source to display
        self.sources = QComboBox()
        self.sources.setMinimumWidth = 150
        self.sources.addItem('No Source')
        self.sources.currentIndexChanged.connect(self.source_changed)
        self.sources.setCurrentIndex(get_players().index(self._display.source))
        self._display.source_changed.connect(self.sources.setCurrentIndex)
        for source in get_players():
            self.sources.addItem(source.name)
        # freeze
        self.freeze = QCheckBox('freeze')
        self.freeze.stateChanged.connect(self.freeze_changed)
        self.freeze.setChecked(self._display.freeze)
        self._display.freeze_changed.connect(self.freeze.setChecked)
        # fullscreen mode
        self.fullscreen = QCheckBox('Fullscreen')
        self.fullscreen.stateChanged.connect(self.fullscreen_changed)
        self.fullscreen.setChecked(self._display.fullscreen)
        self._display.fullscreen_changed.connect(self.fullscreen.setChecked)
        # width
        self.width = QSpinBox()
        # height
        self.height = QSpinBox()
        # set layout
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.active)
        self.layout.addWidget(self.sources)
        self.layout.addWidget(self.freeze)
        self.layout.addWidget(self.width)
        self.layout.addWidget(self.height)
        self.layout.addWidget(self.fullscreen)
        self.show()

    def activation(self, state):
        self._display.active = state

    def size_changed(self, qsize):
        self._display.width = qsize.width()
        self._display.height = qsize.height()

    def freeze_changed(self, state):
        self._display.freeze = state

    def fullscreen_changed(self, state):
        self._display.fullscreen = state

    def source_changed(self, index):
        if index == 0:
            source = None
        else:
            index -= 1
            source = get_players()[index]
        self._display.source = source