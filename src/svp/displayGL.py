#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Display Class
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy, QOpenGLWidget

from PyQt5.QtGui import QPixmap
from PyQt5.Qt import *
from PyQt5.QtCore import QSize

import random
import math

class DisplayGL(QOpenGLWidget):
    size_changed = pyqtSignal(QSize)
    active_changed = pyqtSignal(bool)
    fullscreen_changed = pyqtSignal(bool)
    freeze_changed = pyqtSignal(bool)
    source_changed = pyqtSignal(int)
    def __init__(self, name=None, active=False, source=None, mode=None, parent=None):
        super(DisplayGL, self).__init__(parent)
        midnight = QTime(0, 0, 0)
        random.seed(midnight.secsTo(QTime.currentTime()))

        self.object = 0
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.image = QImage()
        self.bubbles = []
        self.lastPos = QPoint()

        self.trolltechGreen = QColor.fromCmykF(0.40, 0.0, 1.0, 0.0)
        self.trolltechPurple = QColor.fromCmykF(0.39, 0.39, 0.0, 0.0)

        self.animationTimer = QTimer()
        self.animationTimer.setSingleShot(False)
        self.animationTimer.timeout.connect(self.animate)
        self.animationTimer.start(25)

        self.setAutoFillBackground(False)
        self.setMinimumSize(200, 200)
        self.setWindowTitle("Overpainting a Scene")



        self.name = name
        self._freeze = False
        self._source = None
        self.source = source
        self._size = [320, 180]
        #self.setMinimumSize(320, 180)
        #self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self._fullscreen = False
        #self.setAlignment(Qt.AlignCenter)
        self.active = active



    def setXRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.xRot:
            self.xRot = angle

    def setYRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.yRot:
            self.yRot = angle

    def setZRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.zRot:
            self.zRot = angle

    def initializeGL(self):
        self.gl = self.context().versionFunctions()
        self.gl.initializeOpenGLFunctions()

        self.object = self.makeObject()

    def mousePressEvent(self, event):
        self.lastPos = event.pos()

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        if event.buttons() & Qt.LeftButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setYRotation(self.yRot + 8 * dx)
        elif event.buttons() & Qt.RightButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setZRotation(self.zRot + 8 * dx)

        self.lastPos = event.pos()

    def paintEvent(self, event):
        self.makeCurrent()

        self.gl.glMatrixMode(self.gl.GL_MODELVIEW)
        self.gl.glPushMatrix()

        self.setClearColor(self.trolltechPurple.darker())
        self.gl.glShadeModel(self.gl.GL_SMOOTH)
        self.gl.glEnable(self.gl.GL_DEPTH_TEST)
        #self.gl.glEnable(self.gl.GL_CULL_FACE)
        self.gl.glEnable(self.gl.GL_LIGHTING)
        self.gl.glEnable(self.gl.GL_LIGHT0)
        self.gl.glEnable(self.gl.GL_MULTISAMPLE)
        self.gl.glLightfv(self.gl.GL_LIGHT0, self.gl.GL_POSITION,
                (0.5, 5.0, 7.0, 1.0))

        self.setupViewport(self.width(), self.height())

        self.gl.glClear(
                self.gl.GL_COLOR_BUFFER_BIT | self.gl.GL_DEPTH_BUFFER_BIT)
        self.gl.glLoadIdentity()
        self.gl.glTranslated(0.0, 0.0, -10.0)
        self.gl.glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
        self.gl.glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
        self.gl.glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)
        self.gl.glCallList(self.object)

        self.gl.glMatrixMode(self.gl.GL_MODELVIEW)
        self.gl.glPopMatrix()

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        for bubble in self.bubbles:
            if bubble.rect().intersects(QRectF(event.rect())):
                bubble.drawBubble(painter)

        self.drawInstructions(painter)
        painter.end()

    def resizeGL(self, width, height):
        self.setupViewport(width, height)


    def sizeHint(self):
        return QSize(400, 400)

    def makeObject(self):
        list = self.gl.glGenLists(1)
        self.gl.glNewList(list, self.gl.GL_COMPILE)

        self.gl.glEnable(self.gl.GL_NORMALIZE)
        self.gl.glBegin(self.gl.GL_QUADS)

        self.gl.glMaterialfv(self.gl.GL_FRONT, self.gl.GL_DIFFUSE,
                (self.trolltechGreen.red()/255.0,
                 self.trolltechGreen.green()/255.0,
                 self.trolltechGreen.blue()/255.0, 1.0))

        x1 = +0.06
        y1 = -0.14
        x2 = +0.14
        y2 = -0.06
        x3 = +0.08
        y3 = +0.00
        x4 = +0.30
        y4 = +0.22

        self.quad(x1, y1, x2, y2, y2, x2, y1, x1)
        self.quad(x3, y3, x4, y4, y4, x4, y3, x3)

        self.extrude(x1, y1, x2, y2)
        self.extrude(x2, y2, y2, x2)
        self.extrude(y2, x2, y1, x1)
        self.extrude(y1, x1, x1, y1)
        self.extrude(x3, y3, x4, y4)
        self.extrude(x4, y4, y4, x4)
        self.extrude(y4, x4, y3, x3)

        NumSectors = 200

        for i in range(NumSectors):
            angle1 = (i * 2 * math.pi) / NumSectors
            x5 = 0.30 * math.sin(angle1)
            y5 = 0.30 * math.cos(angle1)
            x6 = 0.20 * math.sin(angle1)
            y6 = 0.20 * math.cos(angle1)

            angle2 = ((i + 1) * 2 * math.pi) / NumSectors
            x7 = 0.20 * math.sin(angle2)
            y7 = 0.20 * math.cos(angle2)
            x8 = 0.30 * math.sin(angle2)
            y8 = 0.30 * math.cos(angle2)

            self.quad(x5, y5, x6, y6, x7, y7, x8, y8)

            self.extrude(x6, y6, x7, y7)
            self.extrude(x8, y8, x5, y5)

        self.gl.glEnd()

        self.gl.glEndList()
        return list

    def quad(self, x1, y1, x2, y2, x3, y3, x4, y4):
        self.gl.glNormal3d(0.0, 0.0, -1.0)
        self.gl.glVertex3d(x1, y1, -0.05)
        self.gl.glVertex3d(x2, y2, -0.05)
        self.gl.glVertex3d(x3, y3, -0.05)
        self.gl.glVertex3d(x4, y4, -0.05)

        self.gl.glNormal3d(0.0, 0.0, 1.0)
        self.gl.glVertex3d(x4, y4, +0.05)
        self.gl.glVertex3d(x3, y3, +0.05)
        self.gl.glVertex3d(x2, y2, +0.05)
        self.gl.glVertex3d(x1, y1, +0.05)

    def extrude(self, x1, y1, x2, y2):
        self.setColor(self.trolltechGreen.darker(250 + int(100 * x1)))

        self.gl.glNormal3d((x1 + x2)/2.0, (y1 + y2)/2.0, 0.0)
        self.gl.glVertex3d(x1, y1, +0.05)
        self.gl.glVertex3d(x2, y2, +0.05)
        self.gl.glVertex3d(x2, y2, -0.05)
        self.gl.glVertex3d(x1, y1, -0.05)

    def normalizeAngle(self, angle):
        while angle < 0:
            angle += 360 * 16
        while angle > 360 * 16:
            angle -= 360 * 16
        return angle

    def animate(self):
        for bubble in self.bubbles:
            bubble.move(self.rect())

        self.update()

    def setupViewport(self, width, height):
        side = min(width, height)
        self.gl.glViewport((width - side) // 2, (height - side) // 2, side,
                side)

        self.gl.glMatrixMode(self.gl.GL_PROJECTION)
        self.gl.glLoadIdentity()
        self.gl.glOrtho(-0.5, +0.5, +0.5, -0.5, 4.0, 15.0)
        self.gl.glMatrixMode(self.gl.GL_MODELVIEW)

    def drawInstructions(self, painter):
        text = "Click and drag with the left mouse button to rotate the Qt " \
                "logo."
        metrics = QFontMetrics(self.font())
        border = max(4, metrics.leading())

        rect = metrics.boundingRect(0, 0, self.width() - 2*border,
                int(self.height()*0.125), Qt.AlignCenter | Qt.TextWordWrap,
                text)
        painter.setRenderHint(QPainter.TextAntialiasing)
        painter.fillRect(QRect(0, 0, self.width(), rect.height() + 2*border),
                QColor(0, 0, 0, 127))
        painter.setPen(Qt.white)
        painter.fillRect(QRect(0, 0, self.width(), rect.height() + 2*border),
                QColor(0, 0, 0, 127))
        painter.drawText((self.width() - rect.width())/2, border, rect.width(),
                rect.height(), Qt.AlignCenter | Qt.TextWordWrap, text)

    def setClearColor(self, c):
        self.gl.glClearColor(c.redF(), c.greenF(), c.blueF(), c.alphaF())

    def setColor(self, c):
        self.gl.glColor4f(c.redF(), c.greenF(), c.blueF(), c.alphaF())










    def clear(self):
        self.setPixmap(QPixmap())

    def new_frame(self, pix):
        if not self.freeze:
            # scale the QPixmap to the display size (pixels)
            # todo : give  modes for fillin / keep ratio etc…
            pix = pix.scaled(self.size(), Qt.KeepAspectRatio)
            #self.setPixmap(pix)

    @property
    def source(self):
        return self._source
    @source.setter
    def source(self, source):
        if self._source:
            try:
                self._source.new_frame.disconnect(self.new_frame)
                self._source.clear.disconnect(self.clear)
            except:
                pass
            if source:
                self._source.new_frame.connect(self.new_frame)
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