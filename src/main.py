#! /usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import os,sys
svp_path = os.path.abspath('..')
sys.path.append(svp_path)

import svp
from svp.api import new_player, new_display, get_players
from svp.player_ui import PlayerUI
from svp.display_control import DisplayControl


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.player = new_player()
        self.window = new_display('Desktop Display', False, self.player)
        self.window.setEnabled(True)
        self.window.move(0, 800)
        player_ui = PlayerUI(self.player)
        display_control = DisplayControl(self.window)
        layout = QGridLayout()
        layout.addWidget(player_ui, 1, 0)
        layout.addWidget(display_control, 1, 0)
        widget = QWidget()
        widget.setLayout(layout)
        self.setWindowTitle('Video Player')
        self.move(0, 0)
        self.setFixedSize(800, 1000)
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
    try:
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        pass
    except Exception as error:
        print('failed ' + str(error))
    window = MainWindow()
    sys.exit(app.exec_())
