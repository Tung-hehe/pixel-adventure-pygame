from pathlib import Path

import pygame

from .utils import Utils
from Source.enums import (
    CharacterNames,
    CharacterStatus,
    TilesetNames
)


class CharacterAssets:

    def __init__(self,
            spriteWidth: int,
            spriteHeight: int,
            spriteScale: int,
            spritesheetsFolderPath: Path,
        ) -> None:
        self.animations = self.getAnimations(
            spritesheetsFolderPath,
            spriteWidth,
            spriteHeight,
            spriteScale,
        )
        # NOTE. Add sound effect here
        self.sound = {}
        return None

    def getAnimations(self,
            spritesheetsFolderPath: Path,
            spriteWidth: int,
            spriteHeight: int,
            spriteScale: int
        ) -> dict[CharacterStatus, list[pygame.Surface]]:
        animations = {status: [] for status in CharacterStatus}
        for status in animations.keys():
            spritesheetPath = spritesheetsFolderPath / f'{status.value}.png'
            animations[status] = Utils.getSurfaceListFromSpritesheets(
                spritesheetsPath=spritesheetPath,
                width=spriteWidth,
                height=spriteHeight,
                scale=spriteScale
            )
        return animations


class TilesetAssets:
    def __init__(self,
            tileWidth: int,
            tileHeight: int,
            tileScale: int,
            tilesetFolderPath: Path,
        ) -> None:
        self.surfaces = Utils.getSurfaceListFromTileset(
            tilesetPath=tilesetFolderPath, width=tileWidth, height=tileHeight, scale=tileScale
        )
        return None


class Assets:

    def __init__(self, rootPath: Path) -> None:
        self.characters = self.getAllCharacterAssets(rootPath)
        self.tileset = self.getAllTilesetAssets(rootPath)
        return None

    def getAllCharacterAssets(self, rootPath: Path) -> dict[CharacterNames, CharacterAssets]:
        charactersAssets = {
            characterName: CharacterAssets(
                spriteWidth=32,
                spriteHeight=32,
                spriteScale=2,
                spritesheetsFolderPath=rootPath/f'Assets/Image/MainCharacters/{characterName.value}',
            ) for characterName in CharacterNames
        }
        return charactersAssets

    def getAllTilesetAssets(self, rootPath: Path) -> TilesetAssets:
        tilesetsAssets = {
            tilesetName: TilesetAssets(
                tileWidth=32,
                tileHeight=32,
                tileScale=2,
                tilesetFolderPath=rootPath/f'Assets/Image/Tilesets/{tilesetName.value}.png',
            ) for tilesetName in TilesetNames
        }
        return tilesetsAssets
