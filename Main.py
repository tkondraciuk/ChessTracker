import numpy as np
import cv2
import Calibration
import FieldSeparator as FS
import time
import CameraHandler

ch=CameraHandler.CameraHandler(2)
I=ch.GetFrame()
image=I
calib=Calibration.StartCalibration(ch)
calib=Calibration.setChessboardVerticles(calib)
fieldSeparator=FS.FieldSeparator(calib)
fieldSeparator.getFieldsImage()
i=0
for f in fieldSeparator.fields:
        #mask=getMask(f.image)
        cv2.imwrite('Pola/{}.jpg'.format(i),f.marker)
        i+=1
