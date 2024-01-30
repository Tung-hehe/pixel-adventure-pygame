import random
import sys

from pathlib import Path

import numpy as np
import pygame

from .map import Map
from Source.Utils import (
    GameData,
    Utils
)

from Source.enums import (
    CharacterName,
    BackgroundName
)


class Game:

    def __init__(self) -> None:
        pygame.init()
        self.rootPath = Path(__file__).absolute().parents[2]
        settings = Utils.readJSONFile(self.rootPath/'Data/Settings.json')
        self.FPS = settings['FPS']
        screenWidth = settings['screenWidth']
        screenHeight = settings['screenHeight']
        self.screen = pygame.display.set_mode((screenWidth,screenHeight))
        self.data = GameData(self.rootPath)
        mapData = Utils.readJSONFile(self.rootPath/settings['startMapData'])
        for idx, layer in enumerate(mapData['layers']):
            mapData['layers'][idx]['data'] = np.loadtxt(
                self.rootPath/layer['path'], delimiter=',', dtype=int
            )
        self.map = Map(
            mapData=mapData,
            tilesetData=self.data.tilesets,
            playerData=self.data.characters[random.choice(list(CharacterName))],
            backgroundData=self.data.backgrounds[random.choice(list(BackgroundName))]
        )
        self.clock = pygame.time.Clock()

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
            self.map.update()
            self.map.draw(self.screen)

            pygame.display.update()
            self.clock.tick(self.FPS)
