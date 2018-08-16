import matplotlib.pyplot as plt

from gps3 import gps3
gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()

xs=[]
ys=[]

latf = 13.347944 
lonf = 74.792061
lati = 13.347539 
loni = 74.792088

#plt.axis([13.347082, 74.789050, 13.350082, 74.802050])

latmin = lati - 0.0001
lonmin = loni - 0.0001
latmax = latf + 0.0001
lonmax = lonf + 0.0001

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





