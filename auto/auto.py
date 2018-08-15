#with function for writing and printing
import math,serial,smbus,time,sys 
from gps3 import gps3 
import numpy as np 
import cv2 
gps_socket = gps3.GPSDSocket() 
data_stream = gps3.DataStream() 
gps_socket.connect() 
gps_socket.watch()#gps done
#serial
ser = serial.Serial(port='/dev/ttyUSB1',baudrate = 57600)
#open serial
class hmc5883l:#for heading and gps values in last loop
    __scales = {
        0.88: [0, 0.73],
        1.30: [1, 0.92],
        1.90: [2, 1.22],
        2.50: [3, 1.52],
        4.00: [4, 2.27],
        4.70: [5, 2.56],
        5.60: [6, 3.03],
        8.10: [7, 4.35],
    }
    def __init__(self, port=0, address=0x1E, gauss=1.3, declination=(0,0)):
        self.bus = smbus.SMBus(port)
        self.address = address
        (degrees, minutes) = declination
        self.__declDegrees = degrees
        self.__declMinutes = minutes
        self.__declination = (degrees + minutes / 60) * math.pi / 180
        (reg, self.__scale) = self.__scales[gauss]
        self.bus.write_byte_data(self.address, 0x00, 0x70) # 8 Average, 15 Hz, normal measurement
        self.bus.write_byte_data(self.address, 0x01, reg << 5) # Scale
        self.bus.write_byte_data(self.address, 0x02, 0x00) # Continuous measurement
    def declination(self):
        return (self.__declDegrees, self.__declMinutes)
    def twos_complement(self, val, len):
         # Convert twos compliment to integer
        if (val & (1 << len - 1)):
            val = val - (1<<len)
        return val
    def __convert(self, data, offset):
        val = self.twos_complement(data[offset] << 8 | data[offset+1], 16)
        if val == -4096: return None
        return round(val * self.__scale, 4)
    def axes(self):
        data = self.bus.read_i2c_block_data(self.address, 0x00)
        #print map(hex, data)
        x = self.__convert(data, 3)
        y = self.__convert(data, 7)
        z = self.__convert(data, 5)
        return (x,y,z)
    def heading(self):
        (x, y, z) = self.axes()
#	print(str(x)+' '+str(y))#to check if hmc is connected
        headingRad =math.atan2(y,x)
        headingRad += self.__declination
        # Correct for reversed heading
        if headingRad < 0:
            headingRad += 2 * math.pi
        # Check for wrap and compensate
        elif headingRad > 2 * math.pi:
            headingRad -= 2 * math.pi
        # Convert to degrees from radians
        headingDeg = headingRad * 180 / math.pi
        return headingDeg
    def degrees(self, headingDeg):
        degrees = math.floor(headingDeg)
        minutes = round((headingDeg - degrees) * 60)
        return (degrees, minutes)
    def __str__(self):
        (x, y, z) = self.axes()
        return "Axis X: " + str(x) + "\n" \
               "Axis Y: " + str(y) + "\n" \
               "Axis Z: " + str(z) + "\n" \
               "Declination: " + self.degrees(self.declination()) + "\n" \
               "Heading: " + self.degrees(self.heading()) + "\n"
if __name__ == "__main__":
    compass = hmc5883l(gauss = 4.7, declination = (-2,5))
    def update():
        while True:
            a=hmc5883l()
            for new_data in gps_socket:
                if new_data:
                    data_stream.unpack(new_data)
                    global latitude,longitude,heading
                    heading=float(a.heading())
                    latitude =data_stream.TPV['lat']
                    longitude = data_stream.TPV['lon']
                    return longitude,latitude,heading
            break#end heading and gps values

#####################################
################OPENCV###############
#####################################

##########INITIALIZE CAMERA##########




############################################################################################################################
########HSV VALUES########
#OUTDOOR = [20-70,100-255,50-255]
#INDOOR = [30-50,100-255,100-255]
##########################

##########INITIALIZE CAMERA##########
cv_a = cv2.VideoCapture(1)
ret1,cv_b=cv_a.read()
print 'Starting Camera...'
while ret1!=True:
    cv_a=0
    cv_a=cv2.VideoCapture(1)
    ret1,cv_b=cv_a.read()
print 'DONE'

