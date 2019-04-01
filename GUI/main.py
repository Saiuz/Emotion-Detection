import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QDesktopWidget,
                             QMainWindow, QLabel, QToolTip, QPushButton,QCheckBox)
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

        self.videoRunning = None
        self.PhotoData = SharedData()
        self.initUI()

    def setImage(self, image):
        self.videoFeed.setPixmap(QPixmap.fromImage(image))



    def setFaceImg(self):
        img = self.PhotoData.get_face_image()
        #img = cv2.resize(img, (200, 200))
        # exists = os.path.isfile('testim.png')
        # if not exists:
        #     cv2.imwrite('testim.png', img)
        qimg = QImage(img.data, img.shape[1], img.shape[0],
                   img.shape[1], QImage.Format_Grayscale8)
        scaled = qimg.scaled(self.faceImg.size(),Qt.IgnoreAspectRatio)

        p = QPixmap.fromImage(scaled)
        self.faceImg.setPixmap(p)
        return

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


        #FACE DETECTION
        faceth = FaceDetectionThread(self.PhotoData)
        faceth.start()
        self.faceImg = QLabel(self)
        self.faceImg.move(650, 40)
        self.faceImg.resize(200, 200)

        #GET IMAGE BUTTON
        facebt = QPushButton("get image", self)
        facebt.move(700, 500)
        facebt.clicked.connect(self.setFaceImg)


        #VIDEO STREAM
        self.videoFeed = QLabel(self)
        self.videoFeed.move(0, 40)
        self.videoFeed.resize(640, 480)
        vidth = VideoThread(self.PhotoData)
        vidth.changePixmap.connect(self.setImage)
        vidth.start()

        #GREYSCALE TOGGLE
        #self.GrayScaleBox = Q



        self.show()






if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EmotionLabeler()
    signal.signal(signal.SIGTERM, app.exec_())
    os.kill(PID, signal.SIGTERM)
    sys.exit()