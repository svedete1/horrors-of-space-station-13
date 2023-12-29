from settings import *

import pygame
import math


class Mob:
    def __init__(self, pos: tuple, icon: str="", icon_state: str="", health: int=100, angle: int=0):
        self.x, self.y = pos
        self.icon = icon
        self.icon_state = icon_state
        self.health = health
        self.angle = angle

    @property
    def pos(self):
        return (self.x, self.y)

    def draw(self, player_pos):
        pass
