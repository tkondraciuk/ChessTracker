import numpy as np
import cv2
import Calibration
import FieldSeparator as FS
import time
import CameraHandler
import keyboard as key
from tkinter import *
import device as dev
from InvalidMoveException import InvalidMoveException
from InvalidCastlingException import InvalidCastlingException
from MessageBoxes import *

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

    
cameraId = getCameraId()

infoBox('Usuń wszystkie figury z planszy, a następnie wciśnij Spację')
# while True:
#     if key.is_pressed('Space'):
#         break

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
        try:
            message=chessboardState.Update()
            print(message)
            print("Wykonaj następny ruch i wcisnij spacje.")
        except InvalidMoveException as e:
            errorBox('Wykonany ruch został błędnie odczytany. Za chwilę zostanie ponownie przeprowadzona procedura inicjalizacji. Upewnij się, że oświetlenie na szachownicy jest w miarę równomierne, po czym zamknij to okno. ')
            e.Solve(calib)
        except InvalidCastlingException as e:
            answer=yesnoDialog('Czy wykonany przed chwilą ruch był roszadą?')
            if answer=='no':
                errorBox('Prawdopodobnie nastąpiło błędne odczytanie ruchu. Za chwilę zostanie ponownie przeprowadzona procedura inicjalizacji. Upewnij się, że oświetlenie na szachownicy jest w miarę równomierne, po czym zamknij to okno. ')
                e.Solve(calib)
            else:
                errorBox('Wykonany przed chwilą ruch jest nieprawidłowy. Cofnij swój ruch i spróbuj wykonać go jeszcze raz. Jeśli problem się powtórzy należy w odpowiedzi do poprzedniego okna wybrać \'Nie\'.')

            
        
        
        
           