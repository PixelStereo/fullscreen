#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Player Class
"""

from PyQt5.QtWidgets import QListWidget, QWidget, QLabel, QPushButton, QGridLayout, QGroupBox, QHBoxLayout, QListWidgetItem
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
import os
from PyQt5.Qt import *

from svp.api import new_display
from svp.RangeSlider import QHSpinBoxRangeSlider

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
        # filepath UI
        self.filepath_label = QLabel(self.player.filepath)
        # Autostart
        self.autostart_button = QCheckBox('Autostart')
        self.autostart_button.toggled.connect(self.autostart)
        self.autostart_button.setChecked(self.player.autostart)
        # looppoints
        self.looppoints_slider = QHSpinBoxRangeSlider([0, 100, 1], [0, 100])
        self.looppoints_slider.rangeChanged.connect(self.loop_points)
        #setRange setValues

        # Play / Pause Button
        self.playpause_button = QCheckBox('Play')
        self.playpause_button.setCheckable(True)
        self.playpause_button.toggled.connect(self.playpause)
        # loop
        self.loop_menu = QComboBox()
        self.loop_menu.addItem('one-shot')
        self.loop_menu.addItem('repeat')
        self.loop_menu.addItem('palindrome')
        self.loop_menu.currentTextChanged.connect(self.loop)
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
        self.player.clear.connect(self.updateFrameUIs)
        # Transport Group
        self.files = QGroupBox()
        self.files_layout = QGridLayout()
        self.files.setLayout(self.files_layout)
        self.files_layout.addWidget(self.media_bin)
        # Transport Group
        self.control = QGroupBox()
        self.control_layout = QGridLayout()
        self.control.setLayout(self.control_layout)
        self.control.setFixedSize(600, 480)
        self.control_layout.addWidget(self.files, 0, 0, 2, 4)
        self.control_layout.addWidget(self.filepath_label, 5, 0, 1, 4)
        self.control_layout.addWidget(self.playpause_button, 6, 0, 1, 1)
        self.control_layout.addWidget(self.loop_menu, 6, 1, 1, 1)
        self.control_layout.addWidget(self.autostart_button, 6, 2, 1, 1)
        self.control_layout.addWidget(self.eject_button, 6, 3, 1, 1)
        self.control_layout.addWidget(self.frameSlider, 7, 0, 1, 4)
        self.control_layout.addWidget(self.frame, 7, 5, 1, 1)
        self.control_layout.addWidget(self.looppoints_slider, 8, 0, 4, 4)
        # General Layout
        self.general_layout = QHBoxLayout()
        self.general_layout.addWidget(self.control)
        self.setLayout(self.general_layout)
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

    def updateFrameUIs(self, frame=0):
        if not self.frameSlider.isSliderDown():
            hasFrames = (frame >= 0)
            if hasFrames:
                if self.player.frames > 0:
                    self.frameSlider.setMaximum(self.player.frames - 1)
                    self.looppoints_slider.setRange([0, self.player.frames - 1])
                elif frame > self.frameSlider.maximum():
                    self.frameSlider.setMaximum([0, frame])
                    self.looppoints_slider.setRange(frame)
                self.playpause_button.setChecked(self.player.play)
                self.frameSlider.setValue(frame)
            else:
                self.frameSlider.setMaximum(0)
                self.looppoints_slider.setRange([0, 0])
            self.looppoints_slider.setEnabled(hasFrames)
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

    def loop(self, mode):
        self.player.loop = mode

    def loop_points(self, range):
        self.player.loop_points = range

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
