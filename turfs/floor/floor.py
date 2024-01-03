from settings import *

import turfs
import pygame
import math


class Floor(turfs.turf.Turf):
    impassible = False
    icon_path = "icon/turfs/tiles.png"


class TiledFloor(Floor):
    icon_states = {
        "": (0, 0),
        "tiled floor": (1, 0)
    }
    icon_state = "tiled floor"
