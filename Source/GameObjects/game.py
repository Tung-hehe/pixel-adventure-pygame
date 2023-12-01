import random
import sys

from pathlib import Path

import pygame

from .map import Map
from Source.Utils import (
    Settings,
    Assets
)
from Source.enums import (
    CharacterName,
    TilesetName,
    BackgroundName
)


class Game:

    def __init__(self) -> None:
        map = [
            'XXXXXXXXXXXXXXXX',
            'X              X',
            'X              X',
            'X XX    XXX    X',
            'X XX           X',
            'X XXXX         X',
            'X XXXX       XXX',
            'X XX    X  XXXXX',
            'X       X  XXXXX',
            'X  P XXXXXXXXXXX',
            'XXXXXXXXXXXXXXXX'
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
        characterName = random.choice(list(CharacterName))
        playerAssets = self.assets.characters[characterName]
        playerSettings = self.settings.characters[characterName]

        backgroundName = random.choice(list(BackgroundName))
        backgroundAssets = self.assets.backgrounds[backgroundName]
        backgroundSettings = self.settings.backgrounds[backgroundName]

        self.map = Map(
            map=map,
            playerSettings=playerSettings,
            playerAssets=playerAssets,
            tilesetAssets=self.assets.tilesets[TilesetName.Terrain],
            backgroundAssets=backgroundAssets,
            backgroundSettings=backgroundSettings,
        )

    def run(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            self.map.update(self.screen)

            pygame.display.update()
            self.clock.tick(60)
