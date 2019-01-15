import numpy as np
import cv2
import Calibration
import FieldSeparator as FS
import time
import CameraHandler
import keyboard as key

ch=CameraHandler.CameraHandler(2)
I=ch.GetFrame()
image=I 
calib=Calibration.StartCalibration(ch)
calib=Calibration.setChessboardVerticles(calib)
fieldSeparator=FS.FieldSeparator(calib)
fieldSeparator.createChessboardFields()
i=0

while True:
    if key.is_pressed('Escape'):
        break
    if key.is_pressed('Space'):
        i=0 
        fieldSeparator.updateChessboardFields()
        for row in fieldSeparator.fields:
            for field in row:
                field.checkFieldState()
                factor=None
                if field.state==0:
                    factor=128
                elif field.state==1:
                    factor=225
                elif field.state==2:
                    factor=0
                else:
                    raise Exception('Błąd w określaniu stanu pola')
                cv2.imwrite('Pola/{}.jpg'.format(i),np.ones((30,30) ,dtype=np.uint8)*factor)
                i+=1
        


# fieldSeparator.updateChessboardFields() 
# for row in fieldSeparator.fields:
#         for f in row: 
#               f.checkFieldState()
#             color=[]
#             if f.state==0:
#                 color=np.ones((30,30),dtype=np.uint8) * 128
#             elif f.state==1:
#                 color=np.ones((30,30),dtype=np.uint8)*256
#             elif f.state==2:
#                 color=np.zeros((30,30),dtype=np.uint8)
#             else: 
#                 raise Exception('Coś jest nie tak')
#             cv2.imwrite('Pola/{}.jpg'.format(i),color) 
#             i+=1
# cv2.imread