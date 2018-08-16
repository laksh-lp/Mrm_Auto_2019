import math, time , serial
from gps3 import gps3
#############################GLOBAL VARIABLES##################################################
global latitude,longitude,heading,late,lone,turn,send_stm, current_lat,current_long

###############################################################################################
###########################GPS and Serial Initialization########################################
gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()
#ser = serial.Serial(port='/dev/ttyUSB1',baudrate = 57600)
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

def get_waypoint_heading(lat1,lon1,lat2,lon2):
	waypoint_heading = math.atan2(math.sin(lon2-lon1)*math.cos(lat2),math.cos(lat1)*math.sin(lat2)-math.sin(lat1)*math.cos(lat2)*math.cos(lon2-lon1))
	waypoint_heading = waypoint_heading*180/3.1415926535
	waypoint_heading = int(waypoint_heading)
	if waypoint_heading<0:
		waypoint_heading+=360
	#print(waypoint_heading)	
	return waypoint_heading;
		
################################################################################################


def callfn():
	current_lat=float(input())
	current_long=float(input())
	late=float(input())
	lone=float(input())
	print("Distance to be achieved",get_waypoint_distance(current_lat,current_long,late,lone))
	print("Heading difference",get_waypoint_heading(current_lat,current_long,late,lone))
	while get_waypoint_distance(current_lat,current_long,late,lone)>2:
		current_lat,current_long,heading=update()
		turn = 0
		move_heading(heading,waypoint_heading)

#####################################################################################################
#######################################Start Moving##################################################
def move_heading(heading,waypoint_heading):
	heading_diff=heading-waypoint_heading
	if heading_diff >=-180:
		if heading_diff<=0:
			turn = 1 #############RIGHT###################
			traversal()
	if heading_diff <-180:
		turn = 2 #################LEFT####################
		traversal()
	if heading_diff>=0:
		if heading_diff<180:
			turn = 2 
			traversal()		
	if heading_diff >= 180:
	    	turn = 1
	    	traversal()  
    if heading == waypoint_heading:
    	turn = 0	
    update()	

def traversal():
	if turn == 1:
		while heading-waypoint_heading >  5 and get_waypoint_distance(current_lat,current_long,late,long) > 5:
			send_stm ='m4x9999y4999'
			update()
	if turn == 2:
		while heading-waypoint_heading >  5 and get_waypoint_distance(current_lat,current_long,late,long) > 5:
			send_stm ='m4x0000y4999'
			update()
	if turn == 0 and get_waypoint_distance(current_lat,current_long,late,long) > 5:
	    send_stm ='m4x4999y0000'
	    	update()					

	else 
		print = 'Reached'	    		

########################################################################################################    		