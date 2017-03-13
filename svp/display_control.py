#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Player Class
"""

from PyQt5.QtWidgets import QListWidget, QWidget, QLabel, QPushButton, QGridLayout, QVBoxLayout
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
import os
from PyQt5.Qt import *

from api import get_displays, get_players

class DisplayControl(QWidget):
    """
    """
    def __init__(self, display):
        super(DisplayControl, self).__init__()
        self.sources = QComboBox()
        self.visible = QCheckBox('active')
        self.sources.addItem('No Source')
        for source in get_players():
            self.sources.addItem(str(source))
        layout = QVBoxLayout()
        layout.addWidget(self.sources)
        layout.addWidget(self.visible)
        self.setLayout(layout)
        self.display = display
        self.visible.stateChanged.connect(self.active)
        self.sources.currentTextChanged.connect(self.source)

    def source(self, source):
        if source == 'No Source':
            self.display.clear()
        else:
            self.display.source = source

    def active(self, state):
        self.display.active = state
