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
        # create a media_bin
        self.media_bin = MediaBin(self, '/Users/reno/Dropbox')
        # create a player
        self.player = player
        # What are these 2 lines?
        #self.player.setParent(self)
        #self.player.setWindowFlags(Qt.Tool)
        # create an embeded preview window 
        self.preview = new_display('Preview', False)
        self.player.addDisplay(self.preview)
        # filepath UI
        self.filepath_label = QLabel(self.player.filepath)
        # Mute Button
        self.mute_button = QPushButton('Black')
        self.mute_button.setCheckable(True)
        self.mute_button.toggled.connect(self.preview.mute)
        # Play / Pause Button
        self.playpause_button = QPushButton('Pause')
        self.playpause_button.setCheckable(True)
        self.playpause_button.toggled.connect(self.playpause)
        # self.player.setFPS(1)
        self.eject_button = QPushButton('Eject')
        self.eject_button.clicked.connect(self.player.eject)
        # frame slider 
        self.frameSlider = QSlider(Qt.Horizontal)
        self.frameSlider.setTickPosition(QSlider.TicksBelow)
        self.frameSlider.sliderMoved.connect(self.player.seek)
        self.frameSlider.sliderPressed.connect(self.stop_render)
        self.frameSlider.sliderReleased.connect(self.start_render)
        self.frameSlider.setTickInterval(10)
        self.frame = QSpinBox()
        self.frame.setMinimumWidth(60)
        self.frameSlider.valueChanged.connect(self.frame.setValue)
        # new frame from player update slider's value
        self.player.new_frame.connect(self.updateFrameSlider)
        # make a nice layout of buttons
        self.control_layout = QGridLayout()
        self.control_layout.addWidget(self.media_bin, 0, 0, 4, 2)
        self.control_layout.addWidget(self.filepath_label, 5, 0, 1, 8)
        self.control_layout.addWidget(self.playpause_button, 6, 0, 1, 1)
        self.control_layout.addWidget(self.eject_button, 6, 2, 1, 1)
        self.control_layout.addWidget(self.frameSlider, 7, 0, 1, 1)
        self.control_layout.addWidget(self.frame, 7, 1, 1, 1)
        self.control_layout.addWidget(self.preview, 8, 0, 6, 1)
        self.setLayout(self.control_layout)
        self.media_bin.refresh()

    def start_render(self):
        #self.player.timer.setActive
        if self.player.play:
            self.player.timer.start()

    def stop_render(self):
        # slider is pressed
        if self.frameSlider.value() != self.player.current_frame:
            self.player.seek(self.frameSlider.value())
        if self.player.play:
            self.player.timer.stop()


    def updateFrameSlider(self):
        if not self.frameSlider.isSliderDown():
            hasFrames = (self.player.current_frame >= 0)

            if hasFrames:
                if self.player.frames > 0:
                    self.frameSlider.setMaximum(self.player.frames - 1)
                    self.frame.setMaximum(self.player.frames - 1)
                elif self.player.current_frame > self.frameSlider.maximum():
                    self.frameSlider.setMaximum(self.player.current_frame)
                    self.frame.setMaximum(self.player.current_frame)

                self.frameSlider.setValue(self.player.current_frame)
            else:
                self.frameSlider.setMaximum(0)
                self.frame.setMaximum(0)
            self.frameSlider.setEnabled(hasFrames)
            self.frame.setEnabled(hasFrames)

    def playpause(self, state):
        if state:
            self.playpause_button.setText('playing')
            self.player.play = True
        else:
            self.playpause_button.setText('pausing')
            self.player.pause()

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