# CompostMonitoringSystem
The circuit diagram and software for a vermi-compost monitoring system.
The system was built for our partners at the University of California Cooperative Extension (UCCE) to extend
and autonomize composting to the San Jose community.

# Material List:
  - Raspberry Pi 4
  - micro sd
  - USB type-c power cable
  - wires
  - Temperature sensor (x3)
  - Moisture sensor (x3)
  - MCP3008 chip
  - Blues Wireless Notecard
  - Pi Hat with an M.2 slot for the Notecard

# Instructions:
  - Connect the pi according to the circuit diagram.
  - Pull the github repository onto the raspberry pi.
  - To manually start the software.
    - Enter terminal
    - Run main.py
    - Ensure mositure sensors are calibrated correctly
  - To have the software run on boot.
    - Configure nano to run python script

# Main.py:
  This file is responsible for data collection and storage. By default, the file is configured to
  three moisture sensors, three temperature sensors. The data is saved locally using pickleshare
  and sent to the cloud using Notehub. Editting any of these factors should be done in this file.
  
# moistureSensor.py
  This class is responsible for configuring the moisture sensor. The class extends ReadSensor and ensures the propper calibration of the sensors,
  as well as the correct mapping of values.
 
# TemperatureSensor.py
  This file is responsible for reading the temperature values from the DS18B20 temperature sensors, which accomodate to 1-wire-protocol. In order to
  calibrate this to your own temperature sensors, replace the ids in the sensorids array, located in the init.

# readSensors.py
  This file can be extended to most sensors that provide an analog output. The class is responsible for initializing the MCP3008 analog to digital converter,
  and provides two abstract functions for calibrating the sensors and mapping the values.

# sensorCalibration.py
  This file is responsible for correctly calibrating the moisture sensors. This script provides step-by-step instructions to the user to ensure accurate calibration of the sensors. Calibration results will be stored in `calibrationValues.csv` to be used to correctly map moisture sensor readings to a moisture percentage.
  
# Necessary Libraries:
  - pickleshare
  - adafruit_mcp3xxx.mcp3008
  - multiprocessing
  - smbus
  - urllib3
