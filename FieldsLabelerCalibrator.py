import cv2
import numpy as np
import KeyboardList as key
import ChessboardField as CF
import keyboard
import sys
from Logger import Logger, MESSTYPE_ERROR, MESSTYPE_INFO
from InvalidPieceColorRecognitionException import InvalidPieceColorRecognitionException
import os
from MessageBoxes import *

DIRECTION_NORTH=0
DIRECTION_EAST=1
DIRECTION_SOUTH=2
DIRECTION_WEST=3

class FieldsLabelerCalibrator:

    NUMBER_NORMAL=['1','2','3','4','5','6','7','8']
    NUMBER_REVERSAL=['8','7','6','5','4','3','2','1']
    LETTER_NORMAL=['A','B','C','D','E','F','G','H']
    LETTER_REVERSAL=['H','G','F','E','D','C','B','A']

    

    def __init__(self, calib):
        self.calib=calib
        self.fields=calib.FieldSeparator.fields 
        self.fieldSeparator=calib.FieldSeparator
        self.logger=Logger()

    def Start(self):
        self.logger.log('Field Objects Labeling started', MESSTYPE_INFO)

        try:
            orient=self.getOrientation()
        except InvalidPieceColorRecognitionException as e:
            errorBox('Wystąpił błąd w rozpoznawaniu koloru figur. Prawdopodobnie został on spowodowany niewłaściwymi warunkami oświetleniowymi. Spróbuj zadbać o to aby oświetlenie na szachownicy było w miarę równomierne, a następnie wciśnij OK, aby powtórzyć inicjalizację programu.')
            e.Solve(self.calib)
            return

        orientString=''
        self.logger.log('Chessboard orientation found: '+orientString, MESSTYPE_INFO)

        if orient==DIRECTION_NORTH:
            self.labelFields(self.LETTER_REVERSAL,self.NUMBER_NORMAL)
            orientString='NORTH'
        elif orient==DIRECTION_SOUTH:
            self.labelFields(self.LETTER_NORMAL, self.NUMBER_REVERSAL)
            orientString='SOUTH'
        elif orient==DIRECTION_EAST:
            self.labelFields(self.NUMBER_REVERSAL, self.LETTER_REVERSAL)
            orientString='EAST'
        elif orient==DIRECTION_WEST:
            self.labelFields(self.NUMBER_NORMAL, self.LETTER_NORMAL)
            orientString='WEST'

        self.logger.log('Labeling successfully finished!', MESSTYPE_INFO)
        


    def waitForPiecesPlacement(self):
        print('Umiesc figury na planszy i wcisnij Spacje')
        while True:
            if keyboard.is_pressed('Space'):
                break
            if keyboard.is_pressed(key.Esc):
                self.logger.log('User canceled calibration', MESSTYPE_INFO)
                sys.exit()

        self.fieldSeparator.updateChessboardFields()
        self.fieldSeparator.Log('PiecesStartPlacement')
        self.fields=self.fieldSeparator.fields

    def getOrientation(self):
        fields=self.fields
        if self.isWhiteSide(fields[:1][:]) and self.isBlackSide(fields[6:][:]):
            return DIRECTION_NORTH
        elif self.isWhiteSide(fields[6:][:]) and self.isBlackSide(fields[:1][:]):
            return DIRECTION_SOUTH
        elif self.isWhiteSide([x[6:] for x in fields]) and self.isBlackSide([x[:1] for x in fields]):
            return DIRECTION_EAST
        elif self.isWhiteSide([x[:1] for x in fields]) and self.isBlackSide([x[6:] for x in fields]):
            return DIRECTION_WEST
        else:
            self.logger.log('Can\'t recognize a pieces colors! ', MESSTYPE_ERROR)
            raise InvalidPieceColorRecognitionException('Nastąpił błąd w rozpoznaniu kolorów figur!')

    def isBlackSide(self,side):
        side=np.array(side)
        return np.all([x.state==CF.FIELD_BLACK_PIECE for x in side.ravel()])

    def isWhiteSide(self,side):
        side=np.array(side)
        return np.all([x.state==CF.FIELD_WHITE_PIECE for x in side.ravel()])

    def labelFields(self, columnNames, rowNames):
        for i in range(8):
            for j in range(8):
                label = columnNames[j] + rowNames[i]
                field=self.fields[i][j]
                field.setLabel(label)

