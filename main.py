import sys

from pathlib import Path

import pygame


class PythonPath():
    def __init__(self, path: Path):
        self.path = path

    def __enter__(self):
        sys.path.insert(0, self.path)

    def __exit__(self, exc_type, exc_value, traceback):
        sys.path.remove(self.path)

with PythonPath(Path(__file__).absolute().parents[1]):
    from Source import Level
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
    'XXXXXXXXXXXXXX']

    tileSize = (64, 64)

    screenWidth = len(map[0]) * tileSize[0]
    screenHeight = len(map) * tileSize[1]

    # Pygame setup
    pygame.init()
    screen = pygame.display.set_mode((screenWidth,screenHeight))
    clock = pygame.time.Clock()
    level = Level(map, tileSize)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        screen.fill('black')
        level.update(screen)

        pygame.display.update()
        clock.tick(60)
