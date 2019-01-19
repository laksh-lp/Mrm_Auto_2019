import smbus
import time
import math
from gps3 import gps3
from math import radians, cos, sin, asin, sqrt
from geopy import distance
import time,serial

gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()

ser = serial.Serial(port='/dev/ttyS0',baudrate = 38400)

def pos_update():
        while True:
                for new_data in gps_socket:
                        if new_data:
                                data_stream.unpack(new_data)
                                global latitude,longitude
                                latitude =  data_stream.TPV['lat']
                                longitude =  data_stream.TPV['lon']
                                return latitude,longitude
def imu():
        bus = smbus.SMBus(1)
        pi = 3.14159265358979
        bus.write_byte_data(0x6B, 0x20, 0x0F)
        bus.write_byte_data(0x6B, 0x23, 0x30)
        time.sleep(0.5)
        data0 = bus.read_byte_data(0x6B, 0x28)
        data1 = bus.read_byte_data(0x6B, 0x29)
        xGyro = data1 * 256 + data0
        if xGyro > 32767 :
        	xGyro -= 65536
        data0 = bus.read_byte_data(0x6B, 0x2A)
        data1 = bus.read_byte_data(0x6B, 0x2B)
        yGyro = data1 * 256 + data0
        if yGyro > 32767 :print
        	yGyro -= 65536
        data0 = bus.read_byte_data(0x6B, 0x2C)
        data1 = bus.read_byte_data(0x6B, 0x2D)

        zGyro = data1 * 256 + data0
        if zGyro > 32767 :
        	zGyro -= 65536

        bus.write_byte_data(0x1D, 0x20, 0x67)
        bus.write_byte_data(0x1D, 0x21, 0x20)
        bus.write_byte_data(0x1D, 0x24, 0x70)
        bus.write_byte_data(0x1D, 0x25, 0x60)
        bus.write_byte_data(0x1D, 0x26, 0x00)

        time.sleep(0.5)
        data0 = bus.read_byte_data(0x1D, 0x28)
        data1 = bus.read_byte_data(0x1D, 0x29)
        xAccl = data1 * 256 + data0
        if xAccl > 32767 :
        	xAccl -= 65536
        data0 = bus.read_byte_data(0x1D, 0x2A)
        data1 = bus.read_byte_data(0x1D, 0x2B)
        yAccl = data1 * 256 + data0
        if yAccl > 32767 :
        	yAccl -= 65536
        data0 = bus.read_byte_data(0x1D, 0x2C)
        data1 = bus.read_byte_data(0x1D, 0x2D)

        zAccl = data1 * 256 + data0
        if zAccl > 32767 :
        	zAccl -= 65536
        while True:
                data0 = bus.read_byte_data(0x1D, 0x08)
                data1 = bus.read_byte_data(0x1D, 0x09)
                xMag = data1 * 256 + data0
                if xMag > 32767 :
                        xMag -= 65536
                data0 = bus.read_byte_data(0x1D, 0x0A)
                data1 = bus.read_byte_data(0x1D, 0x0B)
                yMag = data1 * 256 + data0
                if yMag > 32767 :
                        yMag -= 65536
                data0 = bus.read_byte_data(0x1D, 0x0C)
                data1 = bus.read_byte_data(0x1D, 0x0D)
                zMag = data1 * 256 + data0
                if zMag > 32767 :
                        zMag -= 65536
                h= math.atan2(-yMag,xMag)
                if(h > 2*pi):
                        h=h-2*pi
                if(h<0):
                        h=h+2*pi
                ha=int(h* 180/pi)
                print(ha)
                return(ha)
def get_waypoint_heading(lat1,lon1,lat2,lon2):                
        waypoint_heading = math.atan2(math.sin(lon2-lon1)*math.cos(lat2),math.cos(lat1)*math.sin(lat2)-math.sin(lat1)*math.cos(lat2)*math.cos(lon2-lon1))
        waypoint_heading = waypoint_heading*180/3.1415926535
        waypoint_heading = int(waypoint_heading)
        if waypoint_heading<0:
                waypoint_heading+=360
        #print(waypoint_heading)        
        return waypoint_heading
def get_waypoint_distance(lat1,lon1,lat2,lon2):
        l=str(lat1)
        lo=str(lon1)
        if l[len(l)-3:len(l)] is "333" or lo[len(lo)-3:len(l)] is "333":
                                return
        else:
                end=(lat2,lon2)
                current=(lat1,lon1)
                waypoint_dist=(distance.distance(end,current).m)
                return waypoint_dist

def traversal(heading,waypoint_heading):
        if turn == 1:
                while heading-waypoint_heading >  5 and get_waypoint_distance(current_lat,current_lon,end_lat,end_lon) > 5:
                        send_stm ='m4x9999y4999'
                        print('RIGHT')
                        pos_update()
        if turn == 2:
                while heading-waypoint_heading >  5 and get_waypoint_distance(current_lat,current_lon,end_lat,end_lon) > 5:
                        send_stm ='m4x0000y4999'
                        print('LEFT')
                        pos_update()
        if turn == 0 and get_waypoint_distance(current_lat,current_lon,end_lat,end_lon) > 5:
                send_stm ='m4x4999y0000'
                print('FORWARD')
                pos_update()                                        

        else:
                print  ('Reached')                                       


        
                                
global end_lat,end_lon
end_lat=13.347503
end_lon=74.792088
while True:
        current_lat,current_lon=pos_update()
        print(current_lat,current_lon)
        if type(longitude) is type('Str') or type(latitude) is type('Str'):
                continue
        imu_head=imu()
        waypoint_head=get_waypoint_heading(end_lat,end_lon,current_lat,current_lon)
        heading_diff=imu_head-waypoint_head
        print(heading_diff)
        if heading_diff >=-180:
                if heading_diff<=0:
                        turn = 1 #############RIGHT###################
                        traversal(imu_head,waypoint_head)
        if heading_diff <-180:
                turn = 2 #################LEFT####################
                traversal(imu_head,waypoint_head)
        if heading_diff>=0:
                if heading_diff<180:
                        turn = 2 
                        traversal(imu_head,waypoint_head)             
        if heading_diff >= 180:
                turn = 1
                traversal(imu_head,waypoint_head)  
        if heading_diff == waypoint_head:
                turn = 0        
        pos_update()    



