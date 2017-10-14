
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
from PyQt5.QtWidgets import * 
import sys

class MyQDial(QDial):
  
  def __init__(self):
    QDial.__init__(self)
#-----------------------------------

  def paintEvent(self,event):
    QDial.paintEvent(self,event)
    painter = QPainter(self)
       
    rect = self.geometry()
    x = rect.width()/3
    y = rect.height()/2
    painter.setPen(QPen(Qt.red))
    painter.drawText(QPoint(x,y),"My Custom QDial!")
#-----------------------------------

def main():  
    app     = QApplication(sys.argv)
    dia = QDial()
    dia.show()
    dial = MyQDial()    
    dial.setWindowTitle("Custom QDial Colored Text")
    dial.resize(300,300)
    dial.show()    
    return app.exec_()    
#-----------------------------------    

if __name__ == '__main__':
  main()
    