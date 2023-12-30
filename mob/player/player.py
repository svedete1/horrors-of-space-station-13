from settings import *

from mob import mob
import pygame
import math


class Player(mob.Mob):
    def process(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.y += -player_speed
        if keys[pygame.K_s]:
            self.y += player_speed
        if keys[pygame.K_a]:
            self.x += -player_speed
        if keys[pygame.K_d]:
            self.x += player_speed
        self.angle = self._get_mouse_angle()

    def draw(self, player_pos):
        pygame.draw.circle(self.game.screen, GREEN, (HALF_WIDTH, HALF_HEIGHT), 8.0)
        pygame.draw.line(self.game.screen, GREEN, (HALF_WIDTH, HALF_HEIGHT),
                         (HALF_WIDTH + WIDTH * math.cos(self._get_mouse_angle()),
                          HALF_HEIGHT + WIDTH * math.sin(self._get_mouse_angle())), 2)

    def _get_mouse_angle(self):
        m_x, m_y = pygame.mouse.get_pos()
        return math.atan2(m_y - HALF_HEIGHT, m_x - HALF_WIDTH)
