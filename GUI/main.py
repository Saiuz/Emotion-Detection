import sys

from PyQt5.QtWidgets import (QApplication, QDesktopWidget,
                             QMainWindow, QLabel, QToolTip, QPushButton)
from PyQt5.QtGui import QPixmap, QImage, QFont
from video import VideoThread, SharedData
from facedetection import FaceDetectionThread
import cv2
import numpy as np
import os
import signal

PID = os.getpid()


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

        faceth = FaceDetectionThread(self.photoData)


        self.faceImg = QLabel(self)
        self.faceImg.move(650, 40)
        self.faceImg.resize(200, 200)
        facebt = QPushButton("get image", self)
        facebt.move(700, 500)
        facebt.clicked.connect(faceth.getFaceImg)

        vidth = VideoThread(self.photoData)
        vidth.changePixmap.connect(self.setImage)
        vidth.start()

        self.show()






if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EmotionLabeler()
    signal.signal(signal.SIGTERM, app.exec_())
    os.kill(PID, signal.SIGTERM)
    sys.exit()