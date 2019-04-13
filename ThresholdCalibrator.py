import cv2
import numpy as np
from Classifier import Classifier
from math import floor
from FieldSeparator import FieldSeparator
from ChessboardField import FIELD_BLACK_PIECE, FIELD_WHITE_PIECE
import keyboard
import sys
from Logger import Logger, MESSTYPE_ERROR, MESSTYPE_INFO
from ThresholdUnfoundException import ThresholdUnfoundException
from MessageBoxes import *
import os


class ThresholdCalibrator:
    whiteNumber = 16
    blackNumber = 16
    count=1
    thresholdsCount=0

    def __init__(self, calib):
        self.calib=calib
        self.fieldSeparator = calib.FieldSeparator
        self.fields = np.array(self.fieldSeparator.fields).ravel()
        self.minThreshold = 0
        self.maxThreshold = 255
        self.classifier = Classifier()
        self.logger=Logger()
        for f in self.fields:
            f.classifier = self.classifier

    def Start(self):

        infoBox('Umieść figury na szachownicy, zgodnie z regułami gry w szachy, po czym wciśnij OK.')
        self.logger.log('Classifier Threshold Searching started', MESSTYPE_INFO)

        try:
            self.findThreshold()
        except ThresholdUnfoundException as e:
            errorBox('Nie znaleziono prawidłowego progu rozróżniającego kolory figur. Spróbuj dopasować warunki oświetleniowe, tak aby oświetlenie na szachownicy było w miarę równomierne, a następnie kliknij OK, aby powtórzyć inicjalizację programu.')
            e.Solve(self.calib)

    def findThreshold(self):
        minThresholdFound = False
        maxThresholdFound = False
        thresholdsFound = False
        
        self.calib.cameraHandler.GetFrame()
        while not thresholdsFound and self.minThreshold <= self.maxThreshold:
            if not minThresholdFound:
                minThresholdFound = self.testThreshold(self.minThreshold)
            if not maxThresholdFound:
                maxThresholdFound = self.testThreshold(self.maxThreshold)

            if not minThresholdFound:
                self.minThreshold += 1
                self.thresholdsCount+=1
            if not maxThresholdFound:
                self.maxThreshold -= 1
                self.thresholdsCount+=1
            thresholdsFound = maxThresholdFound and minThresholdFound
            os.system('cls')
            print('Poszukiwanie progu rozróżniającego kolory figur:')
            print('Przeszukano {} z 255'.format(self.thresholdsCount))
            # print('Min: '+str(self.minThreshold))
            # print('Max: '+str(self.maxThreshold))
            # print()

        if self.minThreshold <= self.maxThreshold:
            classifierThreshold = (self.minThreshold + self.maxThreshold) / 2
            classifierThreshold = round(classifierThreshold)
            self.classifier.setThreshold(classifierThreshold)
            self.logger.log('Threshold found: '+str(classifierThreshold), MESSTYPE_INFO)
        else:
            self.logger.log('Can\'t find threshold', MESSTYPE_ERROR)
            raise ThresholdUnfoundException('Nie można znaleźć odpowiedniego progu')

    def testThreshold(self, thres):
        self.classifier.setThreshold(thres)
        self.fieldSeparator.updateChessboardFields(newFrame=False)
        self.logger.saveUnlabeledFields(self.fields, 'Threshold '+str(thres))
        self.logger.saveRawFrame(self.calib.cameraHandler.lastFrame, 'Threshold '+str(thres))
        states = list(map(lambda x: x.state, self.fields))
        self.count+=1
        return states.count(FIELD_WHITE_PIECE) == self.whiteNumber and states.count(FIELD_BLACK_PIECE) == self.blackNumber

    def waitForFiguresPlacement(self):
        print('Umieść figury na pozycjach startowych i wciśnij Spację')
        while True:
            if keyboard.is_pressed('Space'):
                self.fieldSeparator.cameraHandler.GetFrame()
                break
            if keyboard.is_pressed('Esc'):
                sys.exit()

