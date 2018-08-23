import RPi.GPIO as GPIO
import serial
import time
ser = serial.Serial(port='/dev/ttyS0',baudrate = 19200)

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

def straight():
    stm_send='m1x4999y0000'
    print ('Going straight')
    ser.write(stm_send.encode())
def anticlockwise():
    stm_send='m1x0000y4999'
    print('Rotating anticlockwise')
    ser.write(stm_send.encode())
def clockwise():
    stm_send='m1x9999y4999'
    print('Rotating clockwise')
    ser.write(stm_send.encode())
def backward():
    stm_send='m1x4999y9999'	
    print('Going backward')
    ser.write(stm_send.encode())
def brute_stop():
    stm_send='m1x4999y4999'
    print('Brute Stop')
    ser.write(stm_send.encode())




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
    time.sleep(0.5)
    obstacle_left = pulse_duration1 * 17150
    obstacle_right = pulse_duration2 * 17150
    obstacle_left = round(obstacle_left, 2)
    obstacle_right = round(obstacle_right, 2)
    print (obstacle_right,obstacle_left)
    if(obstacle_left<0 ):
        print("Waiting for Values")
    elif (obstacle_right>50 and obstacle_left>50):
        straight()	
    elif (obstacle_right>50 and obstacle_left<50):
        clockwise()	
    elif (obstacle_left>50 and obstacle_right<50):
        anticlockwise()			
    elif (obstacle_right<50 and obstacle_left<50):
        backward()
    else :
        brute_stop()




GPIO.cleanup()

