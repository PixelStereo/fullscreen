#! /usr/bin/env python
# -*- coding: utf-8 -*-
from OpenGL import GL
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtOpenGL import *

class PaintWidget(QGLWidget):
	"""docstring for PaintWidget"""
	def __init__(self, filepath=None, parent=None):
		super(PaintWidget, self).__init__()
		self.filepath = filepath
		self.parent = parent
		self.data = QImage()
		self.data = QImage()
		self.data.load('/Users/reno/dropbox/media/testcard.png')
		self.gldata = QGLWidget.convertToGLFormat(self.data)
		#self.gldata.resize(self.data.size())

	def paintGL(self):
		GL.glDrawPixels(self.data.width(), self.data.height(), GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, self.gldata.bits())

	def resizeGL(self, widht, height):
		GL.glViewport (0, 0, widht, height)
		GL.glMatrixMode (GL.GL_PROJECTION);    
		GL.glLoadIdentity()
		GL.glOrtho(0,  widht, 0, height, -1, 1)
		GL.glMatrixMode (GL.GL_MODELVIEW)



if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    try:
        # stylesheet
        import qdarkstyle
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        pass
    except:
        pass

    window = PaintWidget()
    window.show()
    sys.exit(app.exec_())
