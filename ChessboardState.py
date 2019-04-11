import cv2
import numpy as np
from ChessboardField import ChessboardField, FIELD_BLACK_PIECE, FIELD_WHITE_PIECE
from Piece import *
from CommonMessenger import CommonMessenger
from Logger import Logger, MESSTYPE_ERROR, MESSTYPE_INFO
from InvalidMoveException import InvalidMoveException
from InvalidCastlingException import InvalidCastlingException
from MessageBoxes import *

class ChessboardState:
    def __init__(self, calib):
        self.calib=calib
        self.fieldSeparator=calib.fieldSeparator
        self.fields=self.getFieldsDict(self.fieldSeparator.fields)
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

        try:
            if len(changes)==0:
                return ''
            else:
                return self.getMove(changes)
        except InvalidMoveException as e:
            errorBox('Wykonany ruch został błędnie odczytany. Za chwilę zostanie ponownie przeprowadzona procedura inicjalizacji. Upewnij się, że oświetlenie na szachownicy jest w miarę równomierne, po czym zamknij to okno. ')
            e.Solve(self.calib)
        except InvalidCastlingException as e:
            answer=yesnoDialog('Czy wykonany przed chwilą ruch był roszadą?')
            if answer=='no':
                errorBox('Prawdopodobnie nastąpiło błędne odczytanie ruchu. Za chwilę zostanie ponownie przeprowadzona procedura inicjalizacji. Upewnij się, że oświetlenie na szachownicy jest w miarę równomierne, po czym zamknij to okno. ')
                e.Solve(self.calib)
            else:
                errorBox('Wykonany przed chwilą ruch jest nieprawidłowy. Cofnij swój ruch i spróbuj wykonać go jeszcze raz. Jeśli problem się powtórzy należy w odpowiedzi do poprzedniego okna wybrać \'Nie\'.')

    def getMove(self,changes):
        message=''
        if len(changes)==4:
            self.logger.log('4 changes found. Castling detected!', MESSTYPE_INFO)
            ret, message=self.getCastling(changes)
            if not ret:
                raise InvalidCastlingException('Wystąpił błąd przy odczytaniu ruchu')
        elif len(changes)==2:
            self.logger.log('2 changes found.', MESSTYPE_INFO)
            startField, targetField=self.getStartAndTargetFields(changes)
            ret, message=self.messenger.getMessage(startField, targetField)
            if ret:
                targetField.setCurrentPiece(startField.currentPiece)
                startField.releaseField()
        else:
            self.logger.log(str(len(changes))+' changes found. Can\'t recognize the movement', MESSTYPE_ERROR)
            raise InvalidMoveException('Wystąpił błąd przy odczytaniu ruchu')

        return message

    def getCastling(self, changes):
        startPos, targetPos=self.getStartAndTargetFields(changes)
        king=next(filter(lambda f: f.currentPiece.figure==FIGURE_KING,startPos),None)
        rook=next(filter(lambda f: f.currentPiece.figure==FIGURE_ROOK,startPos),None)
        if king==None or rook==None:
            return False, None

        kingStartPos=''
        rookStartPos=''
        rookStartPos_A=''
        rookStartPos_H=''
        kingTargetLongPos=''
        kingTargetShortPos=''
        kingTargetPos=''
        rookTargetLongPos=''
        rookTargetShortPos=''
        rookTargetPos=''
        castlingType=''
        color=''
        if king.currentPiece.color==COLOR_WHITE and rook.currentPiece.color==COLOR_WHITE:
            kingStartPos='E1'
            rookStartPos_A='A1'
            rookStartPos_H='H1'
            kingTargetLongPos='C1'
            kingTargetShortPos='G1'
            rookTargetLongPos='D1'
            rookTargetShortPos='F1'
            color='white'
        elif  king.currentPiece.color==COLOR_BLACK and rook.currentPiece.color==COLOR_BLACK:
            kingStartPos='E8'
            rookStartPos_A='A8'
            rookStartPos_H='H8'
            kingTargetLongPos='C8'
            kingTargetShortPos='G8'
            rookTargetLongPos='D8'
            rookTargetShortPos='F8'
            color='black'
        else:
            return False, None

        if rook.label==rookStartPos_A:
            castlingType='long'
            rookStartPos=rookStartPos_A
            kingTargetPos=kingTargetLongPos
            rookTargetPos=rookTargetLongPos
        elif rook.label==rookStartPos_H:
            castlingType='short'
            rookStartPos=rookStartPos_H
            kingTargetPos=kingTargetShortPos
            rookTargetPos=rookTargetShortPos
        else:
            return False, None

        if set([f.label for f in startPos])!={kingStartPos, rookStartPos} or set([f.label for f in targetPos])!={kingTargetPos, rookTargetPos}:
            return False, None

        message= self.messenger.getCastlingMessage(castlingType, color)
        self.fields[kingTargetPos].setCurrentPiece(king.currentPiece)
        self.fields[rookTargetPos].setCurrentPiece(rook.currentPiece)
        for f in [king, rook]:
            f.releaseField()

        return True, message

    def getStartAndTargetFields(self,changes):
        #Pola z których zniknęła figura
        startFields=list(filter(lambda f: f.state==0 and not f.currentPiece.empty, changes))

        #Pozostałe pola
        targetFields=list(filter(lambda f: not f in startFields, changes))

        if len(startFields)==1 and len(targetFields)==1:
            return startFields[0], targetFields[0]
        else:
            return startFields, targetFields

        
        
        
