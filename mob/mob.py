from settings import *

import main
import pygame
import math
import mob


class Mob:
    icon_states = {
        "": (0, 0)
    }
    x_offset = 0
    y_offset = 0
    hitbox_size = (0, 0)

    def __init__(self, game, pos: tuple[int, int],
                 icon: str = "", icon_state: str = "", health: int = 100, angle: int = 0):
        self.x, self.y = pos
        if icon:
            self.icon = pygame.image.load(icon).convert_alpha()
        else:
            self.icon = None
        self.icon_state = icon_state
        self.health = health
        self.angle = angle
        self.game = game
        self.sprite = pygame.Surface((0, 0))
        self.hitbox = pygame.Surface((0, 0))
        self.hitbox_mask = pygame.Mask((0, 0))

    def process(self):
        self.update_sprite()

    @property
    def pos(self):
        return self.x, self.y

    def draw(self):
        self.game.screen.blit(self.sprite,
                              (HALF_WIDTH - (self.game.mobhandler.get_player.x - self.x * TILE),
                               HALF_HEIGHT - (self.game.mobhandler.get_player.y - self.y * TILE)))

    def update_sprite(self):
        self.sprite = pygame.Surface((TILE, TILE), pygame.SRCALPHA)
        self.hitbox = pygame.Surface(self.hitbox_size)
        self.hitbox.fill(RED)
        state = self.icon_states[self.icon_state]
        self.sprite.blit(self.icon, (0, 0), (state[0] * TILE, state[1] * TILE, TILE, TILE))
        self.hitbox_mask = pygame.mask.from_surface(self.hitbox)
        self.hitbox.set_colorkey(RED)

    def check_collisions(self):
        for i in self.game.turfhandler.world_map:
            turf = self.game.turfhandler.world_map[i]
            if (turf.hitbox_mask.overlap(self.hitbox_mask,
                                         (turf.x - self.x + self.x_offset, turf.y - self.y + self.y_offset))
                    and turf.impassible):
                return True
        return False


class MobHandler:
    def __init__(self, game):
        self.game = game
        self.mobs = list()

    def process(self):
        for mob in self.mobs:
            mob.process()

    def draw(self):
        for mob in self.mobs:
            mob.draw()

    def add_mob(self, mob: Mob):
        self.mobs.append(mob)

    def delete_mob(self, mob: Mob):
        self.mobs.remove(mob)

    @property
    def get_player(self):
        for i in self.mobs:
            if isinstance(i, mob.player.player.Player):
                return i
