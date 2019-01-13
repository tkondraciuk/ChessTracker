import cv2
import numpy as np

class CameraHandler:

    lastFrame=[]
    lastFrameCapured=False
    def __init__(self,CameraID):
        self.cap=cv2.VideoCapture(CameraID)
    
    def GetFrame(self):
        if not self.lastFrameCapured:
            ret, self.lastFrame=self.cap.read()
        
        while True:
            ret, frame=self.cap.read()
            if not ret:
                raise Exception('Błąd kamery: klatka jest pusta!')
            sub=np.subtract(frame, self.lastFrame)
            self.lastFrame=frame
            if np.any(sub):
                return frame