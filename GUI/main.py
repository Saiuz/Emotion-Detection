import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QMainWindow, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QWidget, QToolTip,
    QPushButton, QApplication)
from PyQt5.QtGui import QFont
from titlechange import titlechange
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

    def StartStopVideo(self):
        if self.videoRunning is None:
            self.videoRunning = True
            self.vidth = VideoThread(self)
            self.vidth.changePixmap.connect(self.setImage)
            self.vidth.label("images")
        elif self.videoRunning:
            pass

            #self.vidth.stop()
            #self.vidth.wait()
            #self.videoRunning = False
        #else:
         #   self.vidth.resume()

    def CreateMenu(self):
        self.mainMenu = self.menuBar()
        self.fileMenu = self.mainMenu.addMenu('File')
        
    def CreateVideo(self):
        self.vidbtn = QPushButton('Video', self)
        self.vidbtn.move(0, 20)
        self.vidbtn.setToolTip('Starts video. Can\'t stop won\'t stop')

        self.vidbtn.clicked.connect(self.StartStopVideo)
        self.vidbtn.resize(self.vidbtn.sizeHint())
        self.setWindowTitle('EmotionLabeler')
        self.title = "Icon"
        self.setWindowIcon(QIcon('icon.png'))

        self.label = QLabel(self)
        self.label.move(0, 60)
        self.label.resize(960, 540)

    def initUI(self):
        self.resize(900, 600)
        qtRectangle = self.frameGeometry()
        self.CreateMenu()
        centerpoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerpoint)
        QToolTip.setFont(QFont('SansSerif', 10))

        self.CreateVideo()
        
        self.show()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EmotionLabeler()
    sys.exit(app.exec_())