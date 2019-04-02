import cv2
import numpy as np

class SharedData:
    def __init__(self):
        self.hasPhoto = False
        self.frame = None
        self.FaceImg = None
        self.NoFaceImg = cv2.imread("data/noface.png")
        self.greyscaletoggle = None
        self.facedims = None
        self.label = None

    def __str__(self):
        arrayargs = [self.hasPhoto, self.frame, self.FaceImg, self.NoFaceImg]
        for i in range(len(arrayargs)):
            if type(arrayargs[i]) is np.ndarray:
                arrayargs[i] = arrayargs[i].shape

        datastr = "hasPhoto={}\nphotoshape={}\nfaceimgshape={}\nnofaceimgshape={}".format(*arrayargs)
        return datastr

    def set_photo(self, photo):
        #print("photo set: " + str(photo.shape))
        self.hasPhoto = True
        self.frame = photo

    def get_frame(self):
        return self.frame

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