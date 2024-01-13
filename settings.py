import math

# game settings
WIDTH, HEIGHT = RES = (1200, 700)
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FPS = 0
TILE = 32


# player settings
player_angle = 0
player_speed = 0.4

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 0, 0)
GREEN = (0, 220, 0)
BLUE = (0, 0, 255)
DARKGRAY = (40, 40, 40)
PURPLE = (120, 0, 120)

# icons
icon_walls = "icon/turfs/wall.png"
icon_states_walls = {
        "no_texture": (0, 0),
        "steel": (1, 0),
        "reinforced": (0, 1),
        "corrupted": (1, 1)
}

icon_floors = "icon/turfs/tiles.png"
icon_states_floors = {
    "": (0, 0),
    "gray": (1, 0),
    "gray_rough": (2, 0),
    "gray_rough2": (3, 0),
    "gray2": (4, 0),
    "gray_plain_rough": (5, 0),
    "reinforced": (0, 1),
    "gray_rough_dirty": (1, 1),
    "gray_dirty": (2, 1),
    "gray_rough_dark": (3, 1),
    "gray_dark": (4, 1),
    "gray_plain_dark": (5, 1),
    "white_rough": (0, 2),
    "white": (1, 2),
    "white_plain_rough": (2, 2),
    "kitchen": (3, 2),
    "corrupted": (4, 2),
    "white_plain": (5, 2),

}
