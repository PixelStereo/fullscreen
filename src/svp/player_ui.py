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

from svp.widgets.RangeSlider import QHSpinBoxRangeSlider

class PlayerUI(QGroupBox):
    """
    """
    def __init__(self, player):
        super(PlayerUI, self).__init__()
        # which player
        self.player = player
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
        self.player.new_load.connect(self.loop_points_changed)
        #self.looppoints_slider.resize(200, 10)
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
        self.loop_menu.setCurrentText(self.player.loop)
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


        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.setFixedSize(400, 200)
        self.layout.addWidget(self.filepath_label, 3, 0, 1, 8)
        self.layout.addWidget(self.playpause_button, 4, 0, 1, 1)
        self.layout.addWidget(self.autostart_button, 4, 3, 1, 1)
        self.layout.addWidget(self.loop_menu, 4, 5, 1, 2)
        self.layout.addWidget(self.eject_button, 4, 8, 1, 1)
        self.layout.addWidget(self.frameSlider, 5, 0, 1, 8)
        self.layout.addWidget(self.frame, 5, 9, 1, 1)
        self.layout.addWidget(self.looppoints_slider, 6, 0, 1, 10)

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
                    self.looppoints_slider.setDomain([0, self.player.frames - 1])
                elif frame > self.frameSlider.maximum():
                    self.frameSlider.setMaximum([0, frame])
                    self.looppoints_slider.setDomain(frame)
                self.playpause_button.setChecked(self.player.play)
                self.frameSlider.setValue(frame)
            else:
                self.frameSlider.setMaximum(0)
                self.looppoints_slider.setDomain([0, 0])
            self.looppoints_slider.setEnabled(hasFrames)
            self.frameSlider.setEnabled(hasFrames)
            self.frame.setEnabled(hasFrames)
        self.frame.setText(str(frame))

    def loop_points_changed(self):
        self.looppoints_slider.setDomain([0, self.player.frames])
        self.looppoints_slider.setRange([0, self.player.frames])

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
        print('range', range)
        self.player.loop_points = range

    @property
    def filepath(self):
        return self.player.filepath
    @filepath.setter
    def filepath(self, filepath):
        self.player.filepath = filepath

    def load(self, filepath):
        self.filepath_label.setText(filepath.split('/')[-1])
        self.player.load(filepath)
