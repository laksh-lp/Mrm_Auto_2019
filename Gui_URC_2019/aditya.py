

import math
import serial
ser=serial.Serial('/dev/ttyUSB0',4800)

while(1):
	ser.write('A'.encode())
	print(ser.read())
	ser.write('H'.encode())
	print(ser.read())
	ser.write('F'.encode())
	print(ser.read())
	ser.write('Z'.encode())
	print(ser.read())