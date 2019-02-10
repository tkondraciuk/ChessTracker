import cv2
import numpy as np
from Classifier import Classifier
from math import floor
from FieldSeparator import FieldSeparator
from ChessboardField import FIELD_BLACK_PIECE, FIELD_WHITE_PIECE
import keyboard
import sys
from Logger import Logger, MESSTYPE_ERROR, MESSTYPE_INFO


class ThresholdCalibrator:
    whiteNumber = 16
    blackNumber = 16
    count=1

    def __init__(self, fieldSeparator):
        self.fieldSeparator = fieldSeparator
        self.fields = np.array(fieldSeparator.fields).ravel()
        self.minThreshold = 0
        self.maxThreshold = 255
        self.classifier = Classifier()
        self.logger=Logger()
        for f in self.fields:
            f.classifier = self.classifier

    def Start(self):
        self.logger.log('Classifier Threshold Searching started', MESSTYPE_INFO)
        self.waitForFiguresPlacement()
        minThresholdFound = False
        maxThresholdFound = False
        thresholdsFound = False

        while not thresholdsFound and self.minThreshold <= self.maxThreshold:
            if not minThresholdFound:
                minThresholdFound = self.testThreshold(self.minThreshold)
            if not maxThresholdFound:
                maxThresholdFound = self.testThreshold(self.maxThreshold)

            if not minThresholdFound:
                self.minThreshold += 1
            if not maxThresholdFound:
                self.maxThreshold -= 1
            thresholdsFound = maxThresholdFound and minThresholdFound
            print('Min: '+str(self.minThreshold))
            print('Max: '+str(self.maxThreshold))
            print()

        if self.minThreshold <= self.maxThreshold:
            classifierThreshold = (self.minThreshold + self.maxThreshold) / 2
            classifierThreshold = round(classifierThreshold)
            self.classifier.setThreshold(classifierThreshold)
            self.logger.log('Threshold found: '+str(classifierThreshold), MESSTYPE_INFO)
        else:
            self.logger.log('Can\'t find threshold', MESSTYPE_ERROR)
            raise Exception('Nie można znaleźć odpowiedniego progu')

    def testThreshold(self, thres):
        self.classifier.setThreshold(thres)
        self.fieldSeparator.updateChessboardFields()
        self.logger.saveUnlabeledFields(self.fields, 'Threshold '+str(thres))
        states = list(map(lambda x: x.state, self.fields))
        self.count+=1
        return states.count(FIELD_WHITE_PIECE) == self.whiteNumber and states.count(FIELD_BLACK_PIECE) == self.blackNumber

    def waitForFiguresPlacement(self):
        print('Umieść figury na pozycjach startowych i wciśnij Spację')
        while True:
            if keyboard.is_pressed('Space'):
                break
            if keyboard.is_pressed('Esc'):
                sys.exit()

