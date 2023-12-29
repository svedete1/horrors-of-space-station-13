import sys

from map import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(RES)
        self.clock = pygame.time.Clock()
        self.new_game()

    def new_game(self):
        self.map = Map(self)

    def update(self):
        pygame.display.flip()
        self.clock.tick(FPS)
        pygame.display.set_caption(f"{self.clock.get_fps():.1f}")

    def draw(self):
        self.screen.fill('black')
        self.map.draw()

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