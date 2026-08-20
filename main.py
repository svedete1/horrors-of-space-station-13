import sys

from settings import *
import pygame
from mobs.player import player
import mobs
from mobs.smart import smart_mob
from turfs import turf


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(RES)
        self.clock = pygame.time.Clock()
        self.delta_time = 1
        self.new_game()

    def new_game(self):
        self.mobhandler = mobs.mob.MobHandler(self)
        self.mobhandler.add_mob(player.Player(self, (1, 2),
                                              icon="icon/mobs/mob.png", icon_state="down"))
        self.mobhandler.add_mob(smart_mob.SmartMob(self, (1, 1)))
        self.turfhandler = turf.TurfHandler(self)

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
                sys.exit()
        keys = pygame.key.get_pressed()
        if not self.mobhandler.mobs[1].moving:
            if keys[pygame.K_k]:
                self.mobhandler.mobs[1].patrol([(28, 11), (2, 14), (17, 4)])

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == "__main__":
    game = Game()
    game.run()
