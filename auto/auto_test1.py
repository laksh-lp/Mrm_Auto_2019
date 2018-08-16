import math,time,serial
import RPi.GPIO as GPIO
<<<<<<< HEAD
ser = serial.Serial(port='/dev/ttyS0',baudrate = 57600)
=======
ser = serial.Serial(port='/dev/ttyS0',baudrate = 19200)
>>>>>>> 650f639562c5cc29004c0ed19c9cf196cb0b7e1e

####################################################################################################

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
def get_ult(obstacle_right,obstacle_left):
<<<<<<< HEAD
        time.sleep(1)
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
            obstacle_right = pulse_duration1 * 17150
            obstacle_left = pulse_duration2 * 17150
            obstacle_left = round(obstacle_left, 2)
            obstacle_right = round(obstacle_right, 2)
            print(obstacle_right,obstacle_left)
            if(obstacle_left<0):
				print("Waiting for Values")
			if (obstacle_right>50 and obstacle_left>50):
				straight()	
			if (obstacle_right>50 and obstacle_left<50):
				clockwise()	
			if (obstacle_left>50 and obstacle_right<50):
				anticlockwise()	
			if(obstacle_right<50 and obstacle_left<50):
				slow_down()
				if(obstacle_right<25 and obstacle_left<25):
				  brute_stop()
				  backward()
=======
	time.sleep(1)
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
		obstacle_right = pulse_duration1 * 17150
		obstacle_left = pulse_duration2 * 17150
		obstacle_left = round(obstacle_left, 2)
		obstacle_right = round(obstacle_right, 2)
		print(obstacle_right,obstacle_left)
		if(obstacle_left<0):
			print("Waiting for Values")
		if (obstacle_right>50 and obstacle_left>50):
			straight()	
		if (obstacle_right>50 and obstacle_left<50):
			clockwise()	
		if (obstacle_left>50 and obstacle_right<50):
			anticlockwise()	
		if(obstacle_right<50 and obstacle_left<50):
			if(obstacle_right<25 and obstacle_left<25):
				brute_stop()
			else:  	
				backward()
>>>>>>> 650f639562c5cc29004c0ed19c9cf196cb0b7e1e

                #time.sleep(0.7589)
####################################################################################################
def straight():
	stm_send='m3x4999y0000'
	print ('Going straight')
	ser.write(stm_send.encode())
def anticlockwise():
	stm_send='m3x0000y4999'
	print('Rotating anticlockwise')
	ser.write(stm_send.encode())
def clockwise():
	stm_send='m3x9999y4999'
	print('Rotating clockwise')
	ser.write(stm_send.encode())
def backward():
	stm_send='m3x4999y9999'	
	print('Going backward')
	ser.write(stm_send.encode())
def brute_stop():
	stm_send='m3x4999y4999'
	print('Brute Stop')
	ser.write(stm_send.encode())
<<<<<<< HEAD
def slow_down():
	stm_send='m3x4999y0000'	
	ser.write(stm_send.encode())
	stm_send='m2x4999y0000'
	ser.write(stm_send.encode())
	stm_send='m0x4999y0000'
	ser.write(stm_send.encode())

=======
def obstacle_avoid(obstacle_right,obstacle_left):#TAKING DISTANCE IN CENTIMETERS
	if(obstacle_left<0):
		print("Waiting for Values")
	if (obstacle_right>50 and obstacle_left>50):
		straight()	
	if (obstacle_right>50 and obstacle_left<50):
		clockwise()	
	if (obstacle_left>50 and obstacle_right<50):
		anticlockwise()	
	if(obstacle_right<50 and obstacle_left<50):
		if(obstacle_right<25 and obstacle_left<25):
		  brute_stop()
		else:  	
			backward()
	get_ult(obs)		
>>>>>>> 650f639562c5cc29004c0ed19c9cf196cb0b7e1e

			

if __name__=='__main__':
	obstacle_left=-1111111.0
	obstacle_right=-1111111.0
	get_ult(obstacle_right,obstacle_left)





GPIO.cleanup()