#####################################
count = 0
cv_esc = 0
cv_eqn1 = 0
cv_area_m = 0
cv_timeout = 0
cv_cnt2 = 0
cv_cnt1 = 0
cv_rot = 0
cv_prev_radius = 0
cv_prev_cx = 0
cv_prev_cy = 0
cv_test_area = 0
cv_cx = 0
cv_cy = 0
######################################
def align (x,y,rotation):
    if rotation == 0:
        for w in range(400):
            print 'Searching - Clockwise'
            ser.write('a20482048233c')
        for q in range(500):
            ser.write('a20482048202c')
            print 'stop'
    elif rotation == 1:
        if x>=0 and x<=280:
            ser.write('a20482048201c')
            print 'Anticlockwise'
        elif x>=360 and x<=640:
            ser.write('a20482048203c')
            print 'Clockwise'
        elif x>280 and x<360:
            ser.write('a20482048202c')
            print 'Forward'
    elif rotation == -1:
        ser.write('a20482048202c')
        print 'Found,stop'
        return 27

def area (ar):
    if ar >=1000:
        return -1
    else:
        return 1

def ball_detect():
	global cv_timeout,cv_cx,cv_cy,cv_rot,cv_prev_cx,cv_prev_cy,cv_prev_radius,cv_cnt1,cv_test_area,cv_Radius
	while (1):
	    if cv_timeout >= 1000:
		cv_timeout = 0
		cv_cnt1 = 0
		cv_rot = 0
		print 'timeout resetting'
	    ret1, cv_b = cv_a.read()
	    #cv_gauss = cv2.GaussianBlur(cv_b, (5, 5), 100)
	    cv_c = cv2.cvtColor(cv_b, cv2.COLOR_BGR2HSV)
	    cv_t1 = np.array([20, 100, 50])
	    cv_t2 = np.array([70, 255, 255])
	    cv_m = cv2.inRange(cv_c, cv_t1, cv_t2)
	    cv_f = cv2.bitwise_and(cv_b, cv_b, mask=cv_m)
	    cv_md = cv2.medianBlur(cv_f, 15)
	    cv_gray = cv2.cvtColor(cv_md, cv2.COLOR_BGR2GRAY)
	    cv_mask = cv2.adaptiveThreshold(cv_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 5)
	    cv_edges = cv2.Canny(cv_mask, 100, 255)
	    cv_dil = cv2.dilate(cv_edges, kernel=(3, 3), iterations=1)
	    _, cv_co, hierarchy = cv2.findContours(cv_dil, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	    for i in cv_co:
		cv_M = cv2.moments(i)
		if (cv_M["m00"] != 0):
		    cv_cx = cv_M["m10"] / cv_M["m00"]
		    cv_cy = cv_M["m01"] / cv_M["m00"]
		    cv_first = (i[0][0][0] - cv_cx) * (i[0][0][0] - cv_cx)
		    cv_second = (i[0][0][1] - cv_cy) * (i[0][0][1] - cv_cy)
		    cv_Radius = cv2.contourArea(i) / (np.pi)
		    cv_eqn = (cv_first + cv_second) - cv_Radius
		    #cv_eqn1 += np.int(cv_eqn)
		    cv_area_m = cv2.contourArea(i)
		    if (cv_eqn <= 10 and cv_eqn >= (-10)) and cv_area_m >= 700:
		        cv_prev_cx = cv_cx = np.int(cv_cx)
		        cv_prev_cy = cv_cy = np.int(cv_cy)
		        cv_prev_radius = cv_Radius = np.int(np.sqrt(cv_Radius))
		        cv2.circle(cv_b, (cv_cx, cv_cy), cv_Radius, (255, 0, 0), -1)
		        cv_cnt1 = cv_cnt1 + 1
		        if cv_cnt1 >= 3:
		            cv_rot = area(cv_area_m)
                            print('Rotation '+str(cv_rot)+'Area '+str(cv_area_m))
		        else:
		            cv_rot = 0
		        cv_test_area = cv2.contourArea(i)#####To print area when found
		else:
		    cv_cx = cv_prev_cx
		    cv_cy = cv_prev_cy
		    cv_Radius = cv_prev_radius
		cv2.drawContours(cv_b, cv_co, -1, (0, 0, 255), 1)
	    cv_esc = align(cv_cx, cv_cy, cv_rot)  ######To break out of loop when found
	    cv_x = cv2.waitKey(1) & 0xFF
	    cv_timeout+=1
            cv2.imshow('asdas',cv_b)
	    if cv_x == 27 or cv_esc == 27:
		break
	print 'Area:',cv_area_m
	time.sleep(5)

###############################################################################################################
#######################################################

#num = int(input("Enter how many cordinates you want:"))

#longitudes= list()
#latitudes=list()

num=2
latitudes=[13.348852]
longitudes=[74.792507]


#print 'Enter cordinates as asked in order:'
#for i in range(num):
#    long=float(input("enter logitude of destination point :"))
#    longitudes.append(long)
#    lat=float(input("enter latitude of destination point :"))
#    latitudes.append(lat)

currentcord=0#for multiple points
for z in range(0,5000):
    update()
    print(type(longitude))
    if(type(longitude)is not type('sdas')):
	break
    print('latitude=',latitude)
    print('longitude=',longitude)
    print('heading=',heading)
    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXX')


def chord():
    for range in (0,3):
        update()
        lat1=latitude
        long1=longitude
        head=360-heading
    return lat1,long1,head#cordinates of rover


def distance(y1,x1,y2,x2):
    y=(y2-y1)*100
    x=(x2-x1)*100
    z=x**2+y**2
    d=(pow(z,0.5))*1000
    return d

def angle(y1,x1,y2,x2):
    try:
        slope=(y1-y2)/(x1-x2)
        theta=math.atan(slope)
        degree2=math.fabs(math.degrees(theta))
        return degree2
    except ZeroDivisionError:
        print("enter x cordinates properly")
#        enter()

#(latitudes,longitudes)=ch()

def updates():#updated heading,angle and distance left to achieve
    global d,ang,h,q,f,c,a,currentcord
    (lat1,long1,h)=chord()
    lat2=latitudes[currentcord]
    long2=longitudes[currentcord]
    print('present+given chords',lat1,long1,lat2,long2)
    d=distance(lat1,long1,lat2,long2)
    ang=angle(lat1,long1,lat2,long2)
    q=quad(lat1,long1,lat2,long2)
#    [f,c,a]=speed(d)
    print('DISTANCE=',d,'Rang=',ang,'HEADING=',h,'q=',q)

def quad(lat1,long1,lat2,long2):
    if long1>=0:
        if long1>=long2:
            xaxis=1#positive quad
        elif(long1<long2):
            xaxis=0#negative quad
    if lat1>=0:
        if lat1>=lat2:
            yaxis=1
        else:
            yaxis=0
    if xaxis==1 and yaxis==1:
        quad=1
    elif xaxis==1 and yaxis==0:
        quad=2
    elif xaxis==0 and yaxis==0:
        quad=3
    elif xaxis==0 and yaxis==1:
        quad=4
    return quad


def forward():
	speed(d)
	ser.write(f)
	print('forward',f)

def clock():
	[f,c,a]=speed(d)
	ser.write(c)
	print('clock',c)

def anti():
	[f,c,a]=speed(d)
	ser.write(a)
	print('anti',a)
f=''
c=''
a=''
i=26
newd=0
cal=list()
cal=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]#27
def speed(d):
    global cal,i,f,c,a,newd
#    cal.append(d)
    change=abs(cal[i]-cal[i-25])
    print 'cal[i]',cal[i]
    print 'cal[i-25]',cal[i-25]
    print('d=',d,'change=',change)
    print 'i is',i
    cal.append(d)
    i+=1
#    newd=d
    if(i>45):
        if(change<0.5):
            for z in range(1500):
                f='a20483072252c'
                ser.write(f)
                print('stuck in an area',f)
            cal=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]#27
            i=26
            print 'cal',cal,'i',i
    if d>=8:
        f='a20483072252c'#gear 38
        c='a20482048203c'#gear 20
        a='a20482048201c'#gear 20
    elif d<8 and d>=5:
        f='a20483072222c'#gear 28
        c='a20482048203c'#gear 15
        a='a20482048201c'#gear 15
    elif d<=5:
        f='a20483072192c'#gear 20
        c='a20482048193c'#gear 10
        a='a20482048191c'#gear10
    print 'speeeeed',f,c,a
    return f,c,a


updates()
s='a10241024132c'
buffer=20#buffer
acc=2#accuracy
def traversal():
	try:
		while True:
                    updates()
		    print('_______________________________________________________________')
		    if q==1:

		        angy=90-ang
		        print('ACTUAL ANG=',angy)
		#if math.fabs(h-angy)<buffer or (360-buffer+angy)<h  #for missing buffer first quadrant
		        if d>acc:
		            if math.fabs(h-angy)<buffer or (360-buffer+angy)<h:
				forward()
		                continue
		            elif h>0 and h<angy:
				clock()
		                if math.fabs(h-angy)<buffer or (360-buffer+angy)<h:#rotate clockwise till diff less than 50
		                    forward()
		                    continue
		            elif(h-angy)>=180:
		                clock()
		                if math.fabs(h-angy)<buffer or (360-buffer+angy)<h:#rotate anticlockwise till diff than 50
		                    forward()
		                    continue
		            elif(h-angy)<180:
		                anti()
		                if math.fabs(h-angy)<buffer or (360-buffer+angy)<h:#rotate anticlockwise till diff than 50
		                    forward()
		                    continue
		            else:
		                anti()
		                continue
		        elif d<acc:
