#! /usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import os,sys
lib_path = os.path.abspath('..')
sys.path.append(lib_path)
print(lib_path)
import svp
from svp import new_player, new_display
from svp.media_bin import MediaBin



class PlayerUI(QWidget):
    """
    """
    def __init__(self, player, media_bin=None):
        super(PlayerUI, self).__init__()
        self.media_bin = media_bin
        self.player = player
        self.preview = new_display('Preview', False)
        self.player.addDisplay(self.preview)

        if media_bin:    
            self.filepath = self.media_bin.currentItem().text()
        self.filepath_label = QLabel('filepath')
        self.mute_button = QPushButton('Black')
        self.mute_button.setCheckable(True)
        self.mute_button.toggled.connect(self.preview.mute)
        self.resume_button = QPushButton('Resume')
        self.resume_button.clicked.connect(self.player.resume)
        self.pause_button = QPushButton('Pause')
        self.pause_button.clicked.connect(self.player.pause)
        # self.player.setFPS(1)
        self.player.setParent(self)
        self.player.setWindowFlags(Qt.Tool)
        self.start_button = QPushButton('Start')
        self.start_button.clicked.connect(self.player.start)
        self.eject_button = QPushButton('Eject')
        self.eject_button.clicked.connect(self.player.eject)
        self.control_layout = QGridLayout()
        self.control_layout.addWidget(self.filepath_label, 0, 0, 1, 4)
        self.control_layout.addWidget(self.start_button, 1, 0, 1, 1)
        self.control_layout.addWidget(self.resume_button, 1, 1, 1, 1)
        self.control_layout.addWidget(self.pause_button, 1, 2, 1, 1)
        self.control_layout.addWidget(self.eject_button, 1, 3, 1, 1)
        self.control_layout.addWidget(self.preview, 2, 0, 4, 4)
        #self.setMaximumSize(300, 200)
        self.setLayout(self.control_layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.player = new_player()
        self.desktop = new_display('Desktop Display', False)
        self.desktop.available = False
        self.player.addDisplay(self.desktop)
        media_bin = MediaBin('/Users/reno/Dropbox')
        control_panel = PlayerUI(self.player, media_bin)
        media_bin._players.append(control_panel)
        layout = QGridLayout()
        layout.addWidget(media_bin, 0, 0)
        layout.addWidget(control_panel, 1, 0)
        widget = QWidget()
        widget.setLayout(layout)
        self.setWindowTitle('Video Player')
        self.move(0, 0)
        self.setCentralWidget(widget)
        self.show()


try:
    # stylesheet
    import qdarkstyle
except Exception as error:
    print('failed ' + str(error))

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
