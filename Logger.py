import cv2
import numpy as np
import os
from datetime import datetime
from ChessboardField import FIELD_BLACK_PIECE, FIELD_WHITE_PIECE

MESSTYPE_INFO = 0
MESSTYPE_ERROR = 1

class FieldTest:
    def __init__(self, color, figure, label):
        if not (color==1 or color==2):
            color=0
        self.label=label
        self.state=color
        self.figure=figure

class Logger:
    markerCounter = 1
    rawCounter = 1
    colorsCounter=1
    points=[(85, 91), (163, 90), (237, 91), (312, 91), (384, 93), (459, 92), (534, 92), (608, 91), (88, 167), (162, 168), (238, 164), (309, 167), (385, 165), (460, 168), (533, 165), (608, 165), (87, 237), (165, 238), (240, 239), (312, 239), (384, 240), (460, 241), (533, 241), (609, 238), (89, 312), (163, 313), (239, 314), (310, 314), (387, 313), (460, 314), (534, 314), (607, 313), (88, 386), (162, 387), (240, 390), (311, 388), (387, 388), (459, 387), (533, 386), (607, 386), (89, 461), (164, 462), (239, 461), (311, 462), (389, 461), (460, 462), (534, 461), (608, 459), (87, 535), (168, 537), (238, 535), (311, 535), (385, 534), (462, 535), (533, 533), (605, 534), (88, 609), (165, 606), (236, 604), (312, 607), (384, 610), (460, 612), (533, 615), (604, 611)]
    startSessiontime=None


    def __init__(self):
        if Logger.startSessiontime==None:
            Logger.startSessiontime = datetime.now()
        if not 'debug' in os.listdir():
            os.mkdir('debug')
        if not 'markerMasks' in os.listdir('debug'):
            os.mkdir('debug/markerMasks')
        if not 'logs' in os.listdir('debug'):
            os.mkdir('debug\\logs')
        if not 'raw' in os.listdir('debug'):
            os.mkdir('debug\\raw')
        if not 'colors' in os.listdir('debug'):
            os.mkdir('debug\\colors')
        pass

    def saveMarkerMask(self, mask, fileName=None):
        sessionDirName = self.fileName()
        self.markersSessionDirPath = 'debug\\markerMasks\\'+sessionDirName
        if not sessionDirName in os.listdir('debug\\markerMasks'):
            os.mkdir(self.markersSessionDirPath)

        if fileName==None:
            fileName = 'Turn '+str(Logger.markerCounter)
        path = '{}\\{}.jpg'.format(self.markersSessionDirPath, fileName)
        cv2.imwrite(path, mask)
        Logger.markerCounter += 1

    def log(self, message, type):
        hourString = datetime.now().strftime('%X')
        typeString = ''
        if type == MESSTYPE_ERROR:
            typeString = ' [ERROR]: '
        elif type == MESSTYPE_INFO:
            typeString = ' [INFO]: '

        name = self.fileName()+'.txt'
        path = 'debug\\logs\\'+name

        message = hourString+typeString+message+'\n'
        f = open(path, 'a')
        f.write(message)
        f.close()

    def saveRawFrame(self, image, fileName=None):
        sessionDirName = self.fileName()
        self.rawSessionDirPath = 'debug\\raw\\'+sessionDirName
        if not sessionDirName in os.listdir('debug\\raw'):
            os.mkdir(self.rawSessionDirPath)

        if fileName==None:
            fileName = 'Turn '+str(Logger.rawCounter)
        path = '{}\\{}.jpg'.format(self.rawSessionDirPath, fileName)
        cv2.imwrite(path, image)
        Logger.rawCounter += 1

    def saveFieldStates(self, fields, fileName=None):
        sessionDirName=self.fileName()
        colorsDirPath='debug\\colors\\'+sessionDirName
        if not sessionDirName in os.listdir('debug\\colors\\'):
            os.mkdir(colorsDirPath)
        if fileName==None:
            fileName='Turn '+str(Logger.colorsCounter)
        path='{}\\{}.jpg'.format(colorsDirPath, fileName)
        black=(0,0,0)
        white=(255, 255, 255)
        bg=cv2.imread('chessboard.jpg')
        index=0
        for i in range(1,9):
            for j in ['H','G','F','E','D','C','B','A']:
                label=j+str(i)
                field=next((f for f in fields if f.label==label), None)
                if field!=None:
                    if field.state==FIELD_BLACK_PIECE:
                        cv2.circle(bg, self.points[index], 15, black, -1)
                    elif field.state==FIELD_WHITE_PIECE:
                        cv2.circle(bg, self.points[index], 15, white, -1)
                
                index+=1
        cv2.imwrite(path, bg)
        Logger.colorsCounter+=1

    def saveUnlabeledFields(self, fields, fileName=None):
        sessionDirName=self.fileName()
        colorsDirPath='debug\\colors\\'+sessionDirName
        if not sessionDirName in os.listdir('debug\\colors\\'):
            os.mkdir(colorsDirPath)
        if fileName==None:
            fileName='Turn '+str(Logger.colorsCounter)
        path='{}\\{}.jpg'.format(colorsDirPath, fileName)
        black=(0,0,0)
        white=(255, 255, 255)
        bg=cv2.imread('chessboard.jpg')
        index=0
        for f in fields:
            if f.state==FIELD_BLACK_PIECE:
                cv2.circle(bg, self.points[index], 15, black, -1)
            elif f.state==FIELD_WHITE_PIECE:
                cv2.circle(bg, self.points[index], 15, white, -1)
            index+=1
        cv2.imwrite(path, bg)


    def fileName(self):
        d = Logger.startSessiontime
        return '{}_{}_{} {}.{}'.format(d.day, d.month, d.year, d.hour, d.minute)


# mask = np.zeros((30, 30), dtype=np.uint8)
# cv2.circle(mask, (15, 15), 10, (255, 255, 255), -1)
# f1=FieldTest(FIELD_WHITE_PIECE, 'rook', 'A4')
# f2=FieldTest(FIELD_BLACK_PIECE,'queen','G8')
# f3=FieldTest(0,'','B2')
# debug = Logger()
# debug.saveFieldStates([f1,f2,f3])
