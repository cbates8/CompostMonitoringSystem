# Import all the necessary libraries
from time import *
from datetime import datetime as dt
from pickleshare import *
import adafruit_mcp3xxx.mcp3008 as MCP
from multiprocessing import Process
import shutil
import os
import urllib3
import json
import matplotlib.pyplot as plt
import numpy as np

# Locally imported files.
from moistureSensor import MoistureSensor
from TemperatureSensor import TemperatureSensor

def main():
    # Declare objects.
    moisture_one = MoistureSensor(MCP.P0)
    moisture_two = MoistureSensor(MCP.P1)
    moisture_three = MoistureSensor(MCP.P3)
    temp_one = TemperatureSensor(0)
    temp_two = TemperatureSensor(1)
    temp_three = TemperatureSensor(2)
    temp1 = []
    temp2 = []
    temp3 = []
    moist1 = []
    moist2 = []
    moist3 = []
    timeS = []
    

    # Calibrates the sensors in parallel.
    p1 = Process(target=moisture_one.calibrate())
    p1.start()
    p2 = Process(target=moisture_two.calibrate())
    p2.start()
    p3 = Process(target=moisture_three.calibrate())
    p3.start()

    p1.join()
    p2.join()
    p3.join()

    # Set day 1 used to see when a new day begins
    day1 = dt.now().strftime("%d")
    # Open first data collection file with appropriate date
    dt_string = dt.now().strftime("D%dM%mY%YH%HM%MS%S")
    file = open("/home/pi/Desktop/CompostMonitoringSystem-main/compost_monitoring_code/CompostMonitoringData/" + dt_string + ".txt", "w")

    while (True):
        # Sets up the temperature variables.
        # Records values to appropriate arrays to be used for plots
        temperature_one = temp_one.read_temp()
        temp1.append(temperature_one)
        temperature_two = temp_two.read_temp()
        temp2.append(temperature_two)
        temperature_three = temp_three.read_temp()
        temp3.append(temperature_three)
        current_M1_Val = moisture_one.mapSensorVals()
        moist1.append(current_M1_Val)
        current_M2_Val = moisture_two.mapSensorVals()
        moist2.append(current_M2_Val)
        current_M3_Val = moisture_three.mapSensorVals()
        moist3.append(current_M3_Val)
        # Stores time in seconds when values were taken in array for plotting
        timeS.append(int(dt.now().strftime("%H"))*60*60+int(dt.now().strftime("%M"))*60+int(dt.now().strftime("%S")))

        # Creates a dict of the current vals.
        curr_data = {
            'moisture_value_1': current_M1_Val,
            'moisture_value_2': current_M2_Val,
            'moisture_value_3': current_M3_Val,
            'temp_value_1': temperature_one,
            'temp_value_2': temperature_two,
            'temp_value_3': temperature_three,
            'time': dt_string,
        }

        # Sets dt_string again to be used in print statement
        dt_string = dt.now().strftime("D%dM%mY%YH%HM%MS%S")

        # Prints the current values.
        print("Current value", current_M1_Val, current_M2_Val, current_M3_Val, '\n\tCurrent Time:', dt_string)
        print("Current Temps:\n\t" + str(temperature_one) + "\n\t" + str(temperature_two) + "\n\t" + str(temperature_three))
        
        # Write collected data to text file then wait 30 seconds
        str_dictionary = repr(curr_data)
        file.write(str_dictionary + "\n")
        time.sleep(30)
        # Set day 2 to be used to see if the day has changed by comparing against day 1
        day2 = dt.now().strftime("%d")
        
        # If day has changed, open new data file, generate moisture and temperature plots, and reset arrays and day 1
        if day1 != day2:
            file.close()
            dt_string = dt.now().strftime("D%dM%mY%YH%HM%MS%S")
            file = open("/home/pi/Desktop/CompostMonitoringSystem-main/compost_monitoring_code/CompostMonitoringData/" + dt_string + ".txt", "w")
            fig, ax = plt.subplots()
            ax.plot(timeS, temp1, label='temp 1')
            ax.plot(timeS, temp2, label='temp 2')
            ax.plot(timeS, temp3, label='temp 3')
            ax.set_xlabel('time, s')
            ax.set_ylabel('temp, deg F')
            ax.set_title("Temperature vs. Time")
            ax.legend()
            plt.savefig('/home/pi/Desktop/CompostMonitoringSystem-main/compost_monitoring_code/TemperaturePlots/' + dt_string + '.png', bbox_inches='tight')
            fig, ax = plt.subplots()
            ax.plot(timeS, moist1, label='moisture 1')
            ax.plot(timeS, moist2, label='moisture 2')
            ax.plot(timeS, moist3, label='moisture 3')
            ax.set_xlabel('time, s')
            ax.set_ylabel('moisture, ?')
            ax.set_title("Moisture vs. Time")
            ax.legend()
            plt.savefig('/home/pi/Desktop/CompostMonitoringSystem-main/compost_monitoring_code/MoisturePlots/' + dt_string + '.png', bbox_inches='tight')
            temp1 = []
            temp2 = []
            temp3 = []
            moist1 = []
            moist2 = []
            moist3 = []
            timeS = []
            day1 = dt.now().strftime("%d")

main()