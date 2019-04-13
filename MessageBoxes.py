from tkinter import Tk, messagebox as msb

def infoBox(message):
    root=Tk()
    root.withdraw()
    msb.showinfo('ChessTracker', message)

def errorBox(message):
    root=Tk()
    root.withdraw()
    msb.showerror('ChessTracker', message)

def yesnoDialog(message):
    root=Tk()
    root.withdraw()
    answer=msb.askyesno('ChessTracker',message)
    return answer