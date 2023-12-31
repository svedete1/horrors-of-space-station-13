from settings import *

from mob import mob
import pygame
import math


class Player(mob.Mob):
    icon_states = {
        "": (0, 0),
        "down": (5, 14),
        "up": (6, 14),
        "right": (7, 14),
        "left": (8, 14)
    }
    x_offset = 27
    y_offset = 16
    y_p = False
    y_m = False
    x_p = False
    x_m = False
    hitbox_size = (8, 29)

    def process(self):
        # логика смены напрвления пресонажа из-за смены направления его движения
        if self.y_m and not self.y_p:
            self.icon_state = "up"
        elif self.y_p and not self.y_m:
            self.icon_state = "down"
        if self.x_p and not self.x_m:
            self.icon_state = "right"
        elif self.x_m and not self.x_p:
            self.icon_state = "left"

        self.update_sprite()

        dx = 0
        dy = 0
        speed = player_speed * self.game.delta_time
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()
        self.x_p = False
        self.x_m = False
        self.y_p = False
        self.y_m = False
        if keys[pygame.K_w]:
            self.y += -speed
            dy += -speed
            self.y_m = True
        if keys[pygame.K_s]:
            self.y += speed
            dy += speed
            self.y_p = True
        if keys[pygame.K_a]:
            self.x += -speed
            dx += -speed
            self.x_m = True
        if keys[pygame.K_d]:
            self.x += speed
            dx += speed
            self.x_p = True
        self.angle = self._get_mouse_angle()

        if self.check_collisions():
            self.x -= dx
            self.update_sprite()
            if self.check_collisions():
                self.x += dx
                self.y -= dy
                self.update_sprite()
                if self.check_collisions():
                    self.x -= dx
                    self.update_sprite()
                    if self.check_collisions():
                        self.x += dx
                        self.y += dy
                        self.update_sprite()

        self.update_sprite()

    def draw(self):
        # pygame.draw.circle(self.game.screen, GREEN, (HALF_WIDTH, HALF_HEIGHT), 8.0)
        self.game.screen.blit(self.sprite, (HALF_WIDTH - 16, HALF_HEIGHT - 16))
        self.game.screen.blit(self.hitbox, (HALF_WIDTH - 4, HALF_HEIGHT - 13))
        pygame.draw.line(self.game.screen, GREEN, (HALF_WIDTH, HALF_HEIGHT),
                         (HALF_WIDTH + WIDTH * math.cos(self._get_mouse_angle()),
                          HALF_HEIGHT + WIDTH * math.sin(self._get_mouse_angle())), 1)

    '''
    def check_collisions(self):
        for wall in self.game.turfhandler.world_map:
            if wall.sprite_mask.overlap(self.sprite_mask, (wall.x - self.x + 16, wall.y - self.y + 16)):
                print("COLLISION!")
    '''

    def _get_mouse_angle(self):
        m_x, m_y = pygame.mouse.get_pos()
        return math.atan2(m_y - HALF_HEIGHT, m_x - HALF_WIDTH)
