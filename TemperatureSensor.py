import os
import glob
import time
 
class TemperatureSensor(object):
    
    def __init__(self, index):
        self.index = index
        self.sensorids = ['28-3c01d607597a', '28-3c01d60730cb', '28-3c01d6078b4c']          # << Change these according to your sensor id
        self.base_dir = '/sys/bus/w1/devices/'
        self.device_file = self.base_dir + self.sensorids[self.index] + "/w1_slave"


    def read_temp_raw(self):
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def read_temp(self, measure=0):
        lines = self.read_temp_raw()

        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_temp_raw()
        equals_pos = lines[1].find('t=')

        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            if measure == 0:
                #temp = (temp_c, temp_f)
                temp = temp_f
            elif measure == 1:
                temp = temp_c
            else:
                temp = temp_f
            return temp