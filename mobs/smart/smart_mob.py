from settings import *

import pygame
import math
import mobs


class SmartMob(mobs.mob.Mob):
    # Здесь можно добавить переменные, которые будут идти как self.something
    # something = 'something'

    # __init__ не трогать

    # здесь работает логика моба, эта функция вызывается каждый кадр
    def process(self):
        # Код писать тут

        # НЕ ТРОГАТЬ ЭТО
        self.update_sprite()

    # Задача - добавить мобу возможность нахождения пути до точки на карте и добавить возможность движения к ней.
    # Передвинуть моба на тайл можно через self.move((0, 0)) (0, 0) - координаты тайла на карте
    # Моб должен передвигаться на соседний тайл
    # self.move занимает время, self.moving булевая переменная, показывает, в движении моб или нет
    # self.moving == True - двигается self.moving == False - стоит
    # Если при работе с world_map выдаёт KeyError это значит, что вы наткнулись на пустое пространство
    # обрабатывайте через try
    # self.game тут находится класс игры world_map брать оттуда
    def find_path(self, map_pos: tuple[int, int]):
        pass

    def move_to_map_pos(self, map_pos: tuple[int, int]):
        pass
