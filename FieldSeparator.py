import cv2
import numpy as np
import Calibration
import ChessboardField
import ChessboardField as CF
from math import *

def getMask(image):
        hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
        cmin=np.array([43,54,27])
        cmax=np.array([75,167,131])
        return cv2.inRange(image,cmin, cmax)

class FieldSeparator:
    fields=[]

    def __init__(self,calibration):
        self.fieldVerticles=calibration.verticles
        self.image=calibration.cameraHandler.GetFrame()
        self.image=getMask(self.image)

    def getFieldsImage(self):
        def cutImage(self,image,p1,p2):
            return image[p1[1]:p2[1],p1[0]:p2[0]]
        self.fields=[]
        
        for i in range(8):
            for j in range(8):
                p1=self.fieldVerticles[i][j]
                p2=self.fieldVerticles[i+1][j+1]
                fieldImage=cutImage(self,self.image,p1,p2)
                field=CF.ChessboardField('',fieldImage)
                self.fields.append(field)

