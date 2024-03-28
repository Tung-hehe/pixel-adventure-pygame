from pathlib import Path

import pygame

from .utils import Utils
from Source.enums import (
    CharacterName,
    CharacterStatus,
    TilesetName,
    BackgroundName
)


class CharacterData:

    def __init__(self,
            rootPath: Path,
            characterName: CharacterName,
            commonCharatersSetting: dict[str, dict]
        ) -> None:
        dataDict = Utils.readJSONFile(rootPath/f'Data/Characters/{characterName.value}.json')
        for k, v in dataDict['settings'].items():
            setattr(self, k, v)
        for k, v in commonCharatersSetting['settings'].items():
            if k not in dataDict['settings'].keys():
                setattr(self, k, v)
        self.createAnimations(rootPath, dataDict['assets']['animations'])
        return None

    def createAnimations(self, rootPath: Path, animationData: dict) -> None:
        self.animations = {status: [] for status in CharacterStatus}
        for status in self.animations.keys():
            path = rootPath / animationData['path'] / f'{status.value}.png'
            self.animations[status] = Utils.getSurfaceListFromSpritesheets(
                path=path,
                width=animationData['width'],
                height=animationData['height'],
                scale=animationData['scale']
            )
        return None


class TilesetData:

    def __init__(self, rootPath: Path, tilesetName: TilesetName) -> None:
        dataDict = Utils.readJSONFile(rootPath/f'Data/Tilesets/{tilesetName.value}.json')
        dataDict['path'] = rootPath / dataDict['path']
        self.surfaces = Utils.getSurfaceListFromTileset(**dataDict)
        return None


class BackgroundData:

    def __init__(self, rootPath: Path, backgroundName: BackgroundName, dataDict: dict[str, dict]) -> None:
        self.createImage(rootPath, backgroundName, dataDict['image'])
        for k, v in dataDict['setting'].items():
            setattr(self, k, v)
        self.width = dataDict['image']['width'] * dataDict['image']['scale']
        self.height = dataDict['image']['height'] * dataDict['image']['scale']
        return None

    def createImage(self, rootPath: Path, backgroundName: BackgroundName,imageData: dict) -> None:
        backgroundImage = pygame.image.load(
            rootPath/f'Assets/Image/Background/{backgroundName.value}.png'
        ).convert_alpha()
        self.image = pygame.Surface((imageData['width'], imageData['height']), pygame.SRCALPHA).convert_alpha()
        self.image.blit(backgroundImage, (0, 0), (0, 0, imageData['width'], imageData['height']))
        if imageData['scale'] > 1:
            self.image = pygame.transform.scale(
                self.image, (imageData['width']*imageData['scale'], imageData['height']*imageData['scale'])
            )
        return None


class GameData:

    def __init__(self, rootPath: Path) -> None:
        commonCharatersSetting = Utils.readJSONFile(rootPath/f'Data/Characters/Common.json')
        self.characters = {
            characterName: CharacterData(rootPath, characterName, commonCharatersSetting)
            for characterName in CharacterName
        }
        self.tilesets = {
            tilesetName: TilesetData(rootPath, tilesetName)
            for tilesetName in TilesetName
        }
        backgroundSettings = Utils.readJSONFile(rootPath/f'Data/Backgrounds.json')
        self.backgrounds = {
            backgroundName: BackgroundData(rootPath, backgroundName, backgroundSettings)
            for backgroundName in BackgroundName
        }
        return None
