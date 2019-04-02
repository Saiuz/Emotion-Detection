from PyQt5.QtCore import QThread, Qt, pyqtSignal
import cv2
import numpy as np


class Saver(object):

    #changePixmap = pyqtSignal(QImage)

    def __init__(self, PhotoData):
        self.PhotoData = PhotoData


    def getFaceImg(self):
        if self.PhotoData.hasphoto:
            img = self.PhotoData.get_photo()

            img = cv2.flip(img, 1)
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            faces = self.haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
            faces = self.biggerFace(faces)

            if len(faces) == 1:
                x, y, w, h = faces[0]
                if self.PhotoData.get_graytoggle_state():
                    faceimg = gray[y:y + h, x:x + w]
                else:
                    faceimg = img[y:y + h, x:x + w]
                return np.copy(faceimg)
            else:
                return None
