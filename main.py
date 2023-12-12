import pygame
from settings import *
from player import Player
import math
from map import world_map

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
