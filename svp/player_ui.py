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

from svp.api import new_display

class PlayerUI(QWidget):
    """
    """
    def __init__(self, player, media_bin=None):
        super(PlayerUI, self).__init__()
        # create a media_bin
        self.media_bin = MediaBin(self, '/Users/reno/Dropbox')
        # create a player
        self.player = player
        self.player.clear.connect(self.media_bin.clearSelection)
        # What are these 2 lines?
        #self.player.setParent(self)
        #self.player.setWindowFlags(Qt.Tool)
        # create an embeded preview window 
        self.preview = new_display('Preview', True, self.player)
        # filepath UI
        self.filepath_label = QLabel(self.player.filepath)
        # Mute Button
        self.mute_button = QPushButton('Black')
        self.mute_button.setCheckable(True)
        self.mute_button.toggled.connect(self.preview.mute)
        # Autostart
        self.autostart_button = QCheckBox('Autostart')
        self.autostart_button.toggled.connect(self.autostart)
        self.autostart_button.setChecked(self.player.autostart)
        # Play / Pause Button
        self.playpause_button = QCheckBox('Play')
        self.playpause_button.setCheckable(True)
        self.playpause_button.toggled.connect(self.playpause)
        self.playpause_button.setChecked(self.player.play)
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
        self.frame = QLabel()
        self.frame.setMinimumWidth(60)
        # new frame from player update slider's value
        self.player.new_frame_index.connect(self.updateFrameUIs)
        # make a nice layout of buttons
        self.control_layout = QGridLayout()
        self.control_layout.addWidget(self.media_bin, 0, 0, 4, 2)
        self.control_layout.addWidget(self.filepath_label, 5, 0, 1, 4)
        self.control_layout.addWidget(self.playpause_button, 0, 3, 1, 1)
        self.control_layout.addWidget(self.autostart_button, 1, 3, 1, 1)
        self.control_layout.addWidget(self.eject_button, 2, 3, 1, 1)
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


    def updateFrameUIs(self, frame):
        if not self.frameSlider.isSliderDown():
            hasFrames = (frame >= 0)
            if hasFrames:
                if self.player.frames > 0:
                    self.frameSlider.setMaximum(self.player.frames - 1)
                elif frame > self.frameSlider.maximum():
                    self.frameSlider.setMaximum(frame)
                print('update : ' + str(frame))
                self.frameSlider.setValue(frame)
            else:
                self.frameSlider.setMaximum(0)
            self.frameSlider.setEnabled(hasFrames)
            self.frame.setEnabled(hasFrames)
        self.frame.setText(str(frame))

    def playpause(self, state):
        if state:
            self.player.play = True
        else:
            self.player.pause()

    def autostart(self, state):
        self.player.autostart = state

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
