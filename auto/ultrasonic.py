import RPi.GPIO as GPIO

import time

GPIO.setmode(GPIO.BCM)
TRIG1 = 23
TRIG2 = 17
ECHO1 = 24
ECHO2 = 27
print ("Distance Measurement In Progress")
GPIO.setup(TRIG1,GPIO.OUT)
GPIO.setup(ECHO1,GPIO.IN)
GPIO.setup(TRIG2,GPIO.OUT)
GPIO.setup(ECHO2,GPIO.IN)
GPIO.output(TRIG1,False)
GPIO.output(TRIG2,False)
pulse_end1 = 0
pulse_end2 = 0
print ("Waiting For Sensor To Settle")

time.sleep(2)
while True:
	GPIO.output(TRIG1, True)
	GPIO.output(TRIG2, True)
	time.sleep(0.00001)

	GPIO.output(TRIG1, False)
	GPIO.output(TRIG2, False)

	while GPIO.input(ECHO1)==0 and GPIO.input(ECHO2)==0:
		pulse_start1 = time.time()
		pulse_start2 = time.time()
	while GPIO.input(ECHO1)==1 or GPIO.input(ECHO2)==1:
		if GPIO.input(ECHO1)==1:
			pulse_end1 = time.time() 
		if GPIO.input(ECHO2)==1:
			pulse_end2 = time.time()
	pulse_duration1 = pulse_end1 - pulse_start1
	pulse_duration2 = pulse_end2 - pulse_start2
	distance1 = pulse_duration1 * 17150
	distance2 = pulse_duration2 * 17150
	distance1 = round(distance1, 2)
	distance2 = round(distance2, 2)
	print ("Distance Left: ",distance2," cm ","Distance Right: ",distance1," cm")
	time.sleep(0.7589)
GPIO.cleanup()

