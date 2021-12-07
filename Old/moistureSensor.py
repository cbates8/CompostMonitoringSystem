import time
from readSensors import ReadSensor

class MoistureSensor(ReadSensor):

    def __init__(self, pinNum):
        super().__init__(pinNum)

    # Calibrate the set moisture sensors.
    def calibrate(self):
        sCalibrateVals = []
        print("Calibrating...")
        for i in range(25):
            sCalibrateVals.insert(i, self.getVal())
            print("\tAdding Val: ", sCalibrateVals[i])
            time.sleep(1)
        
        self.airVal = max(sCalibrateVals)
        self.waterVal = min(sCalibrateVals)

        print("Max Value: ", self.airVal)
        print("Min Value: ", self.waterVal)
        print("\nDone calibrating")

    # Maps the raw input accordingly
    def mapSensorVals(self):
        val = self.getVal()
        val = (val - self.waterVal)/(self.airVal - self.waterVal)
        val *= 100
        val = 100 - val
        return val