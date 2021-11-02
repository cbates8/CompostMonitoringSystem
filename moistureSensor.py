import time
import numpy as np
from readSensors import ReadSensor

class MoistureSensor(ReadSensor):

    def __init__(self, pinNum):
        super().__init__(pinNum)

    # Calibrate the set moisture sensors.
    def calibrate(self):
        sCalibrateVals = []
        print(f"Calibrating Sensor {self.pinNum + 1}...")

        input("Hold the sensor in the air. Press 'Enter' to continue...")

        for i in range(10):
            sCalibrateVals.insert(i, self.getVal())
            print("\tAdding Val: ", sCalibrateVals[i])
            time.sleep(0.5)
        
        self.airVal = np.mean(sCalibrateVals)

        sCalibrateVals = []

        input("Submerge the sensor in water. Press 'Enter' to continue...")

        for i in range(10):
            sCalibrateVals.insert(i, self.getVal())
            print("\tAdding Val: ", sCalibrateVals[i])
            time.sleep(0.5)

        self.waterVal = np.mean(sCalibrateVals)

        print("Air Value: ", self.airVal)
        print("Water Value: ", self.waterVal)
        print("\nDone calibrating")

    # Maps the raw input accordingly
    # ((input - min) * 100) / (max - min) --Casey
    def mapSensorVals(self):
        val = self.getVal()
        val = (val - self.waterVal)/(self.airVal - self.waterVal)
        val *= 100 # Turn into % --Casey
        val = 100 - val # What the heck is this for??? --Casey
        return val