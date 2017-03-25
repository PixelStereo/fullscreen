#! /usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import svp
from svp.api import new_player, new_display, get_players
from svp.player_ui import PlayerUI
from svp.bins.display_bin import DisplaysList
from svp.bins.media_bin import MediaBin


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        player = new_player('Player Uno', '/Users/reno/Dropbox/media/cloudy.mov')
        player2 = new_player('Player Dos', '/Users/reno/Dropbox/media/galets.mov')
        window = new_display('Desktop Display', True, player)
        window2 = new_display('Second Display', True, player2)
        window.setEnabled(True)
        player_ui = PlayerUI(player)
        player2_ui = PlayerUI(player2)
        """
        MEDIA BIN

        media_bin = MediaBin('/Users/reno/Dropbox')
        # create a media_bin
        media_bin.selection.connect(self.player.load)
        media_bin.selection.connect(self.player2.load)
        self.player.clear.connect(media_bin.clearSelection)
        self.player2.clear.connect(media_bin.clearSelection)
        """
        display_control = DisplaysList()
        layout = QGridLayout()
        """
        MEDIA BIN

        layout.addWidget(media_bin, 0, 0, 6, 6)
        """
        layout.addWidget(player_ui, 0, 7, 2, 2)
        layout.addWidget(player2_ui, 3, 7, 2, 2)
        layout.addWidget(display_control, 0, 9, 6, 6)
        widget = QWidget()
        widget.setLayout(layout)
        self.setWindowTitle('Video Player')
        self.setCentralWidget(widget)
        self.show()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    try:
        # stylesheet
        import qdarkstyle
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        pass
    except:
        pass
    window = MainWindow()
    sys.exit(app.exec_())
