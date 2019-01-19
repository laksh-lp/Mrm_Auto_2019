import matplotlib.pyplot as plt
import pyproj
import pygame as pg


from gps3 import gps3
g = pyproj.Geod(ellps='WGS84')

gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()
pg.init()
screen = pg.display.set_mode((300, 300))
clock = pg.time.Clock()
player_img = pg.Surface((42, 70), pg.SRCALPHA)
pg.draw.polygon(player_img, pg.Color('dodgerblue1'),
                [(0, 70), (21, 2), (42, 70)])
player_rect = player_img.get_rect(center=screen.get_rect().center)

def get_heading():
    (az12, az21, dist) = g.inv(loni, lati, lonf, latf)
    if az12<0:
        az12=az12+360
    return az12, dist
def pos_update():
    while True:
        for new_data in gps_socket:
            if new_data:
                    data_stream.unpack(new_data)
                    global latitude,longitude
                    latitude =  data_stream.TPV['lat']
                    longitude =  data_stream.TPV['lon']
                    if (type(latitude)==type('Str')):
                            continue
                    else:
                           
                            current=(latitude,longitude)
                            
                            return latitude,longitude
xs=[]
ys=[]

global latf
global lonf
latf = 13.350443 
lonf = 74.789508
global lati
global loni 
lati,loni=pos_update()
#plt.axis([13.347082, 74.789050, 13.350082, 74.802050])

latmin = lati - 0.001
lonmin = loni - 0.001
latmax = latf + 0.001
lonmax = lonf + 0.001

plt.axis([latmin, latmax, lonmin, lonmax])
plt.plot(lati,loni,marker='o',markersize=5, color='blue')
plt.plot(latf,lonf,marker='o',markersize=5, color='red')

while True:
    for event in pg.event.get():
            if event.type == pg.QUIT:
                break
    lati,loni=pos_update()
    angle,distance=get_heading()
    print(lati,loni,angle,distance)
    xs.append(lati)
    ys.append(loni)
    pg.display.set_caption(
                'distance {:.2f} angle {:.2f} '.format(
                    distance, angle))
    # Rotate the image and get a new rect.
    player_rotated = pg.transform.rotozoom(player_img, -angle, 1)
    player_rect = player_rotated.get_rect(center=player_rect.center)

    screen.fill((30, 30, 30))
    screen.blit(player_rotated, player_rect)
    pg.display.flip()
    clock.tick(60)
    #latitude = float(lat)
    #longitude = float(lon)

    plt.plot(lati,loni,marker='o',markersize=3, color='green')
    plt.draw()
    plt.pause(0.001)
plt.show()
