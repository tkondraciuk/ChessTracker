import cv2
import numpy as np
import KeyboardList as Key
import sys

class MarkerExtractionCalibrator:

    windowName='Calibration - Extract Markers'
    hueMinLabel='Min hue: '
    hueMaxLabel='Max hue: '
    saturationMinLabel='Min saturation: '
    saturationMaxLabel='Max saturation: '
    valueMinLabel='Min value: '
    valueMaxLabel='Max value: '

    def __init__(self, cameraHandler):
        self.cameraHandler=cameraHandler
        self.cmin=None
        self.cmax=None

    def Start(self):
        self.AskUserForExtractionCriteria()
        return self.cmin, self.cmax

    def AskUserForExtractionCriteria(self):
        def getValuesFromTrackbars():
            hmin=cv2.getTrackbarPos(self.hueMinLabel,self.windowName)
            hmax=cv2.getTrackbarPos(self.hueMaxLabel,self.windowName)
            smin=cv2.getTrackbarPos(self.saturationMinLabel,self.windowName)
            smax=cv2.getTrackbarPos(self.saturationMaxLabel,self.windowName)
            vmin=cv2.getTrackbarPos(self.valueMinLabel,self.windowName)
            vmax=cv2.getTrackbarPos(self.valueMaxLabel,self.windowName)

            cmin=np.array([hmin, smin, vmin], dtype=np.uint8)
            cmax=np.array([hmax, smax, vmax], dtype=np.uint8)

            return cmin, cmax

        def getFinalImage(image, cmin, cmax):
            hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
            mask=cv2.inRange(hsv,cmin,cmax)
            result=cv2.bitwise_and(image,image,mask=mask)
            return result

        def doNothing(x):
            pass

        cv2.namedWindow(self.windowName)
        cv2.createTrackbar(self.hueMinLabel,self.windowName,0,127,doNothing)
        cv2.createTrackbar(self.hueMaxLabel,self.windowName,127,127,doNothing)
        cv2.createTrackbar(self.saturationMinLabel,self.windowName,0,255,doNothing)
        cv2.createTrackbar(self.saturationMaxLabel,self.windowName,255,255,doNothing)
        cv2.createTrackbar(self.valueMinLabel,self.windowName,0,255,doNothing)
        cv2.createTrackbar(self.valueMaxLabel,self.windowName,255,255,doNothing)

        while True:
            frame=self.cameraHandler.GetFrame()
            cmin, cmax=getValuesFromTrackbars()
            frame=getFinalImage(frame,cmin,cmax)
            cv2.imshow(self.windowName,frame)

            if cv2.waitKey(1) & 0xff==Key.Space:
                self.cmin=cmin
                self.cmax=cmax
                break

            if cv2.waitKey(1) & 0xff==Key.Esc:
                sys.exit()
        
        cv2.destroyAllWindows()


