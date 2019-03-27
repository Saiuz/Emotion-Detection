from PyQt5.QtCore import QThread, Qt, pyqtSignal
import cv2
from PyQt5.QtGui import QImage
import numpy as np

class FaceDetectionThread(QThread):
    changePixmap = pyqtSignal(QImage)

    def __init__(self, PhotoData, parent=None):
        QThread.__init__(self, parent=parent)
        self.PhotoData = PhotoData

    def biggerFace(self,faces):
        faces = np.array(faces)
        if faces.shape[0] < 2:
            return faces
        else:
            biggestFace = None
            biggestSize = 0
            for face in faces:
                size = face[2] * face[3]
                if size > biggestSize:
                    biggestFace = face
                    biggestSize = size
            return [biggestFace]

    def getFaceImg(self):
        if self.photoData.hasphoto:
            img = self.photoData.get_photo()

            img = cv2.flip(img, 1)
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            faces = self.haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
            faces = self.biggerFace(faces)
            faceimg = None

            if len(faces) == 1:
                x, y, w, h = faces[0]
                faceimg = gray[y:y + h, x:x + w]
                img = img[y:y + h, x:x + w]
                self.photoData.FaceImg = np.copy(cv2.resize(faceimg,(128,128)))
            else:
                img = self.photoData.NoFaceImg

            img = cv2.resize(img, (200, 200))
            img = np.copy(img)
            p = QImage(img.data, img.shape[1], img.shape[0],
                                          img.shape[1] * 3,QImage.Format_RGB888)

            self.changePixmap.emit(p)