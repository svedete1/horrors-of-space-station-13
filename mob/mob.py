from settings import *

import main
import pygame
import math
import mob


class Mob:
    def __init__(self, game, pos: tuple[int, int], icon: str = "", icon_state: str = "", health: int = 100, angle: int = 0):
        self.x, self.y = pos
        if icon:
            self.icon = pygame.image.load(icon).convert_alpha()
        else:
            self.icon = None
        self.icon_state = icon_state
        self.health = health
        self.angle = angle
        self.game = game

    def process(self):
        pass

    @property
    def pos(self):
        return (self.x, self.y)

    def draw(self, player_pos: tuple[int, int]):
        spr = self.get_sprite(0, 0)
        self.game.screen.blit(spr, spr.get_rect())

    def get_sprite(self, x: int, y: int):
        sprite = pygame.Surface((TILE, TILE), pygame.SRCALPHA)
        sprite.blit(self.icon, (0, 0), (x * TILE, y * TILE, TILE, TILE))
        return sprite


class MobHandler:
    def __init__(self, game):
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
