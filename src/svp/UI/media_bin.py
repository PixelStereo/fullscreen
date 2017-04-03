#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Player Class
"""

from PyQt5.QtWidgets import QListWidget
import os
from PyQt5.Qt import *

class MediaBin(QListWidget):
    selection = pyqtSignal(str)
    def __init__(self, filepath):
        super(MediaBin, self).__init__()
        self._filepath = filepath
        self._players = []
        self.refresh()
        self.show()

    def refresh(self):
        print(os.path.abspath(self.filepath))
        result = [os.path.join(dp, f) for dp, dn, filenames in os.walk(os.path.abspath(self.filepath)) for f in filenames if os.path.splitext(f)[1] == '.mov']
        for res in result:
            self.addItem(res)
        self.itemSelectionChanged.connect(self.selection_changed)
        self.setCurrentRow(0)

    def selection_changed(self):
        if self.selectedItems():
            path = self.selectedItems()[0]
            self.selection.emit(path.text())

    @property
    def filepath(self):
        return self._filepath
    @filepath.setter
    def filepath(self, filepath):
        self._filepath = filepath
