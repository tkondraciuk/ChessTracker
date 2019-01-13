import numpy as np
import cv2

class ChessboardField:

    cutCorrector1=()
    cutCorrector2=()

    def __init__(self, label, image):
        def cutImage(p1,p2):
            return self.image[p1[1]:p2[1] , p1[0]:p2[0]]
        def setCutCorrectors():
            imSize=self.image.shape
            factor1=0.05
            factor2=1-factor1
            ytransform=0.0
            self.cutCorrector1=(int(factor1*imSize[0]),int(factor1*imSize[1]+ytransform*imSize[1]))
            self.cutCorrector2=(int(factor2*imSize[0]),int(factor2*imSize[1]-ytransform*imSize[1]))
        #self.image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        self.image=image
        self.label=label
        setCutCorrectors()
        self.image=cutImage(self.cutCorrector1,self.cutCorrector2)

    def hasChanged(self):
        quantile=np.quantile(self.image,0.5)
        return quantile>=128
    