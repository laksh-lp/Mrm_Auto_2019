from gps3 import gps3
from math import radians, cos, sin, asin, sqrt
from geopy import distance
import time,serial

gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()

#ser = serial.Serial(port='/dev/ttyS0',baudrate = 19200)

def pos_update():
	while True:
		for new_data in gps_socket:
			if new_data:
				data_stream.unpack(new_data)
				global latitude,longitude
				latitude =  data_stream.TPV['lat']
				longitude =  data_stream.TPV['lon']
				return latitude,longitude
		        
def straight():
	stm_send='m3x4999y0000'
	print ('Going straight')
	##ser.write(stm_send.encode())
def anticlockwise():
	stm_send='m3x0000y4999'
	print('Rotating anticlockwise')
	#ser.write(stm_send.encode())
def clockwise():
	stm_send='m3x9999y4999'
	print('Rotating clockwise')
	#ser.write(stm_send.encode())
def backward():
	stm_send='m3x4999y9999'	
	print('Going backward')
	#ser.write(stm_send.encode())
def brute_stop():
	stm_send='m3x4999y4999'
	print('Brute Stop')
	#ser.write(stm_send.encode())


if __name__=="__main__":
	global end_lat,end_lon
	end_lat=13.347917
	end_long=74.792139
	end=(end_lat,end_long)
	while True:
		pos_update()

		if (type(latitude)==type('Str')):
			continue
		else:
			current=(latitude,longitude)
			print(latitude,longitude)
			waypoint_dist=(distance.distance(end,current).m)
			print (waypoint_dist)
			if waypoint_dist<10:
				brute_stop()
				print("Stop")
			else:
				straight()
				print("Forward")






