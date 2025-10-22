from settings import *

import pygame
import math


class Effect:
    icon_states = {
        "": (0, 0),
    }
    icon_state = ""
    icon_path = ""

    def __init__(self, game, pos, angle, icon_path=""):
        self.game = game
        self.x, self.y = pos
        self.angle = angle
        self.icon_path = icon_path
        self.sprite = None
        self.sprite_mask = None
        self.hitbox = None
        self.hitbox_mask = None
    
    def process(self) -> None:
        pass

    def draw(self) -> None:
        pass

    def update_sprite(self) -> None:
        pass



class EffectHandler:

    def __init__(self, game):
        self.effects = list()
        self.game = game

    def process(self) -> None:
        for effect in self.effects:
            effect.process()

    
    def add_effect(self, effect:Effect) -> None:
        self.effects.append(effect)
    
    def remove_effect(self, effect:Effect) -> bool:
        try:
            self.effects.remove(effect)
        except ValueError:
            return False
        return True
