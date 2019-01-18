import cv2
import numpy as np
import Calibration
import ChessboardField
import ChessboardField as CF
from math import *



class FieldSeparator:
    fields=[]

    def __init__(self,calibration):
        self.fieldVerticles=calibration.verticles
        self.cameraHandler=calibration.cameraHandler
        self.image=self.cameraHandler.GetFrame()
        self.calibration=calibration

    
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
    def updateChessboardFields(self):
        self.image=self.cameraHandler.GetFrame()
        for i in range(8):
            for j in range(8):
                p1=self.fieldVerticles[i][j]
                p2=self.fieldVerticles[i+1][j+1]
                fieldImage=self.cutImage(p1,p2)
                self.fields[i][j].updateImage(fieldImage,False) # Usunąć false


