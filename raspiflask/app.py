from flask import Flask, render_template, send_from_directory
import image
from PIL import Image, ImageDraw, ImageFont
import camera
import thermometer
import sys
import smbus
import time
from datetime import datetime, timedelta
import requests

app = Flask(__name__)

ACTIVE = False
previousTemp = None #1 #for testing only
previousTime = None

debug = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start-program:<filename>:<goalTemp>')
def startProgram(filename,goalTemp):
	try:		
		if(debug()):
			print("INFO app.py, startProgram() filename: {}, goalTemp: {} ".format(filename, goalTemp))	
		
		global ACTIVE
		ACTIVE=True		
		currentTemp = int(thermometer.getTemperature())
		picturePath = camera.takePicture(filename) + filename
		getPictureInfo(picturePath, currentTemp, goalTemp)
	except Exception as e:
		print("ERROR: {}".format(e))
	return send_from_directory(".", picturePath)

@app.route("/stop-program")
def stopProgram():
	if(debug()):
		print("INFO app.py, stopProgram()")	
	global ACTIVE
	ACTIVE=False
	global previousTemp
	global previousTime
	#previousTemp = 1 #for testing only
	previousTime = None
	return str(ACTIVE)
	
@app.route("/check-activity")
def isActive():
	global ACTIVE
	if(debug()):
		print("INFO app.py isActive(), ACTIVE: {}".format(ACTIVE))
	return str(ACTIVE)
	
@app.route("/set-active")
def setActive():
	global ACTIVE
	if(debug()):
		print("INFO app.py setActice(), ACTIVE: {}".format(ACTIVE))
	ACTIVE=True
	if(debug()):
		print("INFO ACTIVE: {}".format(ACTIVE))
	return str(ACTIVE)
	

def getPictureInfo(picturePath, currentTemp, goalTemp):
	if(debug()):	
		print("INFO: app.py, getPictureInfo(), picturePath: {}, currentTemp: {}, goalTemp: {}, ACTIVE: {}"
			.format(picturePath, str(currentTemp), str(goalTemp), ACTIVE))	

	image = Image.open(picturePath)
	font_type = ImageFont.truetype("FreeSans.ttf", 18)
	draw = ImageDraw.Draw(image)
	max = image.size[1]		
	lineDiff=20
	infoLines=[
		"KELLONAIKA: ",
		"LÄMPÖTILA NYT: ",
		"TAVOITELÄMPÖTILA: ",
		"AIKAA JÄLJELLÄ: "]
	createTextLines(draw,infoLines,10,max-10,lineDiff,font_type)
	resultLines=[
		datetime.now().strftime("%H:%M - %d.%m.%Y"),
		str(currentTemp),
		str(goalTemp),
		getTimeEstimate(currentTemp, goalTemp)
		]
	createTextLines(draw,resultLines,max/2,max-10,lineDiff,font_type)		
	image.save(picturePath)

def getTimeEstimate(currentTemp, goalTemp):
	#currentTemp = previousTemp+3 # for testing only
	if(debug()):
		print("INFO app.py, getTimeestimate(), currentTemp: {}, goalTemp: {}".format(currentTemp, goalTemp))
	global previousTemp
	global previousTime
	
	if(previousTemp is not None and previousTime is not None):		
		if(debug()):
			print("INFO previousTemp: {}, previousTime: {}".format(previousTemp, previousTime))			
		try:
			currentTime = datetime.now().replace(microsecond=0)		
			deltaTemp = currentTemp - previousTemp
			if(deltaTemp <= 0):
				return("SAUNA EI OLE PÄÄLLÄ!")
			deltaTime = currentTime - previousTime
			deltaSeconds = int(deltaTime.total_seconds())
			previousTemp= currentTemp
			previousTime=currentTime
			tempIncreasePerSecond = (deltaTemp/deltaSeconds)
			tempToGo = int(goalTemp)-currentTemp	
			secondsToGo = int(tempToGo/tempIncreasePerSecond)
			timeToGo = str(timedelta(seconds=secondsToGo))
			readyTime = currentTime + timedelta(seconds=secondsToGo)	
			
			if(debug()):
				print("INFO DELTA Temp: {}, Time: {}, seconds: {}".format(deltaTemp, deltaTime, deltaSeconds))	
				print("INFO tempIncreasePerSecond: {}".format(tempIncreasePerSecond))
				print("INFO will be ready for: {}".format(readyTime))
				print("INFO tempToGo: {}".format(tempToGo))
				print("INFO secondsToGo: {}".format(secondsToGo))
				print("INFO timeToGo: {}".format(timeToGo))
			
			if(readyTime < currentTime):
				return("VALMIS!")				
		except Exception as e:
			print("ERROR: {}".format(e))
			return("-")
			
		return("{} ( {} )".format(timeToGo, readyTime.strftime("%H:%M")))
	else:
		if(debug()):
			print("INFO no previous info!")
		previousTemp = currentTemp
		previousTime = datetime.now().replace(microsecond=0)
		return("-")	

def createTextLines(draw, textLines,x,y,lineDiff,font_type):
	for i in range(len(textLines)):
		y=y-lineDiff
		draw.text(
			xy=(x,y), 
			text=textLines[i], 
			fill=(255,255,255),
			font=font_type
			)		
		#print("INFO x: {}, y: {}, text: {}".format(x,y,textLines[i]))

def debug():
	global debug
	return debug

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0') # normal debug == False because some bug which prevented startup