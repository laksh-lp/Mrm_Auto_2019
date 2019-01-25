import pygame as pg
from pygame.math import Vector2
import pyproj
from gps3 import gps3


g = pyproj.Geod(ellps='WGS84')
gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()
def pos_update():
    while True:
        for new_data in gps_socket:
            if new_data:
                data_stream.unpack(new_data)
                global latitude,longitude
                latitude =  data_stream.TPV['lat']
                longitude =  data_stream.TPV['lon']
                if type(longitude) is type('sdas') or type(latitude) is type('sdas'):
                    continue                 
                #print(latitude,longitude)
                return latitude,longitude
        break  
def get_heading():
    startlat,startlong=pos_update()
    (az12, az21, dist) = g.inv(startlong, startlat, endlong, endlat)
    if az12<0:
        az12=az12+360
    return az12, dist
global startlat,startlong
startlat,startlong=pos_update()
global end_latitude,end_longitude
endlat=13.3463975   
endlong=74.7921200
def main():
    pg.init()
    screen = pg.display.set_mode((300, 300))
    clock = pg.time.Clock()
    player_img = pg.Surface((42, 70), pg.SRCALPHA)
    pg.draw.polygon(player_img, pg.Color('dodgerblue1'),
                    [(0, 70), (21, 2), (42, 70)])
    player_rect = player_img.get_rect(center=screen.get_rect().center)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        adjusted_angle,distance = get_heading()
        pg.display.set_caption(
            'angle {:.2f} distance {:.2f}'.format(
                adjusted_angle, distance))

        # Rotate the image and get a new rect.
        player_rotated = pg.transform.rotozoom(player_img, -adjusted_angle, 1)
        player_rect = player_rotated.get_rect(center=player_rect.center)

        screen.fill((30, 30, 30))
        screen.blit(player_rotated, player_rect)
        pg.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
    pg.quit()
