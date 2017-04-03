#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Display Class
"""

from PyQt5.QtWidgets import (QApplication, QGraphicsAnchorLayout,
        QGraphicsProxyWidget, QGraphicsScene, QGraphicsView, QGraphicsWidget,
        QPushButton, QSizePolicy, QWidget, QVBoxLayout, QLabel, QSizePolicy, 
        QGraphicsOpacityEffect)

from PyQt5.QtGui import QPixmap, QColor, QSurface
from PyQt5.Qt import *
from PyQt5.QtCore import QSize, QEasingCurve, QSizeF, Qt


def createItem(minimum, preferred, maximum, name):
    w = QGraphicsProxyWidget()

    w.setWidget(QPushButton(name))
    w.setMinimumSize(minimum)
    w.setPreferredSize(preferred)
    w.setMaximumSize(maximum)
    w.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

class Layer(QLabel):
    """
    QLabel pimped to display video
    """
    # signals emited by this class instances
    size_changed = pyqtSignal(QSize)
    active_changed = pyqtSignal(bool)
    fullscreen_changed = pyqtSignal(bool)
    freeze_changed = pyqtSignal(bool)
    source_changed = pyqtSignal(int)
    # create a list for all displays
    __layers__ = []
    # initialisation of each instances
    def __init__(self, name=None, active=True, source=None):
        super(Layer, self).__init__()
        self.name = name
        self._freeze = False
        self._source = None
        self.source = source
        self._size = [640, 480]
        self.setMinimumSize(320, 180)
        self.resize(self._size[0], self._size[1])
        self.setAlignment(Qt.AlignCenter)
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self._fullscreen = False
        self.setAlignment(Qt.AlignCenter)
        self.active = active
        self.__layers__.append(self)
        pos = len(self.__layers__)
        pos = pos - 1
        self.move(0, abs(pos*self.geometry().height()))
        self._display_name = True
        self.opacity = 0.0
        self.fade(target_value=1.0, duration=2000)


    def clear(self):
        self.setPixmap(QPixmap())

    @property
    def display_name(self):
        """
        display the name of the display on it
        """
        return self.__display_name
    @display_name.setter
    def display_name(self, state):
        self._display_name = state

    def new_frame(self, pix):
        if not self.freeze:
            # scale the QPixmap to the display size (pixels)
            # todo : give  modes for fillin / keep ratio etc…
            pix = pix.scaled(self.size(), Qt.KeepAspectRatio)
            painter = QPainter(pix)
            if self._display_name:
                # display window name
                painter.setOpacity(1)
                rect = self.geometry()
                x = pix.width()/3
                y = pix.height()/2
                painter.setPen(QPen(Qt.white))
                painter.drawText(QPoint(x, y), self.name)
            # Degrade output
            # todo : make it as an attribute : display/degrade
            painter.setPen(QPen(Qt.white))
            painter.drawLine(rect.topLeft(), rect.bottomRight())
            painter.drawLine(rect.bottomLeft(), rect.topRight())
            # display a gradient
            gradient = QLinearGradient(QPoint(0, 0), QPoint(x, y))
            gradient.setColorAt(0, Qt.blue)
            gradient.setColorAt(0.4, Qt.cyan)
            gradient.setColorAt(1, Qt.green)
            brush = QBrush(gradient)
            painter.setOpacity(0.2)
            painter.fillRect( QRectF(0, 0, rect.width()-100, rect.width()-100), brush)
            painter.setOpacity(1)
            painter.end()
            # try fade in

            self.setPixmap(pix)

    def fade(self, target_value=1, duration=2000):
        """
        fade layer
        """
        fade = QGraphicsOpacityEffect()
        self.setGraphicsEffect(fade)
        anim = QPropertyAnimation(fade)
        anim.setDuration(duration)
        anim.setStartValue(self.opacity)
        anim.setEndValue(target_value)
        anim.setEasingCurve(QEasingCurve.InBack)
        anim.start()

    @property
    def opacity(self):
        """
        opacity of the layer
        """
        return self._opacity
    @opacity.setter
    def opacity(self, value):
        self._opacity = value


    @property
    def source(self):
        return self._source
    @source.setter
    def source(self, source):
        if self._source:
            try:
                self._source.new_pix.disconnect(self.new_frame)
                self._source.clear.disconnect(self.clear)
            except:
                pass
            if source:
                self._source.new_pix.connect(self.new_frame)
                self._source.clear.connect(self.clear)
            else:
                self.clear()
        self._source = source
        self.source_changed.emit(source)

    @property
    def fullscreen(self):
        return self._fullscreen
    @fullscreen.setter
    def fullscreen(self, state):
        if self.active:
            if state:
                self.showFullScreen()
            else:
                self.showNormal()
            self._fullscreen = state
            self.fullscreen_changed.emit(state)
            return True
        return False

    @property
    def freeze(self):
        return self._freeze
    @freeze.setter
    def freeze(self, state):
        self._freeze = state
        self.freeze_changed.emit(state)

    @property
    def active(self):
        return self.isVisible()
    @active.setter
    def active(self, state):
        if state:
            self.show()
        else:
            self.hide()
        self.active_changed.emit(state)

"""

    def paintEvent(self, event):
        QLabel.paintEvent(self, event)
        pix = QPixmap(QSize(180, 80))
        painter = QPainter(pix)
        painter.setOpacity(0.1)
        rect = self.geometry()
        x = rect.width()/3
        y = rect.height()/2
        painter.setPen(QPen(Qt.red))
        # display window name
        # todo : make it as an attribute : display/name
        painter.drawText(QPoint(x,y), self.name)
        # Degrade output
        # todo : make it as an attribute : display/degrade
        painter.setPen(QPen(Qt.white))
        painter.drawLine(self.rect().topLeft(),self.rect().bottomRight())
        painter.drawLine(self.rect().bottomLeft(),self.rect().topRight())
        # display a gradient
        gradient = QLinearGradient(QPoint(0, 0), QPoint(x, y))
        gradient.setColorAt(0, Qt.blue)
        gradient.setColorAt(0.4, Qt.cyan)
        gradient.setColorAt(1, Qt.green)
        brush = QBrush(gradient)
        painter.fillRect( QRectF(0, 0, 400, 400), brush)
        painter.end()
"""        

"""
    def paintEvent(self, event):
        QLabel.paintEvent(self, event)
        solid = QPixmap(180, 120)
        painter = QPainter()
        painter.begin(solid)
        brush = QBrush(QColor(255, 0, 0))
        painter.fillRect( QRectF(0, 0, 180, 120), brush)
        painter.end()
"""
