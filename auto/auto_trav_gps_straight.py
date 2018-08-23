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
ser = serial.Serial(port='/dev/ttyUSB0',baudrate = 57600)
################################################################################################
#################################Updating GPS Location of the Rover#############################
def update():
        while True:
            
            for new_data in gps_socket:
                if (type(new_data)==type(56.8)):
                    data_stream.unpack(new_data)
                    #ADD HEADING 
                    current_lat =data_stream.TPV['lat']
                    current_long = data_stream.TPV['lon']
                    return current_lat,current_long
                else:
                	print('Waiting for GPS Values')
                	continue                    
            break	 
################################################################################################
##################################Main Traversal Functions######################################
def straight():
	stm_send='m3x4999y0000'
	print ('Going straight')
	ser.write(stm_send.encode())
def anticlockwise():
	stm_send='m3x0000y4999'
	print('Rotating anticlockwise')
	ser.write(stm_send.encode())
def clockwise():
	stm_send='m3x9999y4999'
	print('Rotating clockwise')
	ser.write(stm_send.encode())
def backward():
	stm_send='m3x4999y9999'	
	print('Going backward')
	ser.write(stm_send.encode())
def brute_stop():
	stm_send='m3x4999y4999'
	print('Brute Stop')
	ser.write(stm_send.encode())
def slow_down():
	stm_send='m3x4999y0000'	
	ser.write(stm_send.encode())
	stm_send='m2x4999y0000'
	ser.write(stm_send.encode())
	stm_send='m0x4999y0000'
	ser.write(stm_send.encode())


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

#def angle_waypoint(lat1,lon1,lat2,lon2):
#	try:
#    	slope=(lat1-lat2)/(lon1-lon2)
#        theta=math.atan(slope)
#        degree2=math.fabs(math.degrees(theta))
#        return degree2
#    except ZeroDivisionError:
#        print("ZeroDivisionError Same Longitudes Given")
#        enter()

################################################################################################
def gps_traversal(waypoint_dist):
	if(waypoint_dist<5):
		print('Stop')
		brute_stop()
	else:
		print('Distance remaining',waypoint_dist)
		straight()	

##################################Main Function#################################################		
if __name__ == "__main__":
    end_lat=13.347934
    end_long=74.72134
    update()
    waypoint_dist=get_waypoint_distance(current_lat,current_long,end_lat,end_long)
    if(waypoint_dist<5):
    	print('Stop')
    else:
    	print('Distance remaining',waypoint_dist)	

################################################################################################