import time
from pygame import joystick
import pygame
import math
import serial
from time import sleep
def map1(x,in_min,in_max,out_min,out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
def arm():
	m1=j.get_button(6)
	m2=j.get_button(7)
	m3=j.get_button(8)
	m4=j.get_button(9)
	m5=j.get_button(10)
	m6=j.get_button(11)
	up=j.get_button(4)
	down=j.get_button(2)
	c=0
	
	if m1:
			c=1
			if up:
				print('1up')
				ser.write('aA'.encode())
			if down:
				print('1down')
				ser.write('aB'.encode())
	if m2:
			if up:
				print('2up')
				ser.write('aC'.encode())
			if down:
				print('2down')
				ser.write('aD'.encode())
	if m3:
			if up:
				print('3up')
				ser.write('aE'.encode())
			if down:
				print('3down')
				ser.write('aF'.encode())
	if m4:
			if up:
				print('4up')
				ser.write('aG'.encode())
			if down:
				print('4down')
				ser.write('aH'.encode())
	if m5:
			if up:
				print('5up')
				ser.write('aI'.encode())
			if down:
				print('5down')
				ser.write('aJ'.encode())
	if m6:
			if up:
				print('6up')
				ser.write('aK'.encode())
			if down:
				print('6down')
				ser.write('aL'.encode())
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
	
	#print(x,y)

	ser.write('m'.encode())
	ser.write(str(gear).encode())
	ser.write('x'.encode())
	ser.write(x.encode())
	#print(ser.read())
	#print(ser.read(),ser.read(),ser.read(),ser.read())
	ser.write('y'.encode())
	ser.write(y.encode())
	#print(ser.read(),ser.read(),ser.read(),ser.read())
	print('m'+str(gear)+'x'+x+'y'+y)
count =0
ser=serial.Serial('/dev/ttyS0',19200)
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
