#!/usr/bin/env python

import sys

from PyQt5.QtCore import pyqtSignal, QFileInfo, QPoint, QSize, Qt, QTimer
from PyQt5.QtGui import (QColor, QImage, QMatrix4x4, QOpenGLShader,
        QOpenGLShaderProgram, QOpenGLTexture, QSurfaceFormat)
from PyQt5.QtWidgets import QApplication, QGridLayout, QOpenGLWidget, QWidget


class GLWidget(QOpenGLWidget):

    clicked = pyqtSignal()

    PROGRAM_VERTEX_ATTRIBUTE, PROGRAM_TEXCOORD_ATTRIBUTE = range(2)

    vsrc = """
attribute highp vec4 vertex;
attribute mediump vec4 texCoord;
varying mediump vec4 texc;
uniform mediump mat4 matrix;
void main(void)
{
    gl_Position = matrix * vertex;
    texc = texCoord;
}
"""

    fsrc = """
uniform sampler2D texture;
varying mediump vec4 texc;
void main(void)
{
    gl_FragColor = texture2D(texture, texc.st);
}
"""

    coords = (
        (( +1, -1, -1 ), ( -1, -1, -1 ), ( -1, +1, -1 ), ( +1, +1, -1 )),
        (( +1, +1, -1 ), ( -1, +1, -1 ), ( -1, +1, +1 ), ( +1, +1, +1 )),
        (( +1, -1, +1 ), ( +1, -1, -1 ), ( +1, +1, -1 ), ( +1, +1, +1 )),
        (( -1, -1, -1 ), ( -1, -1, +1 ), ( -1, +1, +1 ), ( -1, +1, -1 )),
        (( +1, -1, +1 ), ( -1, -1, +1 ), ( -1, -1, -1 ), ( +1, -1, -1 )),
        (( -1, -1, +1 ), ( +1, -1, +1 ), ( +1, +1, +1 ), ( -1, +1, +1 ))
    )

    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)

        self.clearColor = QColor(Qt.black)
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.program = None

        self.lastPos = QPoint()

    def minimumSizeHint(self):
        """
        Define the minimum size of the widget
        """
        return QSize(50, 50)

    def sizeHint(self):
        """
        Define a default size for the widget
        """
        return QSize(200, 200)

    def rotateBy(self, xAngle, yAngle, zAngle):
        self.xRot += xAngle
        self.yRot += yAngle
        self.zRot += zAngle
        self.update()

    def setClearColor(self, color):
        self.clearColor = color
        self.update()

    def initializeGL(self):
        self.gl = self.context().versionFunctions()
        self.gl.initializeOpenGLFunctions()

        self.makeObject()

        self.gl.glEnable(self.gl.GL_DEPTH_TEST)
        self.gl.glEnable(self.gl.GL_CULL_FACE)

        vshader = QOpenGLShader(QOpenGLShader.Vertex, self)
        vshader.compileSourceCode(self.vsrc)

        fshader = QOpenGLShader(QOpenGLShader.Fragment, self)
        fshader.compileSourceCode(self.fsrc)

        self.program = QOpenGLShaderProgram()
        self.program.addShader(vshader)
        self.program.addShader(fshader)
        self.program.bindAttributeLocation('vertex',
                self.PROGRAM_VERTEX_ATTRIBUTE)
        self.program.bindAttributeLocation('texCoord',
                self.PROGRAM_TEXCOORD_ATTRIBUTE)
        self.program.link()

        self.program.bind()
        self.program.setUniformValue('texture', 0)

        self.program.enableAttributeArray(self.PROGRAM_VERTEX_ATTRIBUTE)
        self.program.enableAttributeArray(self.PROGRAM_TEXCOORD_ATTRIBUTE)
        self.program.setAttributeArray(self.PROGRAM_VERTEX_ATTRIBUTE,
                self.vertices)
        self.program.setAttributeArray(self.PROGRAM_TEXCOORD_ATTRIBUTE,
                self.texCoords)

    def paintGL(self):
        self.gl.glClearColor(self.clearColor.redF(), self.clearColor.greenF(),
                self.clearColor.blueF(), self.clearColor.alphaF())
        self.gl.glClear(
                self.gl.GL_COLOR_BUFFER_BIT | self.gl.GL_DEPTH_BUFFER_BIT)

        m = QMatrix4x4()
        m.ortho(-0.5, 0.5, 0.5, -0.5, 4.0, 15.0)
        m.translate(0.0, 0.0, -10.0)

        self.program.setUniformValue('matrix', m)

        self.texture.bind()
        self.gl.glDrawArrays(self.gl.GL_TRIANGLE_FAN, 0, 4)

    def resizeGL(self, width, height):
        side = min(width, height)
        self.gl.glViewport((width - side) // 2, (height - side) // 2, side,
                side)


    def makeObject(self):
        self.texCoords = [(True, True), (False, True), (False, False), (True, False)]
        self.vertices = [(0.5, -0.5, -0.5), (-0.5, -0.5, -0.5), (-0.5, 0.5, -0.5), (0.5, 0.5, -0.5)]

        my_movie = QImage('/Users/reno/Dropbox/media/cloudy.png')
        self.texture = QOpenGLTexture(
                            my_movie.mirrored())

class Window(QWidget):

    def __init__(self):
        super(Window, self).__init__()

        self.glWidgets = []

        mainLayout = QGridLayout()

        clearColor = QColor()

        widget = GLWidget()
        widget.setClearColor(clearColor)
        mainLayout.addWidget(widget)
        self.setLayout(mainLayout)

        timer = QTimer(self)
        timer.start(20)

        self.setWindowTitle("Textures")



if __name__ == '__main__':

    app = QApplication(sys.argv)

    format = QSurfaceFormat()
    format.setDepthBufferSize(24)
    QSurfaceFormat.setDefaultFormat(format)

    window = Window()
    window.show()
    sys.exit(app.exec_())
