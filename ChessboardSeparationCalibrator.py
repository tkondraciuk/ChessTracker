import cv2
import numpy as np
import sys
import KeyboardList as key

class ChessboardSeparationCalibrator:

    windowName='Calibration - Mark chessboard'
    selectedMarkerRadius=5
    selectedMarkerColor=(255,0,0)

    def __init__(self,cameraHandler):
        self.cameraHandler=cameraHandler
        image=cameraHandler.GetFrame()
        self.selectedMarkerRadius=self.getMarkerRadius(image,0.01)


    def Start(self):
        return self.AskUserForVerticles()

    
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
        
        chessboardVericles=[]
        cv2.namedWindow(self.windowName)
        cv2.setMouseCallback(self.windowName,getVerticle)
        while True:
            image=self.cameraHandler.GetFrame()
            image=markVerticles(self,image)
            cv2.imshow(self.windowName, image)

            if cv2.waitKey(1) & 0xff == key.Space:
                if len(chessboardVericles)<4:
                    print('Zaznacz wierzcholki szachownicy, a następnie wcisnij Spacje')
                else:
                    break

            if cv2.waitKey(1) & 0xff==key.Esc:
                sys.exit()
        cv2.destroyAllWindows()
        return chessboardVericles

    def getMarkerRadius(self, image, factor):
        size=np.mean(image.shape,dtype=np.uint32)
        return int(size * factor)