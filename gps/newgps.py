import socket,csv,time
import matplotlib.pyplot as plt

def validate(s):
    first_occurence = s.find('lat')
    if s.find('lat',first_occurence+3) is not -1:
        return False
    first_occurence = s.find('lon')
    if s.find('lon',first_occurence+3) is not -1:
        return False
    if len(s) < 20:
        return False
    return True

def distance(y1,x1,y2,x2):
    # print('distttt',y1,x1)
    y=(y2-y1)*100
    x=(x2-x1)*100
    z=x**2+y**2
    d=(pow(z,0.5))*1000
    # print('DISTANCE=',d)
    return d
lats = []
lons = []
filename_source="source.csv"
filename_dest="dest.csv"
fields = []
rows = []
long_source=[]
lat_source=[]
lat_dest=[]
long_dest=[]
with open(filename_source, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    fields = csvreader.next()
    for row in csvreader:
        lat_source.append(float(row[0]))
        long_source.append(float(row[1]))
#        print row[0]
print"start point................."
print 'longitudes=',long_source
print 'latitudes=',lat_source
j=csvreader.line_num
num=j-1
print "Total no. of co-ordinates:",num
print('Field names are:' + ', '.join(field for field in fields))

with open(filename_dest,'r') as csvfile:
    csvreader = csv.reader(csvfile)
    fields = csvreader.next()
    for row in csvreader:
        lat_dest.append(float(row[0]))
        long_dest.append(float(row[1]))
print"destination point................."
print 'longitudes=',long_dest
print 'latitudes=',lat_dest
j=csvreader.line_num
num=j-1
print "Total no. of co-ordinates:",num
print('Field names are:' + ', '.join(field for field in fields))

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('192.168.43.113',5050))
13.349073,74.792548
13.349042,74.792590
plt.axis([13.3460,13.3499,74.7900,74.7931])
plt.ion()
lat_prev_dist=[]
long_prev_dist=[]

while True:
    incoming_msg = s.recv(72)
    if not validate(incoming_msg):
        continue
    first_occurence_lat = incoming_msg.find('lat')
    first_occurence_lon = incoming_msg.find('lon')
    latitude = incoming_msg[first_occurence_lat+3:first_occurence_lon-1]#check
    print latitude,'//////////////////////latitide of rover '
    longitude = incoming_msg[first_occurence_lon+3:]
    print longitude,'//////////////////////longitude of rover '
    #longitude = longitude[:len(longitude)-4]
    print latitude,",",longitude,"for plottingggggggggggggg" 
    print('Lat: '+str(latitude)+' Lon: '+str(longitude))
    latitude = float(latitude)
    longitude = float(longitude)
    plt.scatter(lat_dest,long_dest,marker='P',color='k',s=12)
    plt.scatter(lat_source,long_source,marker='s',color='g',s=12)
    print("happeningggggggggggggg")
#    if distance(lat_prev_dist,long_prev_dist,latitude,longitude) > 8:
#        print 'Skipped'
#        continue
    plt.plot([latitude],[longitude],marker='*',color='blue')
    lats.append(latitude)
    lons.append(longitude)
    long_prev_dist=float(longitude)
    lat_prev_dist=float(latitude)
    plt.pause(0.000001)
