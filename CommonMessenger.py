


class CommonMessenger:
    def __init__(self):
        pass

    def getMessage(self, start, target, castling=False):
        if castling:
            return self.getCastlingMessage()

        if target.currentPiece.empty:
            return True, self.getMoveMessage(start, target)
        elif target.currentPiece.color!=start.currentPiece.color:
            return True, self.getCaptureMessage(start, target)
        else:
            return False, 'Wykryto próbę bicia własnej figury'

    def getMoveMessage(self, start, target):
        pieceName=start.getName()
        destination=target.label
        return 'Ruch {} na {}'.format(pieceName,destination)

    def getCaptureMessage(self, start, target):
        pieceName=start.getName()
        capturedPieceName=target.getName()
        return '{} bije {}'.format(pieceName, capturedPieceName)

    def getCastlingMessage(self):
        return True, 'Roszada'
