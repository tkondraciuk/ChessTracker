import numpy as np
import cv2
import Calibration
import FieldSeparator as FS
import time
import CameraHandler
import keyboard as key
from tkinter import *
import device as dev

root=Tk()    
def onButtonClick():
        root.destroy()

def getCameraId(): 
    cameras=dev.getDeviceList()
    
    label=Label(root, text='Wybierz kamere:')
    label.pack()

    currentChoice=StringVar(root, cameras[0])
    DDmenu=OptionMenu(root, currentChoice, *cameras)
    DDmenu.pack()

    button=Button(root, text='Dalej', command=onButtonClick) 
    button.pack()

    mainloop()
    
    chosenCameraName=currentChoice.get()
    return cameras.index(chosenCameraName)



    


def readCameraId():
    f=open('./cameraId.txt','r')
    fileString=f.read()
    result=fileString.strip()
    if result.isdigit():
        return int(result)
    else:
        return 0
    
cameraId= getCameraId() #readCameraId()

print('Usun wszystkie figury z planszy i wcisnij Spacje')
while True:
    if key.is_pressed('Space'):
        break

ch=CameraHandler.CameraHandler(cameraId) 
calib=Calibration.Calibration(ch)
calib.StartCalibration()
fieldSeparator=calib.GetFieldSeparator()
chessboardState=calib.getChessboardStateInstance()
i=0

print('Umiesc figury na planszy i wcisnij Spacje')
while True:
    if key.is_pressed('Escape'):
        break
    if key.is_pressed('Space'):
        i=0 
        message=chessboardState.Update()
        print(message)
        
        print("Wykonaj następny ruch i wcisnij spacje.")
           