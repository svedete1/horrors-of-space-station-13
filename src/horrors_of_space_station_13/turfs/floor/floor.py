from horrors_of_space_station_13.settings import *

from .. import Turf


class Floor(Turf):
    impassible = False
    icon_path = icon_floors
    icon_states = icon_states_floors
