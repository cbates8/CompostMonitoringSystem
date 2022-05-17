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
import notecard
from periphery import I2C

# Locally imported files.
from moistureSensor import MoistureSensor
from TemperatureSensor import TemperatureSensor

def main():
    # helper functions

    # route: string containing one of the Ubidots routes (Temp1-3, Moisture1-3)
    # value: sensor value
    # timestamp: (int) unix time
    def postUbi(route, value, timestamp):
        try:
            req = {"req": "web.post"}
            req["route"] = "Ubidots: " + route
            req["body"] = {"value": value, "timestamp": epoch }
            rsp = card.Transaction(req)
            print("Sending " + route + f" Data\nNotecard response: {rsp}\n")
            return True
        except:
            print("error sending " + route + " data. skipping\n")
            return False
            

    # subject: string containing subject line
    # message: string containing message text
    # to: string containing destination email address
    # sends email through notecard
    # return true if succesful false otherwise
    def sendEmail(subject, message, to):
        try:
            req = {"req": "web.post"}
            req["route"] = "Email"
            req["body"] = {"personalizations": [{"to": [{"email": e}]}],"from": {"email": "ucce.bin.monitoring@gmail.com"},"subject": subject,"content": [{"type": "text/plain", "value": message}]}
            rsp = card.Transaction(req)
            print("Sending Email\n")
            print("to: " + to + "\nsubject: " + subject + "\nmessage: " + message + "\n")
            print(f"Notecard response: {rsp}\n")
            return True
        except:
            return False

    # gets unix time from a server specified in notehub routes
    # returns (int) unixtime if successful -1 otherwise 
    def getNetTime():
        try:
            req = {"req": "web.get"}
            req["route"] = "Time"
            rsp = card.Transaction(req)
            print(f"Getting Time\nNotecard response: {rsp}\n")
            return (rsp["body"])["unixtime"]
        except:
            return -1
        
    # Declare notecard stuff
    productUID = "com.gmail.ucce.bin.monitoring:compost_monitoring_system"
    port = I2C("/dev/i2c-1")
    card = notecard.OpenI2C(port, 0, 0)
    
    # Declare objects.
    emails = ["scamacho@scu.edu"]
    tempUpperThreshold = 50
    tempLowerThreshold = 49
    moistureUpperThreshold = 79
    moistureLowerThreshold = 80
    #TODO get email and threshold values off a google sheet
    
    thresholdFlags = [0,0,0,0,0,0] #i(0-2): temp1-3, i(3-5): moisture1-3. 1=out of threshold
    waitTimeDefault = 1800 # set default report interval 
    waitTime = waitTimeDefault
    
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

    # Read Calibration values from CSV to correctly map new readings
    print(f"Sensor\tAirVal\tWaterVal")
    moisture_one.readCalibrationVals()
    moisture_two.readCalibrationVals()
    moisture_three.readCalibrationVals()
    
    # Configure Notecard and confirm connection
    connected = False
    while(not connected):
        try:
            req = {"req": "hub.set"}
            req["product"] = productUID
            req["mode"] = "continuous"
            print(f"\nNotecard config request: {json.dumps(req)}")
            rsp = card.Transaction(req)
            print(f"Notecard config response: {rsp}\n")
            connected = True
        except:
            print("error connecting to internet. retrying in 1 minute\n")
            time.sleep(60)
    
    # Set day 1 used to see when a new day begins
    day1 = dt.now().strftime("%d")
    # Open first data collection file with appropriate date
    dt_string = dt.now().strftime("D%dM%mY%YH%HM%MS%S")
    file = open("/home/pi/CompostMonitoringSystem/CompostMonitoringData/" + dt_string + ".txt", "w")

    while (True):
        # Sets up the temperature variables.
        # Records values to appropriate arrays to be used for plots
        # Check if values are within threshold
        temperature_one = temp_one.read_temp()
        temp1.append(temperature_one)
        if(not (tempUpperThreshold > temperature_one > tempLowerThreshold)):
            thresholdFlags[0] = 1
        temperature_two = temp_two.read_temp()
        temp2.append(temperature_two)
        if(not (tempUpperThreshold > temperature_two > tempLowerThreshold)):
            thresholdFlags[1] = 1
        temperature_three = temp_three.read_temp()
        temp3.append(temperature_three)
        if(not (tempUpperThreshold > temperature_three > tempLowerThreshold)):
            thresholdFlags[2] = 1
        current_M1_Val = moisture_one.mapSensorVals()
        moist1.append(current_M1_Val)
        if(not (tempUpperThreshold > current_M1_Val > tempLowerThreshold)):
            thresholdFlags[3] = 1
        current_M2_Val = moisture_two.mapSensorVals()
        moist2.append(current_M2_Val)
        if(not (tempUpperThreshold > current_M2_Val > tempLowerThreshold)):
            thresholdFlags[4] = 1
        current_M3_Val = moisture_three.mapSensorVals()
        moist3.append(current_M3_Val)
        if(not (tempUpperThreshold > current_M1_Val > tempLowerThreshold)):
            thresholdFlags[5] = 1

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
        print("Current Temps:\n\t" + str(temperature_one) + "\n\t" + str(temperature_two) + "\n\t" + str(temperature_three) + "\n")
        
        # Send values to the Notecard
        noteSent = False
        while(not noteSent):
            try:
                req = {"req": "note.add"}
                req["file"] = "sensors.qo"
                req["sync"] = True
                req["body"] = {"temp1": temperature_one, "temp2": temperature_two, "temp3": temperature_three, "moisture1": current_M1_Val, "moisture2": current_M2_Val, "moisture3": current_M3_Val}
                rsp = card.Transaction(req)
                print(f"Notecard response: {rsp}\n")
                noteSent = True
            except:
                print("error note not sent. retrying in 1 minute\n")
                time.sleep(60)
        
        #TODO use internet time instead of local time
        epoch = time.time() * 1000

        # Trigger route to send Temp1 data to Ubidots
        postUbi("Temp1", temperature_one, epoch)
        time.sleep(5)

        # Trigger route to send Temp2 data to Ubidots
        postUbi("Temp2", temperature_two, epoch)
        time.sleep(5)
        
        # Trigger route to send Temp3 data to Ubidots
        postUbi("Temp3", temperature_three, epoch)
        time.sleep(5)
        
        # Trigger route to send Moisture1 data to Ubidots
        postUbi("Moisture1", current_M1_Val, epoch)
        time.sleep(5)
        
        # Trigger route to send Moisture2 data to Ubidots
        postUbi("Moisture2", current_M2_Val, epoch)
        time.sleep(5)

        # Trigger route to send Moisture3 data to Ubidots
        postUbi("Moisture3", current_M3_Val, epoch)
        time.sleep(5)
        # Send email if values are out of threshold
        if(thresholdFlags.count(1) > 0):
            message = "Hi sending a different message so i dont get thrown in the bad place. sysTime: "
            #TODO generate message based on sensor values
            netTime = getNetTime()
            message = message + str(epoch) + " netTime: " + str(netTime)
            #for e in emails:  
            #    sendEmail("Sensor values out of threshold", message, e)
            #TODO make sure email are sent out no more than once every 24 hrs
        # if error
        # print("Connection failed. retrying in 5 minutes")
        # waitTime = 300 #5 minutes

        # Write collected data to text file then wait 30 minutes
        str_dictionary = repr(curr_data)
        file.write(str_dictionary + "\n")
        time.sleep(waitTime)
        waitTime = waitTimeDefault # reset wait time back to default if it was changed
        # Set day 2 to be used to see if the day has changed by comparing against day 1
        day2 = dt.now().strftime("%d")
        

        # If day has changed, open new data file, generate moisture and temperature plots, and reset arrays and day 1
        if day1 != day2:
            file.close()
            dt_string = dt.now().strftime("D%dM%mY%YH%HM%MS%S")
            file = open("/home/pi/CompostMonitoringSystem/CompostMonitoringData/" + dt_string + ".txt", "w")
            fig, ax = plt.subplots()
            ax.plot(timeS, temp1, label='temp 1')
            ax.plot(timeS, temp2, label='temp 2')
            ax.plot(timeS, temp3, label='temp 3')
            ax.set_xlabel('time, s')
            ax.set_ylabel('temp, deg F')
            ax.set_title("Temperature vs. Time")
            ax.legend()
            plt.savefig('/home/pi/CompostMonitoringSystem/TemperaturePlots/' + dt_string + '.png', bbox_inches='tight')
            fig, ax = plt.subplots()
            ax.plot(timeS, moist1, label='moisture 1')
            ax.plot(timeS, moist2, label='moisture 2')
            ax.plot(timeS, moist3, label='moisture 3')
            ax.set_xlabel('time, s')
            ax.set_ylabel('moisture, ?')
            ax.set_title("Moisture vs. Time")
            ax.legend()
            plt.savefig('/home/pi/CompostMonitoringSystem/MoisturePlots/' + dt_string + '.png', bbox_inches='tight')
            temp1 = []
            temp2 = []
            temp3 = []
            moist1 = []
            moist2 = []
            moist3 = []
            timeS = []
            day1 = dt.now().strftime("%d")
        
        # reset threshold flags
        for i in range(len(thresholdFlags)):
            thresholdFlags[i] = 0

main()
