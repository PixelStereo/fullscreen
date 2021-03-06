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

from svp import get_players
from svp.widgets.RangeSlider import QHSpinBoxRangeSlider

class LayerUI(QWidget):
    """
    """
    def __init__(self, display):
        super(LayerUI, self).__init__()
        # initalise selection
        self.selected = None
        # the display model connected to
        self._display = display
        # active parameter
        self.active = QCheckBox('active')
        self.active.stateChanged.connect(self.active_changed)
        self.active.setChecked(self._display.active)
        self._display.active_changed.connect(self.active.setChecked)
        # which source to display
        self.sources = QComboBox()
        self.sources.setMinimumWidth = 150
        self.sources.addItem('No Source')
        self.sources.currentIndexChanged.connect(self.source_changed)
        for source in get_players():
            self.sources.addItem(source.name)
        source = get_players().index(self._display.source)
        self.sources.setCurrentIndex(source + 1)
        #self._display.source_changed.connect(self.sources.setCurrentIndex)
        # freeze
        self.freeze = QCheckBox('freeze')
        self.freeze.stateChanged.connect(self.freeze_changed)
        self.freeze.setChecked(self._display.freeze)
        self._display.freeze_changed.connect(self.freeze.setChecked)
        # width
        self.width = QSpinBox()
        self.width.valueChanged.connect(self.width_changed)
        self.width.setMaximum(4096)
        self.width.setValue(self._display.size().width())
        self._display.size_changed.connect(self.set_size)
        # height
        self.height = QSpinBox()
        self.height.setMaximum(4096)
        self.height.setValue(self._display.size().height())
        self.height.valueChanged.connect(self.height_changed)
        # set layout
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.active)
        self.layout.addWidget(self.sources)
        self.layout.addWidget(self.freeze)
        self.layout.addWidget(self.width)
        self.layout.addWidget(self.height)
        self.show()

    def set_size(self, qsize):
        self.width.setValue(qsize.width())
        self.height.setValue(qsize.height())

    def active_changed(self, state):
        self._display.active = state

    def width_changed(self, width):
        self._display.resize(width, self._display.size().height())

    def height_changed(self, height):
        self._display.resize(self._display.size().width(), height)

    def freeze_changed(self, state):
        self._display.freeze = state

    def source_changed(self, index):
        print('source changed : ', self._display.name, index)
        if index in [0, -1]:
            source = None
        else:
            index -= 1
            source = get_players()[index]
        print('source changed LAST : ', source)
        self._display.source = source
