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
            disp = DisplayUI(display)
            item.setSizeHint(QSize(250, 60))
            self.addItem(item)
            self.setItemWidget(item, disp)
            self.setAlternatingRowColors(True)

    def selection_changed(self):
        if self.selectedItems():
            selected = self.selectedItems()[0]
            print(selected.text())
