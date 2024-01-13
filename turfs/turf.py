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
    icon_path = icon_walls
    icon_states = icon_states_walls

    def __init__(self, game, map_pos: tuple[int, int], icon_state=""):
        self.game = game
        self.mx, self.my = map_pos
        self.x, self.y = self.mx * TILE, self.my * TILE
        self.icon = pygame.image.load(self.icon_path).convert_alpha()
        self.sprite = None
        self.sprite_mask = None
        self.hitbox = None
        self.icon_state = icon_state
        self.update_sprite()

    def process(self):
        pass

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
    def __init__(self, game, tmx_file='maps/test2.tmx'):
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
                    gid_data = self.tmx_map.get_tile_properties_by_gid(gid)
                    if gid_data['icon_state'] in icon_states_walls:
                        self.world_map[(x, y)] = Turf(self.game, (x, y), icon_state=gid_data['icon_state'])
                    elif gid_data['icon_state'] in icon_states_floors:
                        from turfs.floor.floor import Floor
                        self.world_map[(x, y)] = Floor(self.game, (x, y), icon_state=gid_data['icon_state'])

    def process(self):
        for i in self.world_map:
            self.world_map[i].process()

    def draw(self):
        for i in self.world_map:
            self.world_map[i].draw()
