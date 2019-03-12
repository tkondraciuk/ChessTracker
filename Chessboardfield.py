import numpy as np
import cv2
from Piece import *
from Classifier import Classifier

FIELD_STATE_UNKNOWN=-1
FIELD_EMPTY=0

FIELD_WHITE_PIECE= COLOR_WHITE
FIELD_BLACK_PIECE= COLOR_BLACK

NAMES={
    COLOR_WHITE: 'Bialy',
    COLOR_BLACK: 'Czarny',
    FIGURE_ROOK: 'Wieza',
    FIGURE_KNIGHT: 'Skoczek',
    FIGURE_BISHOP: 'Goniec',
    FIGURE_QUEEN: 'Krolowa',
    FIGURE_KING: 'Krol',
    FIGURE_PAWN: 'Pion'
}

def imopen(image, kernelSize):
    kernel=np.ones(kernelSize,np.uint8)
    return cv2.morphologyEx(image,cv2.MORPH_OPEN,kernel)

class ChessboardField:

    marker_min=np.array([31,33,0], dtype=np.uint8)
    marker_max=np.array([83,255,255], dtype=np.uint8)
    strel=(5,5)


    def __init__(self, label, image, colorRange):
        self.updateImage(image, checkState=False)
        self.emptyFieldMarker=self.marker
        self.label=label
        self.state=FIELD_STATE_UNKNOWN
        self.marker_min=colorRange[0]
        self.marker_max=colorRange[1]
        self.currentPiece=buildEmptyPiece()
        self.classifier=Classifier(threshold=45)

    def setClassifierThreshold(self, threshold):
        self.classifier.setThreshold(threshold)

    def findMarkers(self,image):
        hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
        mask=cv2.inRange(hsv,self.marker_min, self.marker_max)
        return mask

    def isEmpty(self):
        return np.any(self.marker)

    def updateImage(self, image, checkState=True):
        self.image=image
        self.markerMask=self.findMarkers(image)
        self.marker=imopen(self.markerMask,self.strel)
        if checkState:
            self.state=self.classifier.getFieldState(self)

    def setLabel(self,label):
        if label[0].isdigit() and label[1].isalpha():
            self.label=label[1]+label[0]
        elif label[0].isalpha and label[1].isdigit():
            self.label=label
        else:
            raise Exception('Błąd w etykietowaniu pól')

    def initCurrentPiece(self, color, figure):
        if not self.currentPiece.empty:
            return
        self.currentPiece=Piece(color,figure)

    def setCurrentPiece(self, piece):
        self.currentPiece=piece

    def releaseField(self):
        self.currentPiece=buildEmptyPiece()

    def getName(self):
        if self.currentPiece.empty:
            return 'EMPTY ({})'.format(self.label)
        color=NAMES[self.currentPiece.color]
        figure=NAMES[self.currentPiece.figure]
        field=self.label
        return '{} {}({})'.format(color, figure, field)

    def hasChanged(self):
        if self.state == FIELD_EMPTY and self.currentPiece.empty:
            return False
        elif self.state == self.currentPiece.color:
            return False
        else:
            return True

    
    