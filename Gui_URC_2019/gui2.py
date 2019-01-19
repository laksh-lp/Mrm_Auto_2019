import pygame as pg
from pygame.math import Vector2


def main():
    pg.init()
    screen = pg.display.set_mode((300, 300))
    clock = pg.time.Clock()
    player_img = pg.Surface((42, 70), pg.SRCALPHA)
    pg.draw.polygon(player_img, pg.Color('dodgerblue1'),
                    [(0, 70), (21, 2), (42, 70)])
    player_rect = player_img.get_rect(center=screen.get_rect().center)

    joysticks = [pg.joystick.Joystick(x) for x in range(pg.joystick.get_count())]
    for joystick in joysticks:
        joystick.init()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        if len(joysticks) > 0:  # At least one joystick.
            # Use the stick axes to create a vector.
            vec = Vector2(joysticks[0].get_axis(0), joysticks[0].get_axis(1))
            radius, angle = vec.as_polar()  # angle is between -180 and 180.
            # Map the angle that as_polar returns to 0-360 with 0 pointing up.
            adjusted_angle = (angle+90) % 360
            pg.display.set_caption(
                'radius {:.2f} angle {:.2f} adjusted angle {:.2f}'.format(
                    radius, angle, adjusted_angle))

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
