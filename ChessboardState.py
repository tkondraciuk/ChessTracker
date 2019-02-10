import cv2
import numpy as np
from ChessboardField import ChessboardField, FIELD_BLACK_PIECE, FIELD_WHITE_PIECE
from Piece import *
from CommonMessenger import CommonMessenger
from Logger import Logger, MESSTYPE_ERROR, MESSTYPE_INFO

class ChessboardState:
    def __init__(self, fieldSeparator):
        self.fieldSeparator=fieldSeparator
        self.fields=self.getFieldsDict(fieldSeparator.fields)
        self.lastFields=dict()
        self.placePieces()
        self.messenger=CommonMessenger()
        self.logger=Logger()
    
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
        self.fieldSeparator.Log()
        self.logger.saveFieldStates(self.fields.values())
        changes=list(filter(lambda f: f.hasChanged(), self.fields.values()))
        if len(changes)==0:
            return ''
        else:
            return self.getMove(changes)

    def getMove(self,changes):
        message=''
        if len(changes)==4:
            self.logger.log('4 changes found. Castling detected!', MESSTYPE_INFO)
            message=self.getCastling(changes)
        elif len(changes)==2:
            self.logger.log('2 changes found.', MESSTYPE_INFO)
            startField, targetField=self.getStartAndTargetFields(changes)
            ret, message=self.messenger.getMessage(startField, targetField)
            if ret:
                targetField.setCurrentPiece(startField.currentPiece)
                startField.releaseField()
        else:
            self.logger.log(str(len(changes))+' changes found. Can\'t recognize the movement', MESSTYPE_ERROR)
            raise Exception('Wystąpił błąd przy odczytaniu ruchu')

        return message

    def getCastling(self, changes):
        succes=True
        startFields, targetFields=self.getStartAndTargetFields(changes)
        piecesColor=np.mean([f.currentPiece.color for f in startFields])
        if piecesColor==FIELD_BLACK_PIECE:
            king=[f for f in startFields if f.currentPiece.figure==FIGURE_KING and f.label=='E8']
            rook=[f for f in startFields if f.currentPiece.figure==FIGURE_ROOK and f.label in ['A8', 'H8']]
            shortCastlingPath=['F8','G8']
            longCastlingPath=['B8','C8','D8']
        elif piecesColor==FIELD_WHITE_PIECE:
            king=[f for f in startFields if f.currentPiece.figure==FIGURE_KING and f.label=='E1']
            rook=[f for f in startFields if f.currentPiece.figure==FIGURE_ROOK and f.label in ['A1', 'H1']]
            shortCastlingPath=['F1','G1']
            longCastlingPath=['B1','C1','D1']
        else:
            return False

        king=king[0]
        rook=rook[0]

        if rook.label[0]=='A':
            castlingType='long'
            kingTargetPoint='C'+king.label[1]
            rookTargetPoint='D'+rook.label[1]
        else:
            castlingType='short'
            kingTargetPoint='G'+king.label[1]
            rookTargetPoint='F'+rook.label[1]
           
            
            



    def getStartAndTargetFields(self,changes):
        #Pola z których zniknęła figura
        startFields=list(filter(lambda f: f.state==0 and not f.currentPiece.empty, changes))

        #Pozostałe pola
        targetFields=list(filter(lambda f: not f in startFields, changes))

        if len(startFields)==1 and len(targetFields)==1:
            return startFields[0], targetFields[0]
        else:
            return startFields, targetFields

        
        
        
