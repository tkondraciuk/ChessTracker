#from InvalidMoveException import InvalidMoveException

class InvalidCastlingException(Exception):
    def Solve(self, calib):
        from InvalidMoveException import InvalidMoveException
        ime=InvalidMoveException()
        ime.Solve(calib)