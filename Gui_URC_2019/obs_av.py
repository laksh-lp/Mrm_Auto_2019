import lidar
import ultrasonic1
import ultrasonic2
from time import sleep

def straight():
	stm_send='m2x4999y0000'
	print ('Going straight')
	ser.write(stm_send.encode())
def anticlockwise():
	stm_send='m2x0000y4999'
	print('Rotating anticlockwise')
	ser.write(stm_send.encode())
def clockwise():
	stm_send='m2x9999y4999'
	print('Rotating clockwise')
	ser.write(stm_send.encode())
def backward():
	stm_send='m2x4999y9999'	
	print('Going backward')
	ser.write(stm_send.encode())
def brute_stop():
	stm_send='m2x4999y4999'
	print('Brute Stop')
	ser.write(stm_send.encode())
while True:
	ld=lidar.get_distnce()
	ur=ultrasonic1.get_distance()
	ul=ultrasonic2.get_distance()
	if ld<20 or ul<20 or ur<20:
		if ld<10:
			backward()
			sleep(0.3)
			brute_stop()
		else if ul<ur:
			clockwise()
		else if ul>ur:
			anticlockwise()

	else straight()

