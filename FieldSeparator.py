import cv2
import numpy as np
import Calibration
import ChessboardField
import ChessboardField as CF
from math import *
from Logger import Logger



class FieldSeparator:
    fields=[]

    def __init__(self,calibration):
        self.fieldVerticles=calibration.verticles
        self.cameraHandler=calibration.cameraHandler
        self.image=self.cameraHandler.GetFrame()
        self.calibration=calibration
        self.logger=Logger()

    
    def cutImage(self,p1,p2):
        return self.image[p1[1]:p2[1],p1[0]:p2[0]]

        
    def createChessboardFields(self):
        colorRange=self.calibration.getColorRange()
        for i in range(8):
            row=[]
            for j in range(8):
                p1=self.fieldVerticles[i][j]
                p2=self.fieldVerticles[i+1][j+1]
                fieldImage=self.cutImage(p1, p2)
                field=CF.ChessboardField('', fieldImage, colorRange)
                row.append(field)
            self.fields.append(row)

            
    def updateChessboardFields(self, newFrame=True):
        if newFrame:
            self.image=self.cameraHandler.GetFrame()
        else:
            self.image=self.cameraHandler.lastFrame
        for i in range(8):
            for j in range(8):
                p1=self.fieldVerticles[i][j]
                p2=self.fieldVerticles[i+1][j+1]
                fieldImage=self.cutImage(p1,p2)
                self.fields[i][j].updateImage(fieldImage) 

    def Log(self, name=None):
        frame=self.cameraHandler.lastFrame
        self.logger.saveRawFrame(frame, name)
        hsv=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask=cv2.inRange(hsv, self.calibration.cmin, self.calibration.cmax)
        mask=CF.imopen(mask, CF.ChessboardField.strel)
        
        self.logger.saveMarkerMask(mask, name)


