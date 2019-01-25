import matplotlib.pyplot as plt
from math import cos, sin, degrees

from gps3 import gps3
gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()

xs=[]
ys=[]

x= latf = 13.3504603   
y= lonf = 74.7915926
lati = 13.350042
loni = 74.791308

#plt.axis([13.347082, 74.789050, 13.350082, 74.802050])

latmin = lati - 0.0001
lonmin = loni - 0.0001
latmax = latf + 0.0001
lonmax = lonf + 0.0001
way = []
r = 1


plt.axis([latmin, latmax, lonmin, lonmax])


plt.plot(lati,loni,marker='o',markersize=5, color='blue')
plt.plot(latf,lonf,marker='o',markersize=5, color='red')

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
        plt.pause(0.001)
plt.show()
