import numpy as np
import cv2
import Calibration
import FieldSeparator as FS
import time
import CameraHandler
import keyboard as key

print('Usun wszystkie figury z planszy i wcisnij Spacje')
while True:
    if key.is_pressed('Space'):
        break

ch=CameraHandler.CameraHandler(2) 
calib=Calibration.Calibration(ch)
calib.StartCalibration()
fieldSeparator=calib.GetFieldSeparator()
chessboardState=calib.getChessboardStateInstance()
i=0

print('Umiesc figury na planszy i wcisnij Spacje')
while True:
    if key.is_pressed('Escape'):
        break
    if key.is_pressed('Space'):
        i=0 
        chessboardState.Update()
        for field in chessboardState.fields.values():
            factor=None
            if field.state==0:
                factor=128
            elif field.state==1:
                factor=225
            elif field.state==2:
                factor=0
            else:
                raise Exception('Blad w okreslaniu stanu pola')
                
            cv2.imwrite('Pola/{}.jpg'.format(field.getName()),np.ones((30,30) ,dtype=np.uint8)*factor)

        print("Stan gry zaktualizowano. Wykonaj ruch i wcisnij spacje.")
           