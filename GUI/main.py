import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QMainWindow, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QWidget, QToolTip,
    QPushButton, QApplication)
from PyQt5.QtGui import QFont

from video import VideoThread


class EmotionLabeler(QMainWindow):

    def __init__(self):
        super().__init__()
        self.videoRunning = None
        self.initUI()

    def changetitle(self):
        titlechange(self)

    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))



    def CreateMenu(self):
        self.mainMenu = self.menuBar()
        self.fileMenu = self.mainMenu.addMenu('File')
        


    def initUI(self):
        self.resize(900, 600)
        qtRectangle = self.frameGeometry()
        self.CreateMenu()
        centerpoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerpoint)
        QToolTip.setFont(QFont('SansSerif', 10))


        
        self.show()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EmotionLabeler()
    sys.exit(app.exec_())