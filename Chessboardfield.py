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

    # Markery na dzien
    # marker_min=np.array([38,33,0], dtype=np.uint8)
    # marker_max=np.array([83,255,255], dtype=np.uint8)

    # Markery na noc
    marker_min=np.array([31,33,0], dtype=np.uint8)
    marker_max=np.array([83,255,255], dtype=np.uint8)


    def __init__(self, label, image):
        self.updateImage(image, checkState=False)
        self.emptyFieldMarker=self.marker
        self.label=label
        self.state=FIELD_STATE_UNKNOWN


    def findMarkers(self,image):
        hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
        mask=cv2.inRange(hsv,self.marker_min, self.marker_max)
        return mask

    def checkFieldState(self):
        def getNonZeroValues(a):
            l=[]
            for row in a:
                for f in row:
                    if f!=0:
                        l.append(f)
            return l
        if self.isEmpty():
            self.state=FIELD_EMPTY
            return
        pieceMask=cv2.bitwise_xor(self.markerMask,self.emptyFieldMarker)
        pieceColorSample=cv2.bitwise_and(self.image,self.image,mask=pieceMask)
        pieceColorSample=cv2.cvtColor(pieceColorSample, cv2.COLOR_BGR2GRAY)

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

    
    