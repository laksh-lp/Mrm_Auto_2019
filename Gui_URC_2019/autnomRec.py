import time
import math
import socket
import serial

UDP_IP = '192.168.43.113' # this IP of my pc. When I want raspberry pi 2`s as a server, I replace it with its IP '169.254.54.195'
UDP_PORT = 5005
BUFFER_SIZE = 12 # Normally 1024, but I want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ser=serial.Serial('/dev/ttyS0',38400)
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((UDP_IP, UDP_PORT))
while(1):
	data=s.recvfrom(BUFFER_SIZE)
	print(data[0])
	ser.write(data[0])
