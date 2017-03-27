#!/usr/bin/env python


import sys
import math, random

from PyQt5.QtCore import (QPoint, QPointF, QRect, QRectF, QSize, Qt, QTime,
        QTimer)
from PyQt5.QtGui import (QBrush, QColor, QFontMetrics, QImage, QPainter,
        QRadialGradient, QSurfaceFormat)
from PyQt5.QtWidgets import QApplication, QOpenGLWidget


class GLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)
        self.image = QImage('uno.png')
        self.setMinimumSize(640, 480)
        self.move(0, 0)

    def initializeGL(self):
        self.gl = self.context().versionFunctions()
        self.gl.initializeOpenGLFunctions()

        self.object = self.makeObject()

    def paintEvent(self, event):
        self.makeCurrent()

        self.gl.glMatrixMode(self.gl.GL_MODELVIEW)
        self.gl.glPushMatrix()
        self.gl.glClearColor(0, 0.6, 0.92, 1)
        self.gl.glShadeModel(self.gl.GL_SMOOTH)
        self.gl.glEnable(self.gl.GL_DEPTH_TEST)
        #self.gl.glEnable(self.gl.GL_CULL_FACE)
        self.gl.glEnable(self.gl.GL_LIGHTING)
        self.gl.glEnable(self.gl.GL_LIGHT0)
        self.gl.glEnable(self.gl.GL_MULTISAMPLE)
        
        self.gl.glClear(
                self.gl.GL_COLOR_BUFFER_BIT | self.gl.GL_DEPTH_BUFFER_BIT)
        self.gl.glLoadIdentity()
        self.gl.glTranslated(0.0, -1.4, -10.0)
        #self.gl.glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
        #self.gl.glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
        #self.gl.glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)
        self.gl.glCallList(self.object)

        self.gl.glMatrixMode(self.gl.GL_MODELVIEW)
        self.gl.glPopMatrix()


    def resizeGL(self, width, height):
        self.setupViewport(width, height)

    def showEvent(self, event):
        print('show')

    def sizeHint(self):
        return QSize(400, 400)

    def makeObject(self):
        list = self.gl.glGenLists(1)
        print('-', list)
        self.gl.glNewList(list, self.gl.GL_COMPILE)
        self.gl.glEnable(self.gl.GL_NORMALIZE)
        self.gl.glBegin(self.gl.GL_QUADS)
        x1 = -10
        y1 = 10
        x2 = 30
        y2 = 30
        x3 = -30
        y3 = -30
        x4 = 30
        y4 = -30
        self.quad(x1, y1, x2, y2, y2, x2, y1, x1)
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

    def normalizeAngle(self, angle):
        while angle < 0:
            angle += 360 * 16
        while angle > 360 * 16:
            angle -= 360 * 16
        return angle

    def animate(self):
        #print('animate')
        self.update()

    def setupViewport(self, width, height):
        side = min(width, height)
        self.gl.glViewport((width - side) // 2, (height - side) // 2, side,
                side)

        self.gl.glMatrixMode(self.gl.GL_PROJECTION)
        self.gl.glLoadIdentity()
        self.gl.glOrtho(-0.5, +0.5, +0.5, -0.5, 4.0, 15.0)
        self.gl.glMatrixMode(self.gl.GL_MODELVIEW)


if __name__ == '__main__':

    app = QApplication(sys.argv)

    fmt = QSurfaceFormat()
    fmt.setSamples(4)
    QSurfaceFormat.setDefaultFormat(fmt)

    window = GLWidget()
    window.show()
    sys.exit(app.exec_())
