from PyQt5.QtCore import QThread, Qt, pyqtSignal
import cv2
from PyQt5.QtGui import QImage
import os
import numpy as np
import csv
from collections import Counter

class VideoThread(QThread):
    changePixmap = pyqtSignal(QImage)

    def __init__(self, parent=None):
        QThread.__init__(self, parent=parent)
        self.isRunning = True
    def run(self):
        cap = cv2.VideoCapture(0)
        while self.isRunning:
            ret, frame = cap.read()
            if ret:
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                convert_to_qt_format = QImage(rgb_image.data, rgb_image.shape[1], rgb_image.shape[0], QImage.Format_RGB888)
                p = convert_to_qt_format.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
        cap.release()
        cv2.destroyAllWindows()

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

    def label(self,savepath, smoothCapture=False):
        haar_cascade = cv2.CascadeClassifier(
            'data/haarcascade_frontalface_alt.xml')
        csvFileWriter = None
        csvFile = None
        labels = ["Neutral", "Happy", "Sad","Angry"]


        num = 0
        if os.path.isfile(savepath + "/faceLabels.csv"):
            with  open(savepath + '/faceLabels.csv', 'r') as file:
                l = np.array(list(csv.reader(file)))
                print(l.shape)
                if l.shape[0] > 0:
                    labelCount = Counter(l[:, 1])
                    num = int(l[-1, 0][4:-4]) + 1
                else:
                    labelCount = {}

            csvFile = open(savepath + '/faceLabels.csv', 'a')

        else:
            csvFile = open(savepath + '/faceLabels.csv', 'w')
            labelCount = {}


        csvFileWriter = csv.writer(csvFile, delimiter=',',
                                   quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')

        cam = cv2.VideoCapture(smoothCapture)
        lastlabel = "Neutral"
        numImages = []
        for label in labels:
            if label in labelCount.keys():
                numImages.append(labelCount[label])
            else:
                numImages.append(0)
        lastlabelidx = 0
        saving = False

        faceimg = None
        while True:
            key = cv2.waitKeyEx(False)
            if key == ord(' ') and saving == False and faceimg is not None:
                saving = True
                numImages[lastlabelidx] += 1
                imgName = "face" + str(num) + '.png'
                cv2.imwrite(savepath + "/" + imgName, faceimg)
                csvFileWriter.writerow([imgName, lastlabel])
                num += 1
                disp_img = self.display(img, faces, numImages, lastlabel, saving)
            else:
                saving = False
                ret_val, img = cam.read()
                img = cv2.flip(img, 1)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
                faceimg = None
                if len(faces) == 1:
                    x, y, w, h = faces[0]
                    faceimg = gray[y:y + h, x:x + w]
                    if key == 2424832:
                        lastlabel = "Neutral"
                        lastlabelidx = 0
                    elif key == 2490368:
                        lastlabel = "Happy"
                        lastlabelidx = 1
                    elif key == 2621440:
                        lastlabel = "Sad"
                        lastlabelidx = 2
                    elif key == 2555904:
                        lastlabel = "Angry"
                        lastlabelidx = 3

                disp_img = self.display(img, faces, numImages, lastlabel, saving)

            cv2.imshow('my webcam', disp_img)

            if key == 27:
                break  # esc to quit
        cv2.destroyAllWindows()

    def stop(self):
        self.isRunning = False
        self.wait()

    def resume(self):
        self.isRunning = True
        self.run()