import pytmx

from horrors_of_space_station_13.settings import *

from .floor import Floor
from .turf import Turf


class TurfHandler:
    def __init__(self, game, tmx_file="src/horrors_of_space_station_13/maps/test2.tmx"):
        self.game = game
        # self.mini_map = mini_map
        self.tmx_map = pytmx.TiledMap(tmx_file)
        self.gid_map = self.tmx_map.tiledgidmap
        self.world_map = {}
        self.get_map()
        self.path_map = []
        self.gen_path_map()

    def get_id(self, gid):
        return self.gid_map[gid] - 1

    def get_map(self):

        turfs = self.tmx_map.get_layer_by_name("turfs")

        for x in range(self.tmx_map.width):
            for y in range(self.tmx_map.height):
                if gid := turfs.data[y][x]:
                    gid_data = self.tmx_map.get_tile_properties_by_gid(gid)
                    if gid_data["icon_state"] in icon_states_walls:
                        self.world_map[(x, y)] = Turf(
                            self.game, (x, y), icon_state=gid_data["icon_state"]
                        )
                    elif gid_data["icon_state"] in icon_states_floors:

                        self.world_map[(x, y)] = Floor(
                            self.game, (x, y), icon_state=gid_data["icon_state"]
                        )

    def gen_path_map(self):
        self.path_map = []
        for y in range(self.tmx_map.height):
            temp_lst = []
            for x in range(self.tmx_map.width):
                if self.world_map[(x, y)].impassible:
                    temp_lst.append(None)
                else:
                    temp_lst.append((x, y))
            self.path_map.append(temp_lst)

    def process(self):
        for i in self.world_map:
            self.world_map[i].process()

    def draw(self):
        for i in self.world_map:
            self.world_map[i].draw()
