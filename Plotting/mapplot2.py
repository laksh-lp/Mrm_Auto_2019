import matplotlib.pyplot as plt
from math import cos, sin, degrees
from coords import coordinates
from gps3 import gps3
gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()

xs=[]
ys=[]
f=[]
f = coordinates()
latf = f[2]
lonf = f[3]
lati = f[0]
loni = f[1]

#plt.axis([13.347082, 74.789050, 13.350082, 74.802050])

latmin = lati - 0.001
lonmin = loni - 0.001
latmax = latf + 0.001
lonmax = lonf + 0.001
#way = []
#r = 1


plt.axis([latmin, latmax, lonmin, lonmax])


plt.plot(lati,loni,marker='o',markersize=7, color='blue', label='Start Point')
plt.plot(latf,lonf,marker='o',markersize=7, color='red', label='End Point')

if f[4]!=0 and f[5]!=0:
    plt.plot(lati,loni,marker='v',markersize=5, color='black', label='Waypoint 1')
if f[6]!=0 and f[7]!=0:
    plt.plot(lati,loni,marker='v',markersize=5, color='yellow', label='Waypoint 2')
if f[8]!=0 and f[9]!=0:
    plt.plot(lati,loni,marker='v',markersize=5, color='blue', label='Waypoint 3')
if f[10]!=0 and f[11]!=0:
    plt.plot(lati,loni,marker='v',markersize=5, color='red', label='Waypoint 4')
if f[12]!=0 and f[13]!=0:
    plt.plot(lati,loni,marker='v',markersize=5, color='green', label='Waypoint 5')
if f[14]!=0 and f[15]!=0:
    plt.plot(lati,loni,marker='v',markersize=5, color='brown', label='Waypoint 6')


for new_data in gps_socket:
    if new_data:
        data_stream.unpack(new_data)

        lat = data_stream.TPV['lat']
        lon = data_stream.TPV['lon']
        if(type(lat) == type('s')):
        	print("Waiting for GPS values")
        	continue
        print(lat,lon)

        xs.append(lat)
        ys.append(lon)

        #latitude = float(lat)
        #longitude = float(lon)

        plt.plot(lat,lon,marker='o',markersize=3, color='green')
        plt.draw()
        plt.legend()
        plt.pause(0.001)
plt.show()