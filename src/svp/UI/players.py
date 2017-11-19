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

from svp import get_players

from svp.UI.player import PlayerUI

class PlayersList(QListWidget):
    """docstring for MediaBin"""
    def __init__(self):
        super(PlayersList, self).__init__()
        self.selected = None
        for player in get_players():
            item = QListWidgetItem()
            play = PlayerUI(player)
            item.setSizeHint(QSize(100, 210))
            self.addItem(item)
            self.setItemWidget(item, play)
            self.setAlternatingRowColors(True)
            self.setMinimumWidth(400)
            self.setMinimumHeight(500)

    def selection_changed(self):
        if self.selectedItems():
            selected = self.selectedItems()[0]
            print(selected.text())
