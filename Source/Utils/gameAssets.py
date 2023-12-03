from pathlib import Path

import pygame

from .utils import Utils
from Source.enums import (
    CharacterName,
    CharacterStatus,
    TilesetName,
    BackgroundName
)


class CharacterAssets:

    def __init__(self, width: int, height: int, scale: int, spritesheetsFolderPath: Path, ) -> None:
        self.animations = self.getAnimations(spritesheetsFolderPath, width, height, scale)
        # NOTE. Add sound effect here
        self.sound = {}
        return None

    def getAnimations(self,
            spritesheetsFolderPath: Path, width: int, height: int, scale: int
        ) -> dict[CharacterStatus, list[pygame.Surface]]:
        animations = {status: [] for status in CharacterStatus}
        for status in animations.keys():
            spritesheetPath = spritesheetsFolderPath / f'{status.value}.png'
            animations[status] = Utils.getSurfaceListFromSpritesheets(
                spritesheetsPath=spritesheetPath,
                width=width,
                height=height,
                scale=scale
            )
        return animations


class TilesetAssets:

    def __init__(self, width: int, height: int, scale: int, tilesetFolderPath: Path) -> None:
        self.surfaces = Utils.getSurfaceListFromTileset(
            tilesetPath=tilesetFolderPath, width=width, height=height, scale=scale
        )
        return None


class BackgroundAssets:

    def __init__(self, backgroundFolderPath: Path, scale: int) -> None:
        backgroundImage = pygame.image.load(backgroundFolderPath).convert_alpha()
        width = backgroundImage.get_width()
        height = backgroundImage.get_height()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
        self.image.blit(backgroundImage, (0, 0), (0, 0, width, height))
        if scale > 1:
            self.image = pygame.transform.scale(self.image, (width*scale, height*scale))
        return None


class Assets:

    def __init__(self, rootPath: Path) -> None:
        self.characters = self.getAllCharacterAssets(rootPath)
        self.tilesets = self.getAllTilesetAssets(rootPath)
        self.backgrounds = self.getAllBackgroundAssets(rootPath)
        return None

    def getAllCharacterAssets(self, rootPath: Path) -> dict[CharacterName, CharacterAssets]:
        charactersAssets = {
            characterName: CharacterAssets(
                width=32,
                height=32,
                scale=2,
                spritesheetsFolderPath=rootPath/f'Assets/Image/MainCharacters/{characterName.value}',
            ) for characterName in CharacterName
        }
        return charactersAssets

    def getAllTilesetAssets(self, rootPath: Path) -> dict[TilesetName, TilesetAssets]:
        tilesetsAssets = {
            tilesetName: TilesetAssets(
                width=32,
                height=32,
                scale=1,
                tilesetFolderPath=rootPath/f'Assets/Image/Tilesets/{tilesetName.value}.png',
            ) for tilesetName in TilesetName
        }
        return tilesetsAssets

    def getAllBackgroundAssets(self, rootPath: Path):
        backgroundsAssets = {
            backgroundName: BackgroundAssets(
                backgroundFolderPath=rootPath/f'Assets/Image/Background/{backgroundName.value}.png', scale=2
            ) for backgroundName in BackgroundName
        }
        return backgroundsAssets
