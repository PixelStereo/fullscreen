#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Player Class
"""

from PyQt5.QtWidgets import QListWidget, QWidget, QLabel, QPushButton, QGridLayout, QHBoxLayout, QListWidgetItem
from PyQt5.QtCore import QTimer, Qt, QSize
from PyQt5.QtGui import QImage, QPixmap
import os
from PyQt5.Qt import *

from svp.api import get_displays, get_players
from svp.display_ui import DisplayUI

def get_screens():
    for screen in QApplication.instance() .screens():
        print(screen.name(), screen.size())


class DisplaysList(QListWidget):
    """docstring for MediaBin"""
    def __init__(self, player):
        super(DisplaysList, self).__init__()
        self.selected = None
        for display in get_displays():
            item = QListWidgetItem()
            # display.name + ' - ' + str(display.size().width()) + ' x ' + str(display.size().height())
            disp = DisplayUI(display)
            item.setSizeHint(QSize(250, 60))
            self.addItem(item)
            self.setItemWidget(item, disp)
            self.setAlternatingRowColors(True)

    def selection_changed(self):
        if self.selectedItems():
            selected = self.selectedItems()[0]
            print(selected.text())

    def selection_changed(self):
        if self.selectedItems():
            selected = self.selectedItems()[0]
            print(selected.text())

class DisplayControl(QListWidget):
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
        self.displays.currentIndexChanged.connect(self.selection)
        self.selection(0)
        self.displays.setCurrentIndex(0)
        layout = QHBoxLayout()
        layout.addWidget(self.displays)
        layout.addWidget(self.sources)
        layout.addWidget(self.visible)
        self.setLayout(layout)
        self.visible.stateChanged.connect(self.active)
        self.sources.currentTextChanged.connect(self.source)
        get_screens()

    

    def source(self, source):
        if source == 'No Source':
            self.display.clear()
        else:
            for player in get_players():
                if str(player) == source:
                    self.display.source = player

    def active(self, state):
        self.selected.active = state

    def selection(self, index):
        self.selected = get_displays()[index]
        if self.selected:
            self.visible.setEnabled(True)
        else:
            self.visible.setEnabled(False)

    @property
    def display(self):
        return self._display
    @display.setter
    def display(self, display):
        self.displays.setCurrentItem(str(display))
        self._display = display
