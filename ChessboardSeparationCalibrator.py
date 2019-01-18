import cv2
import numpy as np

class ChessboardSeparationCalibrator:

    windowName='Calibration - Mark chessboard'
    selectedMarkerRadius=5
    selectedMarkerColor=(255,0,0)

    def __init__(self,cameraHandler):
        self.cameraHandler=cameraHandler
        cv2.namedWindow(self.windowName)


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
        EscASCII=27
        SpaceASCII=32
        cv2.setMouseCallback(self.windowName,getVerticle)
        while True:
            image=self.cameraHandler.GetFrame()
            image=markVerticles(self,image)
            cv2.imshow(self.windowName, image)

            if cv2.waitKey(1) & 0xff == SpaceASCII:
                if len(chessboardVericles)<4:
                    print('Zaznacz wierzcholki szachownicy, a następnie wcisnij Spacje')
                else:
                    break

            if cv2.waitKey(1) & 0xff==EscASCII:
                sys.exit()
        cv2.destroyAllWindows()
        return chessboardVericles