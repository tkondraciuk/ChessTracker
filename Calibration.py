import numpy as np
import cv2
import sys
import math
import ChessboardField
import numpy.linalg as linalg

def StartCalibration(cameraHandler):
    calib=Calibration(cameraHandler)
    cv2.namedWindow('Calibration',cv2.WINDOW_NORMAL|cv2.WINDOW_FREERATIO)
    return calib



def setChessboardVerticles(calib):
    def get_verticle(event,x,y,flags,params):
        if event==cv2.EVENT_LBUTTONDOWN:
            point=(x,y)
            calib.verticles.append(point)
            rad=math.floor(len(imageCopy)*0.005)
            cv2.circle(imageCopy,point,rad,(255,0,0),-1)

    EscASCII=27
    imageCopy=calib.cameraHandler.lastFrame.copy()
    cv2.setMouseCallback('Calibration',get_verticle)
    while len(calib.verticles)<4:
        cv2.imshow('Calibration',imageCopy)
        if cv2.waitKey(1) & 0xff==EscASCII:
            break
    
    if len(calib.verticles)<4:
        sys.exit()

    cv2.destroyAllWindows()
    calib.getFieldPoints()
    return calib




        


class Calibration:
    verticles=[]
    cameraHandler=[]
    def __init__(self, cameraHandler):
        self.cameraHandler=cameraHandler
    
   
    def getFieldPoints(self):
        def getSubPoints(self,start,stop):
            xs=np.linspace(start[0],stop[0],9,dtype=np.int32)
            ys=np.linspace(start[1],stop[1],9,dtype=np.int32)
            return list(zip(xs,ys))
        firstPoint=min(self.verticles,key=lambda x: x[0]*x[1])
        horSecondPoint=min(self.verticles,key=lambda x: x[1]/x[0])
        verSecondPoint=min(self.verticles,key=lambda x: x[0]/x[1])
        dimSecondPoint=min(self.verticles,key=lambda x: 1/(x[0]*x[1]))

        self.verticles=[]
        for p in zip(getSubPoints(self,firstPoint,verSecondPoint),getSubPoints(self,horSecondPoint,dimSecondPoint)):
            row=[q  for q in getSubPoints(self,p[0],p[1])]
            self.verticles.append(row)
