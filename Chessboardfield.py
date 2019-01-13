import numpy as np
import cv2

class ChessboardField:

    marker_min=np.array([43,54,27], dtype=np.uint8)
    marker_max=np.array([75,167,131], dtype=np.uint8)

    whitePiece_min=[]
    whitePiece_max=[]

    blackPiece_min=np.array([0,0,0], dtype=np.uint8)
    blackPiece_max=np.array([2,239,255], dtype=np.uint8)

    def __init__(self, label, image):
        self.marker=self.findMarkers(image)
        self.image=image
        self.label=label

    def hasChanged(self):
        quantile=np.quantile(self.image,0.5)
        return quantile>=128

    def findMarkers(self,image):
        hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
        mask=cv2.inRange(hsv,self.marker_min, self.marker_max)
        return mask

    def findBlackPiece(self,image):
        hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
        mask=cv2.inRange(hsv,self.blackPiece_min, self.blackPiece_max)

    
    