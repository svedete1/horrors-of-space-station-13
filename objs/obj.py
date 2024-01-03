from settings import *

import pygame
import math


class Obj:
    impassible = False
    hitbox_size = (TILE, TILE)
    icon_path = ""
    icon_states = {
        "": (0, 0),
    }
    icon_state = ""

    def __init__(self, game, pos):
        self.game = game
        self.x, self.y = pos
        self.sprite = None
        self.sprite_mask = None
        self.hitbox = None
        self.hitbox_mask = None


class ObjHandler:
    def __init__(self):
        pass
