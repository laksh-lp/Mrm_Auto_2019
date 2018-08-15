import math,time,serial
ser = serial.Serial(port='/dev/ttyUSB50',baudrate = 57600)
global obstacle_left, obstacle_right
def straight():
	stm_send='m4x4999y0000'
	print ('Going straight')
	ser.write(stm_send)
def anticlockwise():
	stm_send='m4x0000y4999'
	print('Rotating anticlockwise')
	ser.write(stm_send)
def clockwise():
	stm_send='m4x9999y4999'
	print('Rotating clockwise')
	ser.write(stm_send)
def backward():
	stm_send='m4x4999y9999'	
	print('Going backward')
	ser.write(stm_send)
def brute_stop():
	stm_send='m4x4999y4999'
	print('Brute Stop')	
def obstacle_avoid():#TAKING DISTANCE IN CENTIMETERS
	while True:
		while(obstacle_right>50 and obstacle_left>50):
			straight()
		if (obstacle_right>50 and obstacle_left<50):
			while(obstacle_left<50):
				clockwise()	
		if (obstacle_left>50 and obstacle_right<50):
			while(obstacle_right<50):
				anticlockwise()	
		if(obstacle_right<50 and obstacle_left<50):
			while(obstacle_left>50 or obstacle_right>50):
				backward()
		if(obstacle_right<25 and obstacle_left<25):
			brute_stop()		
			