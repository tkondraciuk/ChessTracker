import cv2
import numpy as np
import sys
import KeyboardList as key
from Logger import Logger, MESSTYPE_ERROR, MESSTYPE_INFO
from MessageBoxes import *

class ChessboardSeparationCalibrator:

    windowName='Calibration - Mark chessboard'
    selectedMarkerRadius=5
    selectedMarkerColor=(255,0,0)

    def __init__(self,cameraHandler):
        self.cameraHandler=cameraHandler
        image=cameraHandler.GetFrame()
        self.selectedMarkerRadius=self.getMarkerRadius(image,0.01)
        self.logger=Logger()


    def Start(self):
        self.logger.log('Chessboard Separation Calibration started', MESSTYPE_INFO)
        result = self.AskUserForVerticles()
        self.logger.log('Chesboard vertices got: '+', '.join([str(x) for x in result]), MESSTYPE_INFO)
        return result

    
    def AskUserForVerticles(self):

        def inCircle(point, center, radius):
            return (point[0]-center[0])**2+(point[1]-center[1])**2<=radius

        def markVerticles(self, image):
            radius=self.selectedMarkerRadius
            color=self.selectedMarkerColor
            for p in chessboardVericles:
                cv2.circle(image,p,radius,color,-1)
            return image

        def getVerticle(event,x,y,flags,params):
            if event==cv2.EVENT_LBUTTONDOWN:
                clickPoint=(x,y)
                radius=self.selectedMarkerRadius
                nearbyVerticles=list(filter(lambda c: inCircle(clickPoint,c,radius),chessboardVericles))
                if len(nearbyVerticles)>0:
                    pointToRemove=nearbyVerticles[0]
                    chessboardVericles.remove(pointToRemove)
                elif len(chessboardVericles)<4:
                    chessboardVericles.append(clickPoint)
        
        infoBox('Zaznacz wierzchołki szachownicy, a następnie wciśnij Spację.')
        chessboardVericles=[]
        cv2.namedWindow(self.windowName)
        cv2.setMouseCallback(self.windowName,getVerticle)
        while True:
            image=self.cameraHandler.GetFrame()
            image=markVerticles(self,image)
            cv2.imshow(self.windowName, image)

            if cv2.waitKey(1) & 0xff == key.Space:
                vCount=len(chessboardVericles)
                if vCount < 4:
                    errorBox('Zaznaczono {} z 4 wierzchołków. Zaznacz wszystkie wierzchołki, a następnie wciśnij Spację.'.format(vCount))
                else:
                    break

            if cv2.waitKey(1) & 0xff==key.Esc:
                self.logger.log('User canceled calibration', MESSTYPE_INFO)
                sys.exit()
        cv2.destroyAllWindows()
        return chessboardVericles

    def getMarkerRadius(self, image, factor):
        size=np.mean(image.shape,dtype=np.uint32)
        return int(size * factor)