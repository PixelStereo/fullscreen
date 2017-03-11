#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Player Class
"""

from PyQt5.QtWidgets import QListWidget
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
import os

class MediaBin(QListWidget):
    """docstring for MediaBin"""
    def __init__(self, filepath):
        super(MediaBin, self).__init__()
        self._filepath = filepath
        self._players = []
        self.refresh()

    def refresh(self):
        result = [os.path.join(dp, f) for dp, dn, filenames in os.walk(os.path.abspath(self.filepath)) for f in filenames if os.path.splitext(f)[1] == '.mov']
        for res in result:
            self.addItem(res)
        self.itemSelectionChanged.connect(self.selection_changed)
        self.setCurrentRow(0)

    def selection_changed(self):
        if self.selectedItems():
            path = self.selectedItems()[0]
            for player in self._players:
                player.player.load(path.text())
                player.filepath_label.setText(path.text())

    @property
    def filepath(self):
        return self._filepath
    @filepath.setter
    def filepath(self, filepath):
        self._filepath = filepath