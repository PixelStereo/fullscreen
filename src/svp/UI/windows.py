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

from svp import get_windows, get_players
from svp.UI.window import WindowUI

def get_screens():
    for screen in QApplication.instance() .screens():
        print(screen.name(), screen.size())


class WindowsList(QListWidget):
    """docstring for MediaBin"""
    def __init__(self):
        super(WindowsList, self).__init__()
        self.selected = None
        print(get_windows())
        for window in get_windows():
            item = QListWidgetItem()
            win = WindowUI(window)
            item.setSizeHint(QSize(250, 60))
            self.addItem(item)
            self.setItemWidget(item, win)
            self.setAlternatingRowColors(True)
            self.setMinimumWidth(600)

    def selection_changed(self):
        if self.selectedItems():
            selected = self.selectedItems()[0]
            print(selected.text())
