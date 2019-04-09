from InvalidMoveException import InvalidMoveException

class ThresholdUnfoundException(Exception):
    def Solve(self,calib):
        ime=InvalidMoveException()
        ime.Solve(calib)
