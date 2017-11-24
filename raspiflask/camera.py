from picamera import PiCamera
import RPi.GPIO as GPIO
import app

PICTUDE_DIR = "pictures/"

# Use GPIO numbering
GPIO.setmode(GPIO.BCM)

#Set led pin 5 as CAMLED and disabling it
CAMLED = 5
camera = PiCamera()
GPIO.setup(CAMLED, GPIO.OUT, initial=False) 

#takes picture with parameterized filename and saves it to PICTUDE_DIR
def takePicture(filename):
	if(app.debug()):
		print("INFO camera.py. takePicture(), filename: "+filename)
	GPIO.output(CAMLED,True) # On
	camera.capture(PICTUDE_DIR+filename)
	GPIO.output(CAMLED,False) # Off
	return PICTUDE_DIR