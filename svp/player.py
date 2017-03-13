#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Player Class
"""

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
import cv2
from PyQt5.QtCore import pyqtSignal

class Player(QWidget):
    # signal that there is a new frame for the selected universe
    new_frame = pyqtSignal()

    def __init__(self, filepath):
        super(QWidget, self).__init__()
        # store displays
        self._displays = []
        # set openCV capture
        self.cap = cv2.VideoCapture()
        self.autostart = True
        self.current_frame = None
        self.loop_points = None
        self.filepath = filepath
        self.timer = QTimer()
        self.fps = 25
        self._play = False
        self.timer.timeout.connect(self.render_frame)

    @property
    def fps(self):
        return 1000./self.timer.interval()
    @fps.setter
    def fps(self, fps):
        self.timer.setInterval(1000./fps)

    def addDisplay(self, display):
        self._displays.append(display)

    def render_frame(self):
        ret, frame = self.cap.read()
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        if ret:
            img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            pix = QPixmap.fromImage(img)
            self.current_frame = self.cap.get(1)
            # emit the new frame signal
            self.new_frame.emit()
            if self._displays:
                for display in self._displays:
                    if display.available:
                        display.video_frame.setPixmap(pix)
        else:
            self.eject()

    def load(self, filepath):
        # release first the previous playhead if existing
        if self.cap:
            self.cap.release()
        # store filepath
        self.filepath = filepath
        # open the capture
        self.cap.open(self.filepath)

        ret, frame = self.cap.read()
        if ret:
            try:
                # get properties of the movie
                self.width = self.cap.get(3)
                self.height = self.cap.get(4)
                self.fps = (self.cap.get(5))
                self.frames = self.cap.get(7)
                self.loop_points = [0, self.frames]
                print(self.filepath.split('/')[-1], self.fps, self.width, self.height)
                if self.autostart:
                    self.play = True
            except:
                print('skip frame')

    @property
    def loop_points(self):
        return self._loop_points
    @loop_points.setter
    def loop_points(self, points):
        self._loop_points = points

    @property
    def autostart(self):
        """
        if True, player will start when load a movie
        if False, player will load the movie and 
        """
        return self._autostart
    @autostart.setter
    def autostart(self, state):
        self._autostart = state

    def seek(self, frame):
        # check that the frame exists
        if frame <= self.frames:
            # the frame exists, check if player is running
            self.cap.set(1, frame)
            self.render_frame()
        else:
            print('frame ' + str(frame) + ' does not exist')

    def pause(self):
        self.play = False
    
    def resume(self):
        self.play = True

    @property
    def play(self):
        return self._play
    @play.setter
    def play(self, state):
        self._play = state
        if state:
            self.timer.start()
        else:
            self.timer.stop()

    def eject(self):
        self.cap.release()
        self.pause()
        for display in self._displays:
            if display.available:
                display.clear()
