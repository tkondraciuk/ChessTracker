import numpy as np
import cv2
import Calibration
import FieldSeparator as FS
import time
import CameraHandler

def getMask(image):
        hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
        cmin=np.array([43,54,27])
        cmax=np.array([75,167,131])
        return cv2.inRange(image,cmin, cmax)

ch=CameraHandler.CameraHandler(1)
I=ch.GetFrame()
image=I
calib=Calibration.StartCalibration(ch)
calib=Calibration.setChessboardVerticles(calib)
fieldSeparator=FS.FieldSeparator(calib)
fieldSeparator.getFieldsImage()
i=0
for f in fieldSeparator.fields:
        #mask=getMask(f.image)
        cv2.imwrite('Pola/{}.jpg'.format(i),f.image)
        i+=1
