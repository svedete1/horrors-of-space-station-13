import logging

from .mob import Mob
from .player import Player


class MobHandler:
    def __init__(self, game):
        self.game = game
        self.mobs = []
        self.logger = logging.getLogger(__name__)
        self.logger.info("Mobhandler initialized")

    def process(self) -> None:
        for mob in self.mobs:
            mob.process()

    def draw(self) -> None:
        for mob in self.mobs:
            mob.draw()

    def add_mob(self, mob: Mob) -> None:
        self.mobs.append(mob)

    def delete_mob(self, mob: Mob) -> bool:
        try:
            self.mobs.remove(mob)
        except ValueError:
            return False
        return True

    @property
    def get_player(self):
        for i in self.mobs:
            if isinstance(i, Player):
                return i
