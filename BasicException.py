from MarkerExtractionCalibrator import MarkerExtractionCalibrator
from ThresholdCalibrator import ThresholdCalibrator

class BasicException(Exception):
    def repeatInitialization(self, calib):
        mec=MarkerExtractionCalibrator(calib.cameraHandler)
        mec.cmin=calib.cmin
        mec.cmax=calib.cmax
        calib.cmin, calib.cmax=mec.Start()

        tc=ThresholdCalibrator(calib.fieldSeparator)
        tc.Start()
