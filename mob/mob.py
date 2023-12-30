from settings import *

from main import Game
import pygame
import math
import mob


class Mob:
    def __init__(self, game: Game, pos: tuple, icon: str="", icon_state: str="", health: int=100, angle: int=0):
        self.x, self.y = pos
        self.icon = icon
        self.icon_state = icon_state
        self.health = health
        self.angle = angle
        self.game = game

    def process(self):
        pass

    @property
    def pos(self):
        return (self.x, self.y)

    def draw(self, player_pos):
        pass


class MobHandler:
    def __init__(self, game: Game):
        self.game = game
        self.mobs = list()

    def process(self):
        for mob in self.mobs:
            mob.process()

    def draw(self):
        for mob in self.mobs:
            mob.draw(self.game.mobhandler.get_player.pos)

    def add_mob(self, mob: Mob):
        self.mobs.append(mob)

    def delete_mob(self, mob: Mob):
        self.mobs.remove(mob)

    @property
    def get_player(self):
        for i in self.mobs:
            if isinstance(i, mob.player.player.Player):
                return i
