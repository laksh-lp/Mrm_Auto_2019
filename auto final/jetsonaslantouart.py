
import time
import math
import socket
import serial


TCP_IP = '10.42.0.40'
TCP_PORT = 5005
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
ser=serial.Serial('/dev/ttyTHS2',38400)
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print 'Connection address:', addr
while(1):
	data = conn.recv(13)
	if not data: break
	print(data)
	ser.write(data)
conn.close()
