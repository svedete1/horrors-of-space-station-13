from settings import *

import pygame
import math
import pytmx

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
    [1, 1, 1, 1, 1, 1, _, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]


class Turf:
    impassible = True
    hitbox_size = (TILE, TILE)
    icon_path = "icon/turfs/wall.png"
    icon_states = {
        "": (0, 0),
        "steel": (1, 0),
        "reinforced": (0, 1),
        "corrupted": (0, 0)
    }
    icon_state = ""

    def __init__(self, game, map_pos: tuple[int, int]):
        self.game = game
        self.mx, self.my = map_pos
        self.x, self.y = self.mx * TILE, self.my * TILE
        self.icon = pygame.image.load(self.icon_path).convert_alpha()
        self.sprite = None
        self.sprite_mask = None
        self.hitbox = None

    def process(self):
        self.update_sprite()

    def draw(self):
        self.game.screen.blit(self.sprite,
                              (HALF_WIDTH - (self.game.mobhandler.get_player.x - self.mx * TILE),
                               HALF_HEIGHT - (self.game.mobhandler.get_player.y - self.my * TILE)))

    def update_sprite(self):
        self.sprite = pygame.Surface((TILE, TILE), pygame.SRCALPHA)
        state = self.icon_states[self.icon_state]
        self.sprite.blit(self.icon, (0, 0), (state[0] * TILE, state[1] * TILE, TILE, TILE))
        self.hitbox = pygame.mask.from_surface(self.sprite)


class TurfHandler:
    def __init__(self, game, tmx_file='maps/test.tmx'):
        self.game = game
        # self.mini_map = mini_map
        self.tmx_map = pytmx.TiledMap(tmx_file)
        self.gid_map = self.tmx_map.tiledgidmap
        self.world_map = {}
        self.get_map()

    def get_id(self, gid):
        return self.gid_map[gid] - 1

    def get_map(self):

        turfs = self.tmx_map.get_layer_by_name('turfs')

        for x in range(self.tmx_map.width):
            for y in range(self.tmx_map.height):

                if gid := turfs.data[y][x]:
                    if gid == 1:
                        self.world_map[(x, y)] = Turf(self.game, (x, y))
                    elif gid == 2:
                        from turfs.floor.floor import TiledFloor
                        self.world_map[(x, y)] = TiledFloor(self.game, (x, y))

    def process(self):
        for i in self.world_map:
            self.world_map[i].process()

    def draw(self):
        for i in self.world_map:
            self.world_map[i].draw()
