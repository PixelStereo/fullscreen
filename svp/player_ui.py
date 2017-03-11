#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Player Class
"""

from PyQt5.QtWidgets import QListWidget, QWidget, QLabel, QPushButton, QGridLayout
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
import os
from PyQt5.Qt import *

from __init__ import new_display

class PlayerUI(QWidget):
    """
    """
    def __init__(self, player, media_bin=None):
        super(PlayerUI, self).__init__()
        self.media_bin = MediaBin(self, '/Users/reno/Dropbox')
        self.player = player
        self.preview = new_display('Preview', False)
        self.player.addDisplay(self.preview)
        self.filepath_label = QLabel(self.player.filepath)
        self.mute_button = QPushButton('Black')
        self.mute_button.setCheckable(True)
        self.mute_button.toggled.connect(self.preview.mute)
        self.pause_button = QPushButton('Pause')
        self.pause_button.clicked.connect(self.player.pause)
        # self.player.setFPS(1)
        self.player.setParent(self)
        self.player.setWindowFlags(Qt.Tool)
        self.play_button = QPushButton('Play')
        self.play_button.clicked.connect(self.player.play)
        self.eject_button = QPushButton('Eject')
        self.eject_button.clicked.connect(self.player.eject)
        self.control_layout = QGridLayout()
        self.control_layout.addWidget(self.media_bin, 0, 0, 4, 2)
        self.control_layout.addWidget(self.filepath_label, 5, 0, 1, 4)
        self.control_layout.addWidget(self.play_button, 6, 0, 1, 1)
        self.control_layout.addWidget(self.pause_button, 6, 1, 1, 1)
        self.control_layout.addWidget(self.eject_button, 6, 2, 1, 1)
        self.control_layout.addWidget(self.preview, 7, 0, 6, 1)
        #self.setMaximumSize(300, 200)
        self.setLayout(self.control_layout)
        self.media_bin.refresh()

    @property
    def filepath(self):
        return self.player.filepath
    @filepath.setter
    def filepath(self, filepath):
        self.player.filepath = filepath

    def load(self, filepath):
        self.filepath_label.setText(filepath)
        self.player.load(filepath)


class MediaBin(QListWidget):
    """docstring for MediaBin"""
    def __init__(self, parent, filepath):
        super(MediaBin, self).__init__()
        self.parent = parent
        self._filepath = filepath
        self._players = []

    def refresh(self):
        result = [os.path.join(dp, f) for dp, dn, filenames in os.walk(os.path.abspath(self.filepath)) for f in filenames if os.path.splitext(f)[1] == '.mov']
        for res in result:
            self.addItem(res)
        self.itemSelectionChanged.connect(self.selection_changed)
        self.setCurrentRow(0)
        self.parent.filepath = self.currentItem().text()

    def selection_changed(self):
        if self.selectedItems():
            path = self.selectedItems()[0]
            self.parent.load(path.text())

    @property
    def filepath(self):
        return self._filepath
    @filepath.setter
    def filepath(self, filepath):
        self._filepath = filepath