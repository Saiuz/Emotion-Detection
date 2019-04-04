import cv2
import numpy as np
import csv
import os
from collections import Counter


class SaveData:
    def __init__(self, PhotoData, labelconfig="data/labelList.csv", labellist="data/faceLabels.csv"):
        self.labels = None
        self.currentLabel = None
        self.imageDir = "data/Images"
        self.labelcsv = []
        self.imageIndex = 0
        self.PhotoData = PhotoData


        with open(labelconfig) as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            for row in reader:
                self.labelcsv.append(row)

        if os.path.isfile(labellist):
            with open(labellist, 'r') as file:
                l = np.array(list(csv.reader(file)))
                if l.shape[0] > 0:
                    self.labelCount = Counter(l[:, 1])
                    self.imageIndex = int(l[-1, 0][4:-4]) + 1
                else:
                    self.labelCount = {}
            self.csvFile = open(labellist, 'a')
        else:
            self.csvFile = open(labellist, 'w')
            self.labelCount = {}

        self.csvFileWriter = csv.writer(self.csvFile, delimiter=',',
                                   quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')

        print(self.labelCount, self.imageIndex)

        def save_current(self):
            photo = self.PhotoData.FaceImg





class SharedData:
    def __init__(self):
        self.hasPhoto = False
        self.frame = None
        self.FaceImg = None
        self.NoFaceImg = cv2.imread("data/noface.png")
        self.greyscaletoggle = None
        self.facedims = None
        self.hasFaceImg = False


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
        if self.hasFaceImg:
            return self.hasFaceImg, np.copy(self.FaceImg)
        else:
            return self.hasFaceImg, self.NoFaceImg

    def set_face_image(self,ret_val, img):
        self.hasFaceImg = ret_val
        self.FaceImg = img

    def set_graytoggle_state(self,state):
        self.greyscaletoggle = state

    def get_graytoggle_state(self):
        return self.greyscaletoggle