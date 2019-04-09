import numpy as np
import cv2
import ChessboardField as CF

class Classifier:
    def __init__(self, field=None, threshold=127):
        self.threshold=threshold
        self.field=field

    def setThreshold(self,threshold):
        self.threshold=threshold
        
    def getFieldState(self, field):
        if field.isEmpty():
            return CF.FIELD_EMPTY

        pieceMask=cv2.bitwise_xor(field.emptyFieldMarker, field.markerMask)
        pieceColorSample=cv2.cvtColor(field.image, cv2.COLOR_BGR2GRAY)
        pieceColorSample=cv2.merge([pieceColorSample, pieceMask])

        nonZeroSample=self.removeTransparentPixels(pieceColorSample)
        if np.median(nonZeroSample)>self.threshold:
            return CF.FIELD_WHITE_PIECE
        else:
            return CF.FIELD_BLACK_PIECE

    def removeTransparentPixels(self, image):
        l=[]
        for row in image:
            for f in row:
                if f[1]!=0:
                    l.append(f[0])
        return l

