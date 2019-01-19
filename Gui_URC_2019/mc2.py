import RPi.GPIO as IO


import time
import math
import socket

HOST='192.168.1.69'
PORT=5005

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST,PORT))
s.listen()
conn,addr=s.accept()

def map(v, in_min, in_max, out_min, out_max):
	if v < in_min:
		v = in_min
	if v > in_max:
		v = in_max
	return (v - in_min) * (out_max - out_min) // (in_max - in_min) + out_min


def joystickToDiff(x, y, minJoystick, maxJoystick, minSpeed, maxSpeed):
	if x == 0 and y == 0:
		return (0, 0)
   
	z = math.sqrt(x * x + y * y)
	rad = math.acos(math.fabs(x) / z)
	angle = rad * 180 / math.pi

	tcoeff = -1 + (angle / 90) * 2
	turn = tcoeff * math.fabs(math.fabs(y) - math.fabs(x))
	turn = round(turn * 100, 0) / 100


	mov = max(math.fabs(y), math.fabs(x))


	if (x >= 0 and y >= 0) or (x < 0 and y < 0):
		rawLeft = mov
		rawRight = turn
	else:
		rawRight = mov
		rawLeft = turn


	if y < 0:
		rawLeft = 0 - rawLeft
		rawRight = 0 - rawRight

	
	rightOut = map(rawRight, minJoystick, maxJoystick, minSpeed, maxSpeed)
	leftOut = map(rawLeft, minJoystick, maxJoystick, minSpeed, maxSpeed)

	return (rightOut, leftOut)

if __name__=='__main__':

	IO.setwarnings(False)

	IO.setmode (IO.BCM)
	IO.setup(12,IO.OUT)
	IO.setup(13,IO.OUT)
	IO.setup(17,IO.OUT)
	IO.setup(27,IO.OUT)


	p = IO.PWM(12,500)
	q = IO.PWM(13,500)
	#r = IO.PWM(18,500)
	#s = IO.PWM(19,500)


	p.start(0)
	q.start(0)
	#r.start(0)
	#s.start(0)
	
	global a,b
	a=0
	b=0
	with conn:
                print('Connected by', addr)
                while(1):
                        data=conn.recv(12)
                        x=data[3:7]
                        y=data[8:11]
                        if not data:
                                break
                        print(data)
                        x=map(x,0.0,9999,-1.0,1.0)
						y=map(y,0.0,9999,-1.0,1.0)
                        print(x,y)	
                        if y<0.5:
                                b=1
                        else:
                                b=0	
                        #ser.write(17)
                        x,y=joystickToDiff(-x,-y,-1 ,1,-100/3,100/3)
                        if(x<10 and y<10):
                                IO.output(17,0)
                                p.ChangeDutyCycle(math.fabs(x))
                                IO.output(27,0)
                                q.ChangeDutyCycle(math.fabs(y))
                        if(x<10 and y>10):
                                IO.output(17,0)
                                p.ChangeDutyCycle(math.fabs(x))
                                IO.output(27,1)
                                q.ChangeDutyCycle(math.fabs(y))
                        if(x>10 and y<10):
                                IO.output(17,1)
                                p.ChangeDutyCycle(math.fabs(x))
                                IO.output(27,0)
                                q.ChangeDutyCycle(math.fabs(y))
                        if(x>10 and y>10):
                                IO.output(17,1)
                                p.ChangeDutyCycle(math.fabs(x))
                                IO.output(27,1)
                                q.ChangeDutyCycle(math.fabs(y))
                        #print(x,y)

