import pygame
from pathlib import Path

from .utils import Utils
from Source.enums import (
    CharacterNames,
    CharacterStatus
)


class CharacterSettings:
    def __init__(self,
            runSpeed: float,
            fallSpeed: float,
            jumpSpeed: float,
            hitboxWidth: int,
            hitboxHeight: int,
            animationSpeed: float,
        ) -> None:
        self.runSpeed = runSpeed
        self.fallSpeed = fallSpeed
        self.jumpSpeed = jumpSpeed
        self.hitboxWidth = hitboxWidth
        self.hitboxHeight = hitboxHeight
        self.animationSpeed = animationSpeed
        return None


class Settings:

    def __init__(self):
        self.characters = self.getAllCharacterSettings()
        return None

    def getAllCharacterSettings(self) -> dict[CharacterNames, CharacterSettings]:
        characterSettings = {
            characterName: CharacterSettings(
                runSpeed=5,
                fallSpeed=0.8,
                jumpSpeed=-16,
                hitboxWidth=40,
                hitboxHeight=50,
                animationSpeed=0.25,
            ) for characterName in CharacterNames
        }
        return characterSettings
