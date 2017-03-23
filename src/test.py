#! /usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QGroupBox
from PyQt5.QtCore import *
from PyQt5.QtGui import *


import os,sys
svp_path = os.path.abspath('..')
sys.path.append(svp_path)

from svp.RangeSlider import QHSpinBoxRangeSlider
from svp.FloatSlider import FloatSlider


class MainWindow(QGroupBox):
    def __init__(self):
        super(MainWindow, self).__init__()
        rslider = QHSpinBoxRangeSlider([0.0, 1.0, 0.01], [0.2, 0.8])
        fslider = FloatSlider()
        layout = QGridLayout()
        layout.addWidget(rslider, 0, 0)
        layout.addWidget(fslider, 0, 1)
        self.setLayout(layout)
        self.resize(200,200)
        self.move(0, 0)
        self.show()


try:
    # stylesheet
    import qdarkstyle
except Exception as error:
    print('failed ' + str(error))

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    try:
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        pass
    except Exception as error:
        print('failed ' + str(error))
    window = MainWindow()
    sys.exit(app.exec_())
