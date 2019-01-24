FIGURE_ROOK='R'
FIGURE_KNIGHT='Kn'
FIGURE_BISHOP='B'
FIGURE_KING='K'
FIGURE_QUEEN='Q'
FIGURE_PAWN='P'

COLOR_WHITE= 1
COLOR_BLACK= 2

def buildEmptyPiece():
    return Piece(None,None,True)

class Piece:
    def __init__(self,color,figure,empty=False):
        self.color=color
        self.figure=figure
        self.empty=empty



    

