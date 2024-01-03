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

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == "__main__":
    game = Game()
    game.run()

# old code
'''
if __name__ == "__main__":
    pygame.init()
    sc = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    player = Player()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        player.movement()
        sc.fill(BLACK)

        pygame.draw.circle(sc, GREEN, (HALF_WIDTH, HALF_HEIGHT), 12)
        pygame.draw.line(sc, GREEN, (HALF_WIDTH, HALF_HEIGHT), (HALF_WIDTH + WIDTH * math.cos(player.angle),
                                                                HALF_HEIGHT + WIDTH * math.sin(player.angle)), 2)
        for x, y in world_map:
            # pygame.draw.rect(sc, DARKGRAY, (x, y, TILE, TILE), 2)
            pygame.draw.rect(sc, DARKGRAY, (HALF_WIDTH - (player.x - x), HALF_HEIGHT - (player.y - y), TILE, TILE), 2)

        pygame.display.flip()
        clock.tick(FPS)
'''