from settings import *

import pygame
import math

_ = False

mini_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, 1, 1, 1, 1, _, _, _, 1, 1, 1, _, _, 1],
    [1, _, _, _, _, _, 1, _, _, _, _, _, 1, _, _, 1],
    [1, _, _, _, _, _, 1, _, _, _, _, _, 1, _, _, 1],
    [1, _, _, 1, 1, 1, 1, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, 1, _, _, _, 1, _, _, _, _, _, _, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]


class Turf:
    def __init__(self, game, map_pos: tuple[int, int]):
        self.game = game
        self.mx, self.my = map_pos
        self.x, self.y = self.mx * TILE, self.my * TILE

    def process(self):
        pass

    def draw(self):
        pygame.draw.rect(self.game.screen, DARKGRAY,
                         (HALF_WIDTH - (self.game.mobhandler.get_player.x - self.mx * TILE),
                          HALF_HEIGHT - (self.game.mobhandler.get_player.y - self.my * TILE),
                          TILE, TILE), 2)


class TurfHandler:
    def __init__(self, game):
        self.game = game
        self.mini_map = mini_map
        self.world_map = []
        self.get_map()

    def get_map(self):
        for j, row in enumerate(self.mini_map):
            for i, value in enumerate(row):
                if value:
                    self.world_map.append(Turf(self.game, (i, j)))

    def process(self):
        pass

    def draw(self):
        for turf in self.world_map:
            turf.draw()

