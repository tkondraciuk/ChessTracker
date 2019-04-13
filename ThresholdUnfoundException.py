#from InvalidMoveException import InvalidMoveException

class ThresholdUnfoundException(Exception):
    def Solve(self,calib):
        from InvalidMoveException import InvalidMoveException
        ime=InvalidMoveException()
        ime.Solve(calib)
