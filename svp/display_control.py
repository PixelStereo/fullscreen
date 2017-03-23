#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Player Class
"""

from PyQt5.QtWidgets import QListWidget, QWidget, QLabel, QPushButton, QGridLayout, QHBoxLayout
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
import os
from PyQt5.Qt import *

from svp.api import get_displays, get_players

class DisplayControl(QWidget):
    """
    """
    def __init__(self, display):
        super(DisplayControl, self).__init__()
        # initialise selection : 
        self.selected = None
        self.visible = QCheckBox('active')
        self._display = display
        self.sources = QComboBox()
        self.sources.setMinimumWidth = 150
        self.sources.addItem('No Source')
        for source in get_players():
            self.sources.addItem(source.name)
        self.displays = QComboBox()
        self.displays.setMinimumWidth = 150
        for display in get_displays():
            self.displays.addItem(display.name)
        self.displays.currentTextChanged.connect(self.selection)
        self.displays.setCurrentIndex(0)
        layout = QHBoxLayout()
        layout.addWidget(self.displays)
        layout.addWidget(self.sources)
        layout.addWidget(self.visible)
        self.setLayout(layout)
        self.visible.stateChanged.connect(self.active)
        self.sources.currentTextChanged.connect(self.source)

    def source(self, source):
        if source == 'No Source':
            self.display.clear()
        else:
            for player in get_players():
                if str(player) == source:
                    self.display.source = player

    def active(self, state):
        self.selected.active = state

    def selection(self, display_name):
        for display in get_displays():
            if display.name == display_name:
                self.selected = display

    @property
    def display(self):
        return self._display
    @display.setter
    def display(self, display):
        self.displays.setCurrentItem(str(display))
        self._display = display
