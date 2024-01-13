from settings import *

import turfs
import pygame
import math


class Floor(turfs.turf.Turf):
    impassible = False
    icon_path = icon_floors
    icon_states = icon_states_floors

