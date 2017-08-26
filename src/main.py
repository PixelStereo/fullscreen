#! /usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QOpenGLWidget, QGroupBox
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import svp
from svp.UI.player import PlayerUI
from svp.Sources.player import SmartPlayer, Player
from svp.window import Window
from svp.layer import Layer
from svp.UI.windows import WindowsList
from svp.UI.layers import LayersList
from svp.UI.players import PlayersList
from svp.UI.media_bin import MediaBin


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        player = Player(name='Ein Player', filepath='/Users/reno/Library/Mobile Documents/com~apple~CloudDocs/Media/Video/Photo Jpeg/cloudy.mov')
        player2 = Player(name='Second Player', filepath='/Users/reno/Library/Mobile Documents/com~apple~CloudDocs/Media/Video/Photo Jpeg/galets.mov')
        layer = Layer(name='Desktop Display', active=True, source=player)
        layer2 = Layer(name='Second Display', active=True, source=player2)
        window = Window(name='First Window', active=True, layers=[layer, layer2])
        layer_list = LayersList()
        player_list = PlayersList()
        window_list = WindowsList()
        layout = QGridLayout()

        """
        MEDIA BIN
        media_bin = MediaBin('/Users/reno/Dropbox')
        # create a media_bin
        media_bin.selection.connect(self.player.load)
        media_bin.selection.connect(self.player2.load)
        self.player.clear.connect(media_bin.clearSelection)
        self.player2.clear.connect(media_bin.clearSelection)
        
        layout.addWidget(media_bin, 0, 0, 6, 6)
        """
        players = QGroupBox('Players')
        layers = QGroupBox('Layers')
        windows = QGroupBox('Windows')
        players_layout = QGridLayout()
        players_layout.addWidget(player_list)
        players.setLayout(players_layout)
        layers_layout = QGridLayout()
        layers_layout.addWidget(layer_list)
        layers.setLayout(layers_layout)
        windows_layout = QGridLayout()
        windows_layout.addWidget(window_list)
        windows.setLayout(windows_layout)
        layout.addWidget(players, 0, 7, 2, 2)
        layout.addWidget(layers, 0, 9, 6, 6)
        layout.addWidget(windows, 0, 15, 6, 6)
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

    format = QSurfaceFormat()
    format.setDepthBufferSize(24)
    QSurfaceFormat.setDefaultFormat(format)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
