import cv2
import numpy as np
import KeyboardList as Key
import sys
from Logger import Logger, MESSTYPE_ERROR, MESSTYPE_INFO


class MarkerExtractionCalibrator:

    windowName = 'Calibration - Extract Markers'
    trackbarsName = 'Trackbars'
    hueMinLabel = 'Min hue: '
    hueMaxLabel = 'Max hue: '
    saturationMinLabel = 'Min saturation: '
    saturationMaxLabel = 'Max saturation: '
    valueMinLabel = 'Min value: '
    valueMaxLabel = 'Max value: '

    def __init__(self, cameraHandler):
        self.cameraHandler = cameraHandler
        self.cmin = None
        self.cmax = None
        self.logger = Logger()

    def Start(self):
        self.logger.log('Marker Extration Calibration started.', MESSTYPE_INFO)
        self.AskUserForExtractionCriteria()
        self.logger.log('Marker lower limit found: '+str(self.cmin), MESSTYPE_INFO)
        self.logger.log('Marker higher limit found: '+str(self.cmax), MESSTYPE_INFO)
        return self.cmin, self.cmax

    def AskUserForExtractionCriteria(self):
        def getValuesFromTrackbars():
            hmin = cv2.getTrackbarPos(self.hueMinLabel, self.trackbarsName)
            hmax = cv2.getTrackbarPos(self.hueMaxLabel, self.trackbarsName)
            smin = cv2.getTrackbarPos(
                self.saturationMinLabel, self.trackbarsName)
            smax = cv2.getTrackbarPos(
                self.saturationMaxLabel, self.trackbarsName)
            vmin = cv2.getTrackbarPos(self.valueMinLabel, self.trackbarsName)
            vmax = cv2.getTrackbarPos(self.valueMaxLabel, self.trackbarsName)

            cmin = np.array([hmin, smin, vmin], dtype=np.uint8)
            cmax = np.array([hmax, smax, vmax], dtype=np.uint8)

            return cmin, cmax

        def getFinalImage(image, cmin, cmax):
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, cmin, cmax)
            result = cv2.bitwise_and(image, image, mask=mask)
            return result

        def doNothing(x):
            pass

        cv2.namedWindow(self.windowName)
        cv2.namedWindow(self.trackbarsName)
        cv2.createTrackbar(
            self.hueMinLabel, self.trackbarsName, 0, 127, doNothing)
        cv2.createTrackbar(
            self.hueMaxLabel, self.trackbarsName, 127, 127, doNothing)
        cv2.createTrackbar(self.saturationMinLabel,
                           self.trackbarsName, 0, 255, doNothing)
        cv2.createTrackbar(self.saturationMaxLabel,
                           self.trackbarsName, 255, 255, doNothing)
        cv2.createTrackbar(self.valueMinLabel,
                           self.trackbarsName, 0, 255, doNothing)
        cv2.createTrackbar(self.valueMaxLabel,
                           self.trackbarsName, 255, 255, doNothing)

        while True:
            frame = self.cameraHandler.GetFrame()
            cmin, cmax = getValuesFromTrackbars()
            frame = getFinalImage(frame, cmin, cmax)
            cv2.imshow(self.windowName, frame)

            if cv2.waitKey(1) & 0xff == Key.Space:
                self.cmin = cmin
                self.cmax = cmax
                break

            if cv2.waitKey(1) & 0xff == Key.Esc:
                self.logger.log('User canceled calibration', MESSTYPE_INFO)
                sys.exit()

        cv2.destroyAllWindows()
