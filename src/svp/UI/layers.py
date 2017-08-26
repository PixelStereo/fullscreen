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

from svp import get_windows, get_players, get_layers
from svp.UI.layer import LayerUI

def get_screens():
    for screen in QApplication.instance() .screens():
        print(screen.name(), screen.size())


class LayersList(QListWidget):
    """
    A layer list is a list of all layers of the project
    """
    def __init__(self):
        super(LayersList, self).__init__()
        self.selected = None
        for layer in get_layers():
            item = QListWidgetItem()
            lay = LayerUI(layer)
            item.setSizeHint(QSize(250, 60))
            self.addItem(item)
            self.setItemWidget(item, lay)
            self.setAlternatingRowColors(True)
            self.setMinimumWidth(600)

    def selection_changed(self):
        if self.selectedItems():
            selected = self.selectedItems()[0]
            print(selected.text())
