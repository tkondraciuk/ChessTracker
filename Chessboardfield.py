import numpy as np
import cv2

class ChessboardField:


    def __init__(self, label, image):
        self.image=image
        self.label=label

    def hasChanged(self):
        quantile=np.quantile(self.image,0.5)
        return quantile>=128
    