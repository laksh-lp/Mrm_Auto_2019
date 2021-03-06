import time
from pygame import joystick
import pygame
import math
import serial
from time import sleep
def map1(x,in_min,in_max,out_min,out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
def ellipticalSquareToDisc(x,y):
	u = x * (1.0 - y*y/2.0)**(0.5)
	v = y * (1.0 - x*x/2.0)**(0.5)
	return u,v
def ellipticalDiscToSquare(u,v):
	u2 = u * u
	v2 = v * v
	twosqrt2 = 2.0 * (2.0)**(0.5)
	subtermx = 2.0 + u2 - v2
	subtermy = 2.0 - u2 + v2
	termx = subtermx + u * twosqrt2
	termx2 = subtermx - u * twosqrt2
	termy = subtermy + v * twosqrt2
	termy2 = subtermy - v * twosqrt2
	x = 0.5 * (termx)**(0.5) - 0.5 * (termx2)**(0.5)
	y = 0.5 * (termy)**(0.5) - 0.5 * (termy2)**(0.5)
	return x,y
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
	ser.write('n'.encode())
	if m1:
			c=1
			if up:
				print('1up')
				ser.write('A'.encode())
			if down:
				print('1down')
				ser.write('B'.encode())
	if m2:
			if up:
				print('2up')
				ser.write('C'.encode())
			if down:
				print('2down')
				ser.write('D'.encode())
	if m3:
			if up:
				print('3up')
				ser.write('E'.encode())
			if down:
				print('3down')
				ser.write('F'.encode())
	if m4:
			if up:
				print('4up')
				ser.write('G'.encode())
			if down:
				print('4down')
				ser.write('H'.encode())
	if m5:
			if up:
				print('5up')
				ser.write('I'.encode())
			if down:
				print('5down')
				ser.write('J'.encode())
	if m6:
			if up:
				print('6up')
				ser.write('K'.encode())
			if down:
				print('6down')
				ser.write('L'.encode())
def motorcode():
	x1=j.get_axis(0)
	y1=j.get_axis(1)
	x=int((x1+1)*512)-512
	y=512-int((1-y1*-1)*512)
	gear=j.get_axis(3)

	gear=int(map1(gear,-1.0,1.0,9,0))
	x=map1(x,-512,512,-1,1)
	y=map1(y,-512,512,-1,1)
	x,y=ellipticalSquareToDisc(x, y)
	x1 = (x * 0.707) + (y * 0.707)
	y1 = (-x * 0.707) + (y * 0.707)
	x,y=ellipticalDiscToSquare(x1,y1)
	x=int(map1(x,-0.991273,0.991273,-255,255)*gear/9)
	y=int(map1(y,-0.991273,0.991273,-255,255)*gear/9)
	if x<20*gear/9 and x>-20*gear/9:
		x=0
	if y<20*gear/9 and y>-20*gear/9:
		y=0
	if x>230*gear/9:
		x=255*gear/9
	if y>230*gear/9:
		y=255*gear/9
	if x<-230*gear/9:
		x=-255*gear/9
	if y<-230*gear/9:
		y=-255*gear/9
	if x>=0:
		x='0'+str(int(x)).zfill(3)
	else:
		x='1'+str(int(-x)).zfill(3)
	if y>=0:
		y='0'+str(int(y)).zfill(3)
	else:
		y='1'+str(int(-y)).zfill(3)
	print(str(gear)+x+y)
	#print(x,y)
	ser.write('m'.encode())
	ser.write(adx.encode())
	ser.write(x.encode())
	#print(ser.read())
	#print(ser.read(),ser.read(),ser.read(),ser.read())
	ser.write(ady.encode())
	ser.write(y.encode())
	#print(ser.read(),ser.read(),ser.read(),ser.read())
count =0
ser=serial.Serial('/dev/ttyUSB0',9600)
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
