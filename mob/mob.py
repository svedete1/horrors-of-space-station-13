from settings import *

from main import Game
import pygame
import math


class Mob:
    def __init__(self, game: Game, pos: tuple, icon: str="", icon_state: str="", health: int=100, angle: int=0):
        self.x, self.y = pos
        self.icon = icon
        self.icon_state = icon_state
        self.health = health
        self.angle = angle
        self.game = game

    @property
    def pos(self):
        return (self.x, self.y)

    def draw(self, player_pos):
        pass
