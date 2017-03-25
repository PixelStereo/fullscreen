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
    new_frame = pyqtSignal(QPixmap)
    new_load = pyqtSignal()
    new_frame_index = pyqtSignal(int)
    clear = pyqtSignal()

    def __init__(self, name, filepath):
        super(QWidget, self).__init__()
        self.name = name
        self._loop = 'repeat'
        self.frames = 0
        self.loop_points = None
        # set openCV capture
        self.cap = cv2.VideoCapture()
        self.autostart = True
        self.current_frame = None
        self.timer = QTimer()
        self.fps = 25
        self._play = False
        self.timer.timeout.connect(self.render_frame)
        #self.filepath = filepath
        if filepath:
            self.load(filepath)

    def __repr__(self):
        return self.name

    @property
    def fps(self):
        return 1000./self.timer.interval()
    @fps.setter
    def fps(self, fps):
        self.timer.setInterval(1000./fps)

    def render_frame(self):
        ret, frame = self.cap.read()
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        if ret:
            img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            img = img.rgbSwapped()
            pix = QPixmap.fromImage(img)
            current_frame = self.cap.get(1)
            #print('render frame : ' + str(current_frame))
            # emit the new frame signal
            self.new_frame.emit(pix)
            self.new_frame_index.emit(current_frame)
            if current_frame == self.frames:
                print(self.loop)
                if self.loop == 'repeat':
                    self.seek(0)
                elif self.loop == 'one-shot':
                    self.end_action()
                else:
                    self.end_action()
        else:
            print('nothing to play')

    def end_action(self, action='eject'):
        if action == 'loop':
            self.seek(0)
        elif action == 'freeze':
            self.play = False
        elif action == 'eject':
            self.eject()


    def load(self, filepath):
        # release first the previous playhead if existing
        if self.cap:
            self.cap.release()
        # store filepath
        self.filepath = filepath
        try:
            # open the capture
            self.cap.open(self.filepath)
            ret, frame = self.cap.read()
            if ret:
                try:
                    # get properties of the movie
                    self.width = self.cap.get(3)
                    self.height = self.cap.get(4)
                    self.frames = self.cap.get(7)
                    self.fps = (self.cap.get(5))
                    self.loop_points = [0, self.frames]
                    print(self.filepath.split('/')[-1], self.fps, self.width, self.height)
                    self.render_frame()
                    if self.autostart:
                        self.play = True
                    self.new_load.emit()
                except:
                    print('cannot access to the movie')
        except:
            print('cannot open the file')

    @property
    def loop(self):
        return self._loop
    @loop.setter
    def loop(self, mode):
        self._loop = mode

    @property
    def loop_points(self):
        return self._loop_points
    @loop_points.setter
    def loop_points(self, points):
        print('loop_point setter : ', points)
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
            # set playhead to the desired frame
            self.cap.set(1, frame)
            # render the frame
            self.render_frame()
        else:
            print('frame ' + str(frame) + ' does not exist')

    def pause(self):
        """
        calling this method will pause the media
        same effect than self.play = 0
        """
        self.play = False
    
    def resume(self):
        """
        calling this methid will play the media
        same effect than self.play = 1
        """
        self.play = True

    @property
    def play(self):
        """
        The play property
        if set to True, media is playing
        if set to False, media is pausing
        """
        return self._play
    @play.setter
    def play(self, state):
        self._play = state
        if state:
            self.timer.start()
        else:
            self.timer.stop()

    def eject(self):
        """
        unload the media from the player
        """
        # release the player
        self.cap.release()
        self.pause()
        self.clear.emit()
