
import time
import math
import socket

UDP_IP = '192.168.1.4' # this IP of my pc. When I want raspberry pi 2`s as a server, I replace it with its IP '169.254.54.195'
UDP_PORT = 5005
BUFFER_SIZE = 1024 # Normally 1024, but I want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((UDP_IP, UDP_PORT))
def map1(x,in_min,in_max,out_min,out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
while(1):
    data=s.recvfrom(2000)
    left=int(data[0][4:8])
    right=int(data[0][12:16])
    left=str(map1(left,1000,2000,9999,0))
    right=str(map1(right,1000,2000,9999,0))
    print('m4x'+left+'y'+right)	
s.close()

