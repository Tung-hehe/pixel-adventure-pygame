import sys

import pygame

from .map import Map


class Game:

    def __init__(self):
        map = [
            '              ',
            '              ',
            '              ',
            ' XX    XXX    ',
            ' XX           ',
            ' XXXX         ',
            ' XXXX       XX',
            ' XX    X  XXXX',
            '       X  XXXX',
            '  P XXXXXXXXXX',
            'XXXXXXXXXXXXXX'
        ]
        tileSize = (64, 64)
        screenWidth = len(map[0]) * tileSize[0]
        screenHeight = len(map) * tileSize[1]
        pygame.init()
        self.screen = pygame.display.set_mode((screenWidth,screenHeight))
        self.clock = pygame.time.Clock()
        self.level = Map(map, tileSize)

    def loadTileset(self):
        pass

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            self.screen.fill('black')
            self.level.update(self.screen)

            pygame.display.update()
            self.clock.tick(60)
