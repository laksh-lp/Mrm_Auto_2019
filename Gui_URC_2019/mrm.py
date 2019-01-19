import time
from pygame import joystick
import pygame
import math
import serial
from time import sleep
def map1(x,in_min,in_max,out_min,out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
def arm():
	_1u=j.get_button(6)
	_1d=j.get_button(7)
	_2u=j.get_button(8)
	_2d=j.get_button(9)
	_3u=j.get_button(10)
	_3d=j.get_button(11)
	_4u=j.get_button(4)
	_4d=j.get_button(2)
	_5u=j.get_button(5)
	_5d=j.get_button(3)
	_6u=0
	_6d=0
	ser.write('n'.encode())
	if _1u:
		print('1up')
		ser.write('A'.encode())
	elif _1d:
		print('1down')
		ser.write('B'.encode())
	elif _2u:
		print('2up')
		ser.write('C'.encode())
	elif _2d:
		print('2down')
		ser.write('D'.encode())
	elif _3u:
		print('3up')
		ser.write('E'.encode())
	elif _3d:
		print('3down')
		ser.write('F'.encode())
	elif _4u:
		print('4up')
		ser.write('G'.encode())
	elif _4d:
		print('4down')
		ser.write('H'.encode())
	elif _5u:
		print('5up')
		ser.write('K'.encode())
	elif _5d:
		print('5down')
		ser.write('L'.encode())
	elif _6u:
		print('6up')
		ser.write('K'.encode())
	elif _6d:
		print('6down')
		ser.write('L'.encode())
def motorcode():
	x1=j.get_axis(0)
	y1=j.get_axis(1)
	gear=j.get_axis(3)
	gear=int(map1(gear,-1.0,1.0,9,0))
	x=map1(x1,-1.0,1.0,0.0,9999)
	y=map1(y1,-1.0,1.0,0.0,9999)
	zero=j.get_axis(2)
	if(zero>0.7):
		x=9999
		y=4999
	elif(zero<-0.7):
		x=0
		y=4999
	x=str(int(x)).zfill(4)
	y=str(int(y)).zfill(4)
	
	ser.write('m'.encode())
	ser.write(str(gear).encode())
	ser.write('x'.encode())
	ser.write(x.encode())
	ser.write('y'.encode())
	ser.write(y.encode())
	print('m'+str(gear)+'x'+x+'y'+y)
count =0
ser=serial.Serial('/dev/ttyUSB0',38400)
joystick.init()
pygame.display.init()
j=joystick.Joystick(0)
j.init()
adx='a'
ady='b'
switch=True
active=True
while(1):

	pygame.event.pump()
	on=j.get_button(1)
	if on:
		sleep(0.2)
		if j.get_button(1):
			if active==True:
				active=False
				print('Idle')
			else:
				active=True
				print('Active')

	if active:
		change=j.get_button(0)
		if change:
			sleep(0.2)
			if j.get_button(0):
				if switch==True:
					switch=False
					print('Arm')
				else:
					switch=True
					print('Motor')

		if switch:
			motorcode()
		else:
			arm()
ser.close()
