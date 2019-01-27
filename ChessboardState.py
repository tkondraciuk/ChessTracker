import cv2
import numpy as np
from ChessboardField import ChessboardField
from Piece import *
from CommonMessenger import CommonMessenger

class ChessboardState:
    def __init__(self, fieldSeparator):
        self.fieldSeparator=fieldSeparator
        self.fields=self.getFieldsDict(fieldSeparator.fields)
        self.lastFields=dict()
        self.placePieces()
        self.messenger=CommonMessenger()
    
    def getFieldsDict(self, fields):
        fieldsDict=dict()
        numpyFields=np.array(fields)
        for field in numpyFields.ravel():
            fieldsDict[field.label]=field
        return fieldsDict

    def placePieces(self):
        fields=self.fields

        fields['A1'].initCurrentPiece(COLOR_WHITE, FIGURE_ROOK)
        fields['H1'].initCurrentPiece(COLOR_WHITE, FIGURE_ROOK)
        fields['B1'].initCurrentPiece(COLOR_WHITE, FIGURE_KNIGHT)
        fields['G1'].initCurrentPiece(COLOR_WHITE, FIGURE_KNIGHT)
        fields['C1'].initCurrentPiece(COLOR_WHITE, FIGURE_BISHOP)
        fields['F1'].initCurrentPiece(COLOR_WHITE, FIGURE_BISHOP)
        fields['D1'].initCurrentPiece(COLOR_WHITE, FIGURE_QUEEN)
        fields['E1'].initCurrentPiece(COLOR_WHITE, FIGURE_KING)

        fields['A8'].initCurrentPiece(COLOR_BLACK, FIGURE_ROOK)
        fields['H8'].initCurrentPiece(COLOR_BLACK, FIGURE_ROOK)
        fields['B8'].initCurrentPiece(COLOR_BLACK, FIGURE_KNIGHT)
        fields['G8'].initCurrentPiece(COLOR_BLACK, FIGURE_KNIGHT)
        fields['C8'].initCurrentPiece(COLOR_BLACK, FIGURE_BISHOP)
        fields['F8'].initCurrentPiece(COLOR_BLACK, FIGURE_BISHOP)
        fields['D8'].initCurrentPiece(COLOR_BLACK, FIGURE_QUEEN)
        fields['E8'].initCurrentPiece(COLOR_BLACK, FIGURE_KING)

        # Uzupełnij drugi rząd białymi pionami
        whiteKeys=filter(lambda k: '2' in k, fields.keys())
        for key in whiteKeys:
            fields[key].initCurrentPiece(COLOR_WHITE, FIGURE_PAWN)

        # Uzupełnij siódmy rząd czarnymi pionami
        blackKeys=filter(lambda k: '7' in k, fields.keys())
        for key in blackKeys:
            fields[key].initCurrentPiece(COLOR_BLACK, FIGURE_PAWN)

    def Update(self):
        self.fieldSeparator.updateChessboardFields()
        changes=list(filter(lambda f: f.hasChanged(), self.fields.values()))
        if len(changes)==0:
            return ''
        else:
            return self.getMove(changes)

    def getMove(self,changes):
        message=''
        if len(changes)==4:
            message=self.getCastling(changes)
        elif len(changes)==2:
            startField, targetField=self.getStartAndTargetFields(changes)
            ret, message=self.messenger.getMessage(startField, targetField)
            if ret:
                targetField.setCurrentPiece(startField.currentPiece)
                startField.releaseField()
        else:
            raise Exception('Wystąpił błąd przy odczytaniu ruchu')

        return message


    def getStartAndTargetFields(self,changes):
        #Pola z których zniknęła figura
        startFields=list(filter(lambda f: f.state==0 and not f.currentPiece.empty, changes))

        #Pozostałe pola
        targetFields=list(filter(lambda f: not f in startFields, changes))

        if len(startFields)==1 and len(targetFields)==1:
            return startFields[0], targetFields[0]
        else:
            return startFields, targetFields

        
        
        
