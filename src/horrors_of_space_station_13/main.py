import logging
import sys

import pygame

from horrors_of_space_station_13.logging_setup import setup_logging
from horrors_of_space_station_13.renderer import Renderer
from horrors_of_space_station_13.settings import *

from .mobs import MobHandler
from .mobs.player import Player
from .mobs.smart import SmartMob
from .turfs import TurfHandler

logger = logging.getLogger(__name__)


class Game:
    def __init__(self):
        pygame.init()
        self._set_gl_attributes()
        self.screen = pygame.display.set_mode(RES, WINDOW_FLAGS)
        self.renderer = Renderer(WIDTH, HEIGHT)
        self.clock = pygame.time.Clock()
        self.delta_time = 1
        logger.info("Game initialized")
        self.new_game()

    @staticmethod
    def _set_gl_attributes():
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(
            pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE
        )

    def new_game(self):
        self.mobhandler = MobHandler(self)
        self.mobhandler.add_mob(
            Player(self, (1, 2), icon="src/horrors_of_space_station_13/icon/mobs/mob.png", icon_state="down")
        )
        self.mobhandler.add_mob(SmartMob(self, (1, 1)))
        self.turfhandler = TurfHandler(self)

    def update(self):
        self.delta_time = self.clock.tick(FPS)
        pygame.display.set_caption(f"{self.clock.get_fps():.1f}")
        self.turfhandler.process()
        self.mobhandler.process()

    def draw(self):
        self.renderer.begin()
        self.turfhandler.draw()
        self.mobhandler.draw()
        self.renderer.end()

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
    setup_logging()
    logger.info("Starting game")
    try:
        game = Game()
        game.run()
    except SystemExit:
        raise
    except Exception:
        logger.exception("Fatal error during game loop")
        raise
    finally:
        logger.info("Game stopped")
