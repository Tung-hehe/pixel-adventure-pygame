import os

from pathlib import Path

import pygame

def getSurfaceList(path: Path) -> None:
    surfaceList = []

    for imageFilename in os.listdir(path):
        pathToImage = path / imageFilename
        surface = pygame.image.load(pathToImage).convert_alpha()
        surfaceList.append(surface)

    return surfaceList
