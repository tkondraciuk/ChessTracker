import numpy as np
import cv2

FIELD_STATE_UNKNOWN=-1
FIELD_EMPTY=0
FIELD_WHITE_PIECE=1
FIELD_BLACK_PIECE=2

def imopen(image, kernelSize):
    kernel=np.ones(kernelSize,np.uint8)
    return cv2.morphologyEx(image,cv2.MORPH_OPEN,kernel)

class ChessboardField:

    marker_min=np.array([31,33,0], dtype=np.uint8)
    marker_max=np.array([83,255,255], dtype=np.uint8)


    def __init__(self, label, image, colorRange):
        self.updateImage(image, checkState=False)
        self.emptyFieldMarker=self.marker
        self.label=label
        self.state=FIELD_STATE_UNKNOWN
        self.marker_min=colorRange[0]
        self.marker_max=colorRange[1]


    def findMarkers(self,image):
        hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
        mask=cv2.inRange(hsv,self.marker_min, self.marker_max)
        return mask

    def checkFieldState(self):
        def getNonZeroValues(a):
            l=[]
            for row in a:
                for f in row:
                    if f[1]!=0:
                        l.append(f[0])
            return l
        if self.isEmpty():
            self.state=FIELD_EMPTY
            return
        pieceMask=cv2.bitwise_xor(self.markerMask,self.emptyFieldMarker)
        pieceColorSample=cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        pieceColorSample=cv2.merge([pieceColorSample,pieceMask])  #cv2.bitwise_and(self.image,self.image,mask=pieceMask)

        if np.median(getNonZeroValues(pieceColorSample))>45:
            self.state=FIELD_WHITE_PIECE
        else:
            self.state=FIELD_BLACK_PIECE

    def isEmpty(self):
        return np.any(self.marker)

    def updateImage(self, image, checkState=True):
        self.image=image
        self.markerMask=self.findMarkers(image)
        self.marker=imopen(self.markerMask,(6,6))
        if checkState:
            self.checkFieldState()

    def setLabel(self,label):
        if label[0].isdigit() and label[1].isalpha():
            self.label=label[1]+label[0]
        elif label[0].isalpha and label[1].isdigit():
            self.label=label
        else:
            raise Exception('Błąd w etykietowaniu pól')

    
    