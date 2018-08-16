import math, time , serial
ser = serial.Serial(port='/dev/ttyS0',baudrate = 57600)


while True:
	stm_send='m4x4999y0000'
	ser.write(stm_send.encode())
