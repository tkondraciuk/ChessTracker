import cv2
import numpy as np
from threading import Timer
import KeyboardList as key
import keyboard
import sys

class CameraHandler:

    lastFrame=[]
    lastFrameCapured=False
    def __init__(self,CameraID):
        self.cap=cv2.VideoCapture(CameraID)
    
    def GetFrame(self):
        def sendCameraError():
            print('Kamera nie odpowiada. Upewnij się, że wszysko działa poprawnie i uruchom program jeszcze raz. Wciśnij Esc aby kontynuować')


        timer=Timer(5,sendCameraError)
        if not self.lastFrameCapured:
            ret, self.lastFrame=self.cap.read()
        
        timer.start()
        while True:
            ret, frame=self.cap.read()
            if ret:
                sub=np.subtract(frame, self.lastFrame)
                self.lastFrame=frame
                if np.any(sub):
                    timer.cancel()
                    return frame