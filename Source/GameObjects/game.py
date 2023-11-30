import random
import sys

from pathlib import Path

import pygame

from .map import Map
from Source.Utils import (
    Settings, Assets
)
from Source.enums import CharacterNames


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

        self.rootPath = Path(__file__).absolute().parents[2]
        self.settings = Settings()
        self.assets = Assets(self.rootPath)

        self.clock = pygame.time.Clock()
        playerSettings = self.settings.characters[random.choice(list(CharacterNames))]
        playerAssets = self.assets.characters[random.choice(list(CharacterNames))]
        self.map = Map(map, tileSize, playerSettings=playerSettings, playerAssets=playerAssets)

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
            self.map.update(self.screen)

            pygame.display.update()
            self.clock.tick(60)
