import busio
import time
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

# Super class for reading sensors.
class ReadSensor(object):

    # Constructor for the readSensor class.
    def __init__(self, pinNum=MCP.P0):
        cs = digitalio.DigitalInOut(board.D5)                                   # Assigns the MCP3008 cs pin to D5 on RPI.
        spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)      # Assigns rest of the pins on MCP3008.
        self.mcp = MCP.MCP3008(spi, cs)                                         # Creates an instance of the MCP class with configurations.
        self.pinNum = pinNum
        self.channel = AnalogIn(self.mcp, self.pinNum)                               # Assigns the channel to pinNum.

        # Sets max and min val for mapping.
        self.maxVal = 0
        self.minVal = 0                                                      

    # Used to calibrate the sensors.
    def calibrate(self):
        pass
    
    # Used to configure the sensors.
    def mapSensorVals(self, x, in_min, in_max, out_min, out_max):
        pass

    # Returns the raw analog to digital converted mcp value.
    def getVal(self):
        return self.channel.value