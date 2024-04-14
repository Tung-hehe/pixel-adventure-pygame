import random

import numpy as np
import pygame

from .character import Character
from .fruit import Fruit
from .tile import *

from Source.Enums import (
    EffectName,
    FruitName,
)
from Source.Utils import (
    CharacterData,
    EffectData,
    FruitData,
    TilesetData
)


class Layer:

    @classmethod
    def createTileLayer(cls,
            layer: dict, tileset: TilesetData, mapData: dict
        ) -> pygame.sprite.Group:
        tiles = pygame.sprite.Group()
        for rowIndex, row in enumerate(layer['data']):
            for colIndex, tileIndex in enumerate(row):
                if tileIndex == -1: continue
                position = (
                    colIndex * mapData['tileWidth'],
                    (rowIndex + 1) * mapData['tileHeight']
                )
                TileClass = eval(layer['class'])
                tile = None
                if issubclass(TileClass, StaticTile):
                    tile = TileClass(
                        position=position,
                        surface=tileset.surfaces[tileIndex],
                        **layer["settings"]
                    )
                elif issubclass(TileClass, DynamicTile):
                    tile = TileClass(
                        position=position,
                        tilesetData=tileset,
                        **layer["settings"]
                    )
                if tile is not None:
                    tiles.add(tile)
        return tiles

    @classmethod
    def createPlayerLayer(cls,
            layer: dict,
            mapData: dict,
            playerData: CharacterData,
            effectData: dict[EffectName: EffectData]
        ) -> pygame.sprite.GroupSingle:
        coordinateX = np.where(layer['data'] != -1)[1]
        coordinateY = np.where(layer['data'] != -1)[0]
        if len(coordinateX) != len(coordinateY):
            raise ValueError("Player coordinate not valide")
        if len(coordinateX) > 1 or len(coordinateY) > 1:
            raise ValueError("More than one player")
        elif len(coordinateX) == 1 and len(coordinateY) == 1:
            coordinateX = coordinateX[0]
            coordinateY = coordinateY[0]
            position = (
                coordinateX * mapData['tileWidth'],
                (coordinateY + 1) * mapData['tileHeight']
            )
            player = pygame.sprite.GroupSingle()
            player.add(
                Character(
                    position=position,
                    startState=layer["startState"],
                    data=playerData,
                    effectsData={
                        k: effectData[k] for k in [
                            EffectName.Run,
                            EffectName.Jump,
                            EffectName.Land
                        ]
                    }
                )
            )
            return player
        else:
            raise ValueError("More than one player")

    @classmethod
    def createFruitLayer(self,
            layer: dict,
            mapData: dict,
            fruitsData: dict[FruitName: FruitData]
        ) -> pygame.sprite.Group:
        fruits = pygame.sprite.Group()
        for rowIndex, row in enumerate(layer['data']):
            for colIndex, tileIndex in enumerate(row):
                if tileIndex == -1: continue
                position = (
                    colIndex * mapData['tileWidth'],
                    (rowIndex + 1) * mapData['tileHeight']
                )
                fruits.add(Fruit(position, fruitsData[random.choice(list(FruitName))]))
        return fruits
