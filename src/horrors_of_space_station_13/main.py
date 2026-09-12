import sys

import pygame

from horrors_of_space_station_13.settings import *

from .mobs import Mob, MobHandler
from .mobs.player import Player
from .mobs.smart import SmartMob
from .turfs import TurfHandler


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(RES)
        self.clock = pygame.time.Clock()
        self.delta_time = 1
        self.new_game()

    def new_game(self):
        self.mobhandler = MobHandler(self)
        self.mobhandler.add_mob(
            Player(self, (1, 2), icon="src/horrors_of_space_station_13/icon/mobs/mob.png", icon_state="down")
        )
        self.mobhandler.add_mob(SmartMob(self, (1, 1)))
        self.turfhandler = TurfHandler(self)

    def update(self):
        pygame.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pygame.display.set_caption(f"{self.clock.get_fps():.1f}")
        self.turfhandler.process()
        self.mobhandler.process()

    def draw(self):
        self.screen.fill(BLACK)
        self.turfhandler.draw()
        self.mobhandler.draw()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        keys = pygame.key.get_pressed()
        if not self.mobhandler.mobs[1].moving and keys[pygame.K_k]:
            self.mobhandler.mobs[1].patrol([(28, 11), (2, 14), (17, 4)])

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


def main():
    game = Game()
    game.run()
