import numpy as np
import cv2
import sys
import math
import ChessboardField
import FieldSeparator as FS
from ChessboardSeparationCalibrator import *
from MarkerExtractionCalibrator import *
from FieldSeparator import FieldSeparator
from FieldsLabelerCalibrator import FieldsLabelerCalibrator
from ChessboardState import ChessboardState
from ThresholdCalibrator import ThresholdCalibrator
from Logger import Logger
from InvalidPieceColorRecognitionException import InvalidPieceColorRecognitionException
from ThresholdUnfoundException import ThresholdUnfoundException
from MessageBoxes import *

class Calibration:
    verticles=[]
    cameraHandler=[]
    def __init__(self, cameraHandler):
        self.cameraHandler=cameraHandler
        self.findChessboardCalibrator=ChessboardSeparationCalibrator(cameraHandler)
        self.extractMarkersCalibrator=MarkerExtractionCalibrator(cameraHandler)
        self.logger=Logger()


    def getFieldPoints(self):
        def getSubPoints(self,start,stop):
            xs=np.linspace(start[0],stop[0],9,dtype=np.int32)
            ys=np.linspace(start[1],stop[1],9,dtype=np.int32)
            return list(zip(xs,ys))
        firstPoint=min(self.verticles,key=lambda x: x[0]*x[1])
        horSecondPoint=min(self.verticles,key=lambda x: x[1]/x[0])
        verSecondPoint=min(self.verticles,key=lambda x: x[0]/x[1])
        dimSecondPoint=min(self.verticles,key=lambda x: 1/(x[0]*x[1]))

        self.verticles=[]
        for p in zip(getSubPoints(self,firstPoint,verSecondPoint),getSubPoints(self,horSecondPoint,dimSecondPoint)):
            row=[q  for q in getSubPoints(self,p[0],p[1])]
            self.verticles.append(row)


    def StartCalibration(self):
        self.verticles=self.findChessboardCalibrator.Start()
        self.getFieldPoints()
        self.cmin, self.cmax = self.extractMarkersCalibrator.Start()
        self.FieldSeparator=FieldSeparator(self)
        self.FieldSeparator.createChessboardFields()
        self.FieldSeparator.Log('EmptyFields')
        self.thresholdCalibrator=ThresholdCalibrator(self.FieldSeparator)
        try:
            self.thresholdCalibrator.Start()
        except ThresholdUnfoundException as e:
            errorBox('Nie znaleziono prawidłowego progu rozróżniającego kolory figur. Spróbuj dopasować warunki oświetleniowe, tak aby oświetlenie na szachownicy było w miarę równomierne, a następnie kliknij OK, aby powtórzyć inicjalizację programu.')
            e.Solve(self)
            
        self.fieldLabererCalibrator=FieldsLabelerCalibrator(self.FieldSeparator)
        try:
            self.fieldLabererCalibrator.Start()
        except InvalidPieceColorRecognitionException as e:
            errorBox('Wystąpił błąd w rozpoznawaniu koloru figur. Prawdopodobnie został on spowodowany niewłaściwymi warunkami oświetleniowymi. Spróbuj zadbać o to aby oświetlenie na szachownicy było w miarę równomierne, a następnie wciśnij OK, aby powtórzyć inicjalizację programu.')
            e.Solve(self)
        self.chessboardState=ChessboardState(self.FieldSeparator)

    def GetFieldSeparator(self):
        return FS.FieldSeparator(self)

    def getColorRange(self):
        return self.cmin, self.cmax

    def getChessboardStateInstance(self):
        return self.chessboardState

