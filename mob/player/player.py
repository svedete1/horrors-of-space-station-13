from settings import *

from mob import mob
import pygame
import math

icon_states = {
    "down": (5, 14),
    "up": (6, 14),
    "right": (7, 14),
    "left": (8, 14)
}

class Player(mob.Mob):
    def process(self):
        speed = player_speed * self.game.delta_time
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()
        y_p = False; y_m = False; x_p = False; x_m = False
        if keys[pygame.K_w]:
            self.y += -speed
            y_m = True
        if keys[pygame.K_s]:
            self.y += speed
            y_p = True
        if keys[pygame.K_a]:
            self.x += -speed
            x_m = True
        if keys[pygame.K_d]:
            self.x += speed
            x_p = True
        self.angle = self._get_mouse_angle()

        # логика смены напрвления пресонажа из-за смены направления его движения
        if y_m and not y_p:
            self.icon_state = "up"
        elif y_p and not y_m:
            self.icon_state = "down"
        if x_p and not x_m:
            self.icon_state = "right"
        elif x_m and not x_p:
            self.icon_state = "left"

    def draw(self, player_pos: tuple[int, int]):
        # pygame.draw.circle(self.game.screen, GREEN, (HALF_WIDTH, HALF_HEIGHT), 8.0)
        spr = self.get_sprite(5, 14)
        self.game.screen.blit(spr, (HALF_WIDTH - 16, HALF_HEIGHT - 16))
        pygame.draw.line(self.game.screen, GREEN, (HALF_WIDTH, HALF_HEIGHT),
                         (HALF_WIDTH + WIDTH * math.cos(self._get_mouse_angle()),
                          HALF_HEIGHT + WIDTH * math.sin(self._get_mouse_angle())), 1)

    def get_sprite(self, x, y):
        sprite = pygame.Surface((TILE, TILE), pygame.SRCALPHA)
        state = icon_states[self.icon_state]
        sprite.blit(self.icon, (0, 0), (state[0] * TILE, state[1] * TILE, TILE, TILE))
        return sprite

    def _get_mouse_angle(self):
        m_x, m_y = pygame.mouse.get_pos()
        return math.atan2(m_y - HALF_HEIGHT, m_x - HALF_WIDTH)
