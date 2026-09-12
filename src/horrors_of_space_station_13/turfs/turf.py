
import pygame

from horrors_of_space_station_13.settings import *
from horrors_of_space_station_13.renderer import TextureManager

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
        self.texture = TextureManager.get(self.icon_path)
        self.icon = self.texture.surface
        self.sprite = None
        self.sprite_mask = None
        self.hitbox = None
        self.icon_state = icon_state
        self.update_sprite()

    def process(self):
        pass

    def draw(self):
        col, row = self.icon_states[self.icon_state]
        self.game.renderer.draw_tile(
            self.texture,
            HALF_WIDTH - (self.game.mobhandler.get_player.x - self.mx * TILE),
            HALF_HEIGHT - (self.game.mobhandler.get_player.y - self.my * TILE),
            col,
            row,
        )

    def update_sprite(self):
        self.sprite = pygame.Surface((TILE, TILE), pygame.SRCALPHA)
        state = self.icon_states[self.icon_state]
        self.sprite.blit(
            self.icon, (0, 0), (state[0] * TILE, state[1] * TILE, TILE, TILE)
        )
        self.hitbox = pygame.mask.from_surface(self.sprite)
