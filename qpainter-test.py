
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
from PyQt5.QtWidgets import * 
import sys

def MainWindow():  
    pixmap = QPixmap (QSize(400, 400))    
    painter = QPainter (pixmap)    
    gradient = QLinearGradient(QPointF(pixmap.rect().topLeft()), QPointF(pixmap.rect().bottomLeft()))    

    gradient.setColorAt(0, Qt.blue)
    gradient.setColorAt(0.4, Qt.cyan)
    gradient.setColorAt(1, Qt.green)    

    brush = QBrush(gradient)        
    painter.fillRect( QRectF(0, 0, 400, 400), brush)
    painter.drawText( QRectF(0, 0, 400, 400), Qt.AlignCenter,  "This is an image created with QPainter and QPixmap")

    pixmap.save("/Users/reno/Desktop/output.jpg")    
    painter.end() 


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
    