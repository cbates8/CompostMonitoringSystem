import adafruit_mcp3xxx.mcp3008 as MCP
from multiprocessing import Process

from moistureSensor import MoistureSensor

moisture_one = MoistureSensor(MCP.P0)
moisture_two = MoistureSensor(MCP.P1)
moisture_three = MoistureSensor(MCP.P3)

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

with open("calibrationValues.csv", "w") as ofile:
	ofile.write("Sensor, AirVal, WaterVal\n")
	sensors = [moisture_one, moisture_two, moisture_three]
	for s in sensors:
		ofile.write(f"{s.pinNum},{s.airVal},{s.waterVal}\n")