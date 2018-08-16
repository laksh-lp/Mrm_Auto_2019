import math,time,serial
from gps3 import gps3
###########################Global Variables#####################################################
global stm_send,current_lat,current_long,end_lat,end_long, obstacle_distance_left,obstacle_distance_right,current_heading
################################################################################################
###########################GPS and Serial Initialization########################################
gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()
ser = serial.Serial(port='/dev/ttyUSB1',baudrate = 57600)
################################################################################################ 
##################################Main Function#################################################		
if __name__ == "__main__":
    def update():
        while True:
            
            for new_data in gps_socket:
                if new_data:
                    data_stream.unpack(new_data)
                    #ADD HEADING 
                    latitude =data_stream.TPV['lat']
                    longitude = data_stream.TPV['lon']
                    return longitude,latitude
            break		
################################################################################################
#########################GPS Distance and Heading Calculations##################################

def get_waypoint_distance(lat1,lon1,lat2,lon2):
	lat_diff=math.radians(lat2-lat1)
	lat1=math.radians(lat1)    
	lat2=math.radians(lat2)  
	lon_diff=math.radians((lon2)-(lon1))   
	waypoint_dist = (math.sin(lat_diff/2.0)*math.sin(lat_diff/2.0))
	waypoint_dist2= math.cos(lat1)
	waypoint_dist2*=math.cos(lat2)
	waypoint_dist2*=math.sin(lon_diff/2.0)*math.sin(lon_diff/2.0)                                      	
	waypoint_dist +=waypoint_dist2
	waypoint_dist=(2*math.atan2(math.sqrt(waypoint_dist),math.sqrt(1.0-waypoint_dist)))
	waypoint_dist*=6371000.0 
	#print(waypoint_dist)
	return waypoint_dist

#def get_waypoint_heading(lat1,lon1,lat2,lon2):
#	waypoint_heading = math.atan2(math.sin(lon2-lon1)*math.cos(lat2),math.cos(lat1)*math.sin(lat2)-math.sin(lat1)*math.cos(lat2)*math.cos(lon2-lon1))
#	waypoint_heading = waypoint_heading*180/3.1415926535
#	waypoint_heading = int(waypoint_heading)
#	if waypoint_heading<0:
#		waypoint_heading+=360
	#print(waypoint_heading)	
#	return waypoint_heading;

def angle_waypoint(lat1,lon1,lat2,lon2):
	try:
    	slope=(lat1-lat2)/(lon1-lon2)
        theta=math.atan(slope)
        degree2=math.fabs(math.degrees(theta))
        return degree2
    except ZeroDivisionError:
        print("ZeroDivisionError Same Longitudes Given")
#        enter()

################################################################################################
angle_buffer=10
def straight():
	stm_send='m4x4999y0000'
	print ('Going straight')
	ser.write(stm_send)
def anticlockwise():
	stm_send='m4x0000y4999'
	print('Rotating anticlockwise')
	ser.write(stm_send)
def clockwise():
	stm_send='m4x9999y4999'
	print('Rotating clockwise')
	ser.write(stm_send)
def backward():
	stm_send='m4x4999y9999'	
	print('Going backward')
	ser.write(stm_send)

def decide_move():
	if (math.fabs(current_heading-)