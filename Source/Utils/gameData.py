from pathlib import Path

import pygame

from .utils import Utils
from Source.enums import (
    BackgroundName,
    CharacterName,
    CharacterStatus,
    EffectName,
    FruitName,
    TilesetName,
)


class EffectData:

    def __init__(self,
            rootPath: Path,
            effectData: dict[str, dict]
        ) -> None:
        self.animation = Utils.getSurfaceListFromSpritesheets(
            path=rootPath / effectData['animation']['path'],
            width=effectData['animation']['width'],
            height=effectData['animation']['height'],
            scale=effectData['animation']['scale']
        )
        self.setting = effectData['setting']
        return None


class CharacterData:

    def __init__(self,
            rootPath: Path,
            characterName: CharacterName,
            commonCharatersSetting: dict[str, dict],
        ) -> None:
        dataDict = Utils.readJSONFile(rootPath/f'Data/Characters/{characterName.value}.json')
        for k, v in commonCharatersSetting['assets']['animations'].items():
            if k not in dataDict['assets']['animations'].keys():
                dataDict['assets']['animations'][k] = v
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

class FruitData:

    def __init__(self,
            rootPath: Path,
            fruitName: FruitName,
            fruitData: dict[str, dict]
        ) -> None:
        self.animation = Utils.getSurfaceListFromSpritesheets(
            path=rootPath / f'Assets/Image/Items/Fruits/{fruitName.value}.png',
            width=fruitData['width'],
            height=fruitData['height'],
            scale=fruitData['scale']
        )
        self.animationSpeed = fruitData['animationSpeed']
        self.hitbox = fruitData['hitbox']
        return None


class GameData:

    def __init__(self, rootPath: Path) -> None:
        self.characters = self.getCharacterData(rootPath=rootPath)
        self.tilesets = self.getTilesetData(rootPath=rootPath)
        self.backgrounds = self.getBackgroundData(rootPath=rootPath)
        self.fruits = self.getFruitData(rootPath=rootPath)
        self.effects = self.getEffectData(rootPath=rootPath)
        return None

    def getCharacterData(self,
            rootPath: Path,
        ) -> dict[CharacterName, CharacterData]:
        commonCharatersSetting = Utils.readJSONFile(rootPath/f'Data/Characters/Common.json')
        characters = {
            characterName: CharacterData(rootPath, characterName, commonCharatersSetting)
            for characterName in CharacterName
        }
        return characters

    def getTilesetData(self, rootPath: Path) -> dict[TilesetName, TilesetData]:
        tilesets = {
            tilesetName: TilesetData(rootPath, tilesetName)
            for tilesetName in TilesetName
        }
        return tilesets

    def getBackgroundData(self, rootPath: Path) -> dict[BackgroundName, BackgroundData]:
        backgroundSettings = Utils.readJSONFile(rootPath/f'Data/Backgrounds.json')
        backgrounds = {
            backgroundName: BackgroundData(rootPath, backgroundName, backgroundSettings)
            for backgroundName in BackgroundName
        }
        return backgrounds

    def getFruitData(self, rootPath: Path) -> dict[FruitName, FruitData]:
        fruitSetting = Utils.readJSONFile(rootPath/f'Data/Items/Fruit.json')
        fruits = {
            fruitName: FruitData(rootPath, fruitName, fruitSetting)
            for fruitName in FruitName
        }
        return fruits

    def getEffectData(self, rootPath: Path) -> dict[EffectName, EffectData]:
        effectData = Utils.readJSONFile(rootPath/f'Data/Effects.json')
        effects = {
            EffectName[k]: EffectData(rootPath, v) for k, v  in effectData.items()
        }
        return effects
