# CompostMonitoringSystem
The circuit diagram and software for a vermi-compost monitoring system.
The system was built for our partners at the University of California Cooperative Extension (UCCE) to extend
and autonomize composting to the San Jose community.

# Material List:
  - Raspberry pi
  - micro sd
  - type-c power cable
  - usb
  - wires
  - MCP3008 chip
  - LCD Screen

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
  This file is responsible for data storage, sensor calibration, and lcd display. By default, the file is configured to
  three moisture sensors, three temperature sensors, and the utilization of a 4x20 i2c LCD screen. The data is saved locally using pickleshare
  and copied to a removable drive using shutil. Editting any of these factors should be done in this file.
  
# moistureSensor.py
  This class is responsible for configuring the moisture sensor. The class extends ReadSensor and ensures the propper calibration of the sensors,
  as well as the correct mapping of values.
 
# TemperatureSensor.py
  This file is responsible for reading the temperature values from the DS18B20 temperature sensors, which accomodate to 1-wire-protocol. In order to
  calibrate this to your own temperature sensors, replace the ids in the sensorids array, located in the init.

# readSensors.py
  This file can be extended to most sensors that provide an analog output. The class is responsible for initializing the MCP3008 analog to digital converter,
  and provides two abstract functions for calibrating the sensors and mapping the values.
  
# Necessary Libraries:
  - pickleshare
  - adafruit_mcp3xxx.mcp3008
  - multiprocessing
  - smbus
  - urllib3
