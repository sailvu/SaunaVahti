import smbus
import sys
import app 

REG_TEMP = 0b00
I2C_ADDRESS = 0x48

def getTemperature():
	if(app.debug()):
		print("INFO thermometer.py, getTemperature()")
	bus = smbus.SMBus(1)
	temperature = bus.read_byte_data(I2C_ADDRESS, REG_TEMP)
	if(app.debug()):
		print("INFO temperature: "+str(temperature))
	return str(temperature)