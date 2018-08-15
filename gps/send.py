from gps3 import gps3
import socket
import csv
import sys
gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('192.168.43.113',5050))
while True:
    s.listen(1)
    conn,addr = s.accept()
    try:
        for new_data in gps_socket:
            if new_data:
                data_stream.unpack(new_data)
                # print('Altitude = ', data_stream.TPV['alt'])
                print('Latitude = ', data_stream.TPV['lat'])
                print('longitude= ',data_stream.TPV['lon'])
                print(type(data_stream.TPV['lon']))
                print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
                conn.send('lat'+str(data_stream.TPV['lat'])+'lon'+str(data_stream.TPV['lon']))
    except KeyboardInterrupt:
        conn.close()
        print 'Exiting program'
        break