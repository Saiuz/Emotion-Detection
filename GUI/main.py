import sys
from PyQt5.QtCore import QThread, Qt, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QWidget, QDesktopWidget,
                             QMainWindow, QLabel, QHBoxLayout, QToolTip, QPushButton)
from PyQt5.QtGui import QIcon, QPixmap, QImage, QFont
from video import VideoThread, SharedData
import cv2
import numpy as np


class EmotionLabeler(QMainWindow):

    def __init__(self):
        super().__init__()
        self.haar_cascade = cv2.CascadeClassifier(
            'data/haarcascade_frontalface_alt.xml')
        self.videoRunning = None
        self.photoData = SharedData()
        self.initUI()

    def setImage(self, image):
        self.videoFeed.setPixmap(QPixmap.fromImage(image))

    def setFaceImg(self):
        if self.photoData.hasphoto:
            img = self.photoData.get_photo()

            img = cv2.flip(img, 1)
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            faces = self.haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
            faceimg = None
            if len(faces) == 1:
                x, y, w, h = faces[0]
                faceimg = gray[y:y + h, x:x + w]
                img = img[y:y + h, x:x + w]
                img = cv2.resize(img, (200,200))
                img = np.copy(img)
            convert_to_qt_format = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)
            p = convert_to_qt_format #convert_to_qt_format.scaled(640, 480, Qt.KeepAspectRatio)
            self.__setFaceImg__(p)

    def __setFaceImg__(self, image):
        self.faceImg.setPixmap(QPixmap.fromImage(image))

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

        self.videoFeed = QLabel(self)
        self.videoFeed.move(0, 40)
        self.videoFeed.resize(640, 480)



        self.faceImg = QLabel(self)
        self.faceImg.move(650, 40)
        self.faceImg.resize(200, 200)
        facebt = QPushButton("get image", self)
        facebt.move(700, 500)
        facebt.clicked.connect(self.setFaceImg)

        #hbox = QHBoxLayout()
        #hbox.addStretch(1)
        #hbox.addWidget(facebt)



        th = VideoThread(self.photoData)
        th.changePixmap.connect(self.setImage)
        th.start()

        self.show()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EmotionLabeler()
    sys.exit(app.exec_())