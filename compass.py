import pygame as pg
from pygame.math import Vector2
from magneto import get_imu_head

def main():
    pg.init()
    screen = pg.display.set_mode((300, 300))
    clock = pg.time.Clock()
    player_img = pg.Surface((42, 70), pg.SRCALPHA)
    pg.draw.polygon(player_img, pg.Color('white'),
                    [(0, 70), (21, 2), (42, 70)])
    player_rect = player_img.get_rect(center=screen.get_rect().center)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        adjusted_angle = get_imu_head()
        pg.display.set_caption(
            'angle {:.2f}'.format(
                adjusted_angle))

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
