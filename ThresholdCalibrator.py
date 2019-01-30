import cv2
import numpy as np
from Classifier import Classifier
from math import floor
from FieldSeparator import FieldSeparator
from ChessboardField import FIELD_BLACK_PIECE, FIELD_WHITE_PIECE


class ThresholdCalibrator:
    whiteNumber = 5
    blackNumber = 5

    def __init__(self, fieldSeparator):
        self.fieldSeparator = fieldSeparator
        self.fields = np.array(fieldSeparator.fields).ravel()
        self.minThreshold = 0
        self.maxThreshold = 255
        self.classifier = Classifier()
        for f in self.fields:
            f.classifier = self.classifier

    def Start(self):
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

        if self.minThreshold <= self.maxThreshold:
            classifierThreshold = (self.minThreshold + self.maxThreshold) / 2
            classifierThreshold = round(classifierThreshold)
            self.classifier.setThreshold(classifierThreshold)
        else:
            raise Exception('Nie można znaleźć odpowiedniego progu')

    def testThreshold(self, thres):
        self.classifier.setThreshold(thres)
        self.fieldSeparator.updateChessboardFields()
        states = list(map(lambda x: x.state, self.fields))
        return states.count(FIELD_WHITE_PIECE) == self.whiteNumber and states.count(FIELD_BLACK_PIECE) == self.blackNumber