#                            currentcord+=1
		            break

		    elif q==2:
		        angx=ang+90
		        print('actual ang=',angx)
		        if d>acc:
		            if math.fabs(h-angx)<buffer:
		                forward()
		                continue
		            elif (h<angx):
		                clock()
		                if math.fabs(h-angx)<buffer:
		                    forward()
		                    continue
		            elif(h-angx)>=180:
		                clock()
		                if math.fabs(h-angx)<buffer:
		                    forward()
		                    continue
		            elif(h-angx)<180:
		                anti()
		            elif h>=0 and h<=90:
		                clock()
		            else:
		                anti()
		                print('nothing detected rotating anticlockwise')
		                continue
		        elif d<acc:
#		            currentcord+=1
		            break

		    elif q==3:
		        angy=270-ang
		        print('anctual ang=',angy)
		        if d>acc:
		            if math.fabs(h-angy)<buffer:
		                forward()
		                continue
		            elif h>180 and h<angy:
		                clock()
		                if math.fabs(h-angy)<buffer:
		                    forward()
		                    continue
		            elif h>180 and (h>angy):
		                anti()
		                if math.fabs(h-angy)<buffer:
		                    forward()
		                    continue
		            elif (h<360) and (h>angy):
		                anti()
		                if math.fabs(h-angy)<buffer:
		                    forward()
		                    continue
		            elif (angy-h)<180:
		                clock()
		                if math.fabs(h-angy)<buffer:
		                    forward()
		                    continue
		            elif (angy-h)>180:
		                anti()
		                if math.fabs(h-angy)<buffer:
		                    forward()
		                    continue
		            else:
		                ser.write(a)
		                print('nothing detected rotating anticlockwise')
		                continue
		        elif d<acc:
#		            currentcord+=1
		            break

		    elif q==4:
		#math.fabs(h-angx)<buffer or (angx+buffer-360)>h
		        angx=270+ang
		        print('actual ang=',angx)
		        if d>acc:
		            if math.fabs(h-angx)<buffer or (-360+angx+buffer)>h:
		                forward()
		                continue
		            elif(angx-h)>180:
		                anti()
		                if math.fabs(h-angx)<buffer or (-360+angx+buffer)>h:
		                    forward()
		                    continue
		            elif h>angx:
		                anti()
		                if math.fabs(h-angx)<buffer or (-360+angx+buffer)>h:
		                    forward()
		                    continue
		            elif(angx-h)<180:
		                clock()
		                if math.fabs(h-angx)<buffer or (-360+angx+buffer)>h:
		                    forward()
		                    continue
		            else:
		                anti()
		                print('nothing detected rotating anticlockwise')
		                continue
		        elif d<acc:
#		            currentcord+=1
		            break

		print("REACHED:looking for marker")
		ball_detect()


	except KeyboardInterrupt:
		ser.write(s)
		ser.close()
		print('Exiting...')
		sys.exit(0)


for y in range(num):
        print('currentcord before traversal function',currentcord)
        print y
	traversal()
        print 'completed point',(y+1)
        currentcord+=1
        print('currentcord after traversal function',currentcord)

#exit loop if heading not matched till sometime#gears-while testing

print 'Closing'
cv_a.release()
