import os

from pathlib import Path

import pygame

class Utils:

    @classmethod
    def getSurfaceListFromSpritesheets(cls, spritesheetsPath: Path) -> None:
        surfaceList = []
        for imageFilename in os.listdir(spritesheetsPath):
            pathToImage = spritesheetsPath / imageFilename
            surface = pygame.image.load(pathToImage).convert_alpha()
            surfaceList.append(surface)

        return surfaceList
