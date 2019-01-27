import cv2
import numpy as np
import KeyboardList as key
import ChessboardField as CF
import keyboard
import sys

DIRECTION_NORTH=0
DIRECTION_EAST=1
DIRECTION_SOUTH=2
DIRECTION_WEST=3

class FieldsLabelerCalibrator:

    NUMBER_NORMAL=['1','2','3','4','5','6','7','8']
    NUMBER_REVERSAL=['8','7','6','5','4','3','2','1']
    LETTER_NORMAL=['A','B','C','D','E','F','G','H']
    LETTER_REVERSAL=['H','G','F','E','D','C','B','A']

    

    def __init__(self, fieldSeparator):
        self.fields=[] 
        self.fieldSeparator=fieldSeparator

    def Start(self):
        self.waitForPiecesPlacement()
        orient=self.getOrientation()

        if orient==DIRECTION_NORTH:
            self.labelFields(self.LETTER_REVERSAL,self.NUMBER_NORMAL)
        elif orient==DIRECTION_SOUTH:
            self.labelFields(self.LETTER_NORMAL, self.NUMBER_REVERSAL)
        elif orient==DIRECTION_EAST:
            self.labelFields(self.NUMBER_REVERSAL, self.LETTER_REVERSAL)
        elif orient==DIRECTION_WEST:
            self.labelFields(self.NUMBER_NORMAL, self.LETTER_NORMAL)


    def waitForPiecesPlacement(self):
        print('Umiesc figury na planszy i wcisnij Spacje')
        while True:
            if keyboard.is_pressed('Space'):
                break
            if keyboard.is_pressed(key.Esc):
                sys.exit()

        self.fieldSeparator.updateChessboardFields()
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
            raise Exception('Nastąpił błąd w rozpoznaniu kolorów figur!')

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
