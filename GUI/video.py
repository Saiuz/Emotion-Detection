from PyQt5.QtCore import QThread, Qt, pyqtSignal
import cv2
from PyQt5.QtGui import QImage
import numpy as np

class SharedData:
    def __init__(self):
        self.hasphoto = False
        self.photo = None
        self.FaceImg = None
        self.NoFaceImg = cv2.imread("data/NoFace.png")
        self.greyscaletoggle = None

    def __str__(self):
        arrayargs = [self.hasphoto,self.photo,self.FaceImg,self.NoFaceImg]
        for i in range(len(arrayargs)):
            if type(arrayargs[i]) is np.ndarray:
                arrayargs[i] = arrayargs[i].shape

        datastr = "hasphoto={}\nphotoshape={}\nfaceimgshape={}\nnofaceimgshape={}".format(*arrayargs)
        return datastr

    def set_photo(self, photo):
        #print("photo set: " + str(photo.shape))
        self.hasphoto = True
        self.photo = photo

    def get_photo(self):
        return self.photo

    def get_face_image(self):
        if self.FaceImg is not None:
            return True, np.copy(self.FaceImg)
        else:
            return False, self.NoFaceImg

    def set_face_image(self,img):
        self.FaceImg = img

    def set_graytoggle_state(self,state):
        self.greyscaletoggle = state

    def get_graytoggle_state(self):
        return self.greyscaletoggle

class VideoThread(QThread):
    changePixmap = pyqtSignal(QImage)

    def __init__(self, PhotoData, parent=None, camera=0):
        QThread.__init__(self, parent=parent)
        self.isRunning = True
        self.PhotoData = PhotoData
        self.cap = None
        if self.cap is not None:
            self.cap.release()
        self.cap = cv2.VideoCapture(camera)

    def run(self):

        while self.isRunning:
            ret, frame = self.cap.read()
            if ret:
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.PhotoData.set_photo(rgb_image)
                p = QImage(rgb_image.data, rgb_image.shape[1], rgb_image.shape[0], QImage.Format_RGB888)
                #p = convert_to_qt_format.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

    def __del__(self):
        self.cap.release()


    def display(self, img, faces, numImages, lastlabel, saving):
        disp_img = np.copy(img)
        if len(faces) == 1:
            x, y, w, h = faces[0]
            savestr = ""
            if saving:
                savestr = "SAVED"
            cv2.rectangle(disp_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(disp_img, lastlabel + "  {}".format(str(numImages)) + savestr,
                        (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 255, 0))

        return disp_img

