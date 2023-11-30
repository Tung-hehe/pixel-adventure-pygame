from pathlib import Path

import pygame

from .utils import Utils
from Source.enums import (
    CharacterNames,
    CharacterStatus
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


class Assets:

    def __init__(self, rootPath: Path) -> None:
        self.characters = self.getAllCharacterAssets(rootPath)
        return None

    def getAllCharacterAssets(self, rootPath: Path) -> dict[CharacterNames, CharacterAssets]:
        characterAssets = {
            characterName: CharacterAssets(
                spriteWidth=32,
                spriteHeight=32,
                spriteScale=2,
                spritesheetsFolderPath=rootPath/f'Assets/Image/MainCharacters/{characterName.value}',
            ) for characterName in CharacterNames
        }
        return characterAssets
