from settings import *

import pygame
import math
import mobs


class Mob:
    icon_states = {
        "": (0, 0)
    }
    x_offset = 0
    y_offset = 0
    speed = 0.45

    def __init__(self, game, map_pos: tuple[int, int],
                 icon: str = "icon/mobs/mob.png", icon_state: str = "", health: int = 100, angle: int = 0):
        self.x, self.y = map_pos[0] * TILE, map_pos[1] * TILE
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
        self.moving = False
        self.moving_pos = (int(self.x / TILE), int(self.y / TILE))

    def process(self):
        self.update_sprite()

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x / TILE), int(self.y / TILE)

    def draw(self):
        self.game.screen.blit(self.sprite,
                              (HALF_WIDTH - (self.game.mobhandler.get_player.x - self.x),
                               HALF_HEIGHT - (self.game.mobhandler.get_player.y - self.y)))

    def update_sprite(self):
        self.sprite = pygame.Surface((TILE, TILE), pygame.SRCALPHA)
        state = self.icon_states[self.icon_state]
        self.sprite.blit(self.icon, (0, 0), (state[0] * TILE, state[1] * TILE, TILE, TILE))
        self.hitbox = pygame.mask.from_surface(self.sprite)

    def move(self, map_pos: tuple[int, int]):
        try:
            turf = self.game.turfhandler.world_map[map_pos].impassible
        except KeyError:
            print("MOB in empty space!")
            turf = False
        if not self.moving and not turf:
            self.moving_pos = map_pos
            self.moving = True
            return True
        return False

    def movement(self):
        if (self.moving_pos[0] * TILE, self.moving_pos[1] * TILE) == self.pos:
            self.moving = False

        if self.moving:
            mov_angle = math.atan2(
                self.moving_pos[1] * TILE - self.y,
                self.moving_pos[0] * TILE - self.x
            )

            dx = self.speed * round(math.cos(mov_angle), 5) * self.game.delta_time
            dy = self.speed * round(math.sin(mov_angle), 5) * self.game.delta_time

            if (abs(self.moving_pos[0] * TILE - self.x) < abs(dx) or
                    abs(self.moving_pos[1] * TILE - self.y) < abs(dy)):
                self.x, self.y = self.moving_pos[0] * TILE, self.moving_pos[1] * TILE
                self.moving = False
            else:
                self.x += int(dx)
                self.y += int(dy)


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
            if isinstance(i, mobs.player.player.Player):
                return i
