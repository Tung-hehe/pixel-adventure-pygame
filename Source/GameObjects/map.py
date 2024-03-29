import random

import numpy as np
import pygame

from .background import Background
from .character import Character
from .effect import Effect
from .fruit import Fruit
from .tile import (
    Tile,
    StaticTile,
    OneWayCollisionStaticTile
)

from Source.Utils import (
    BackgroundData,
    CharacterData,
    Collition,
    EffectData,
    FruitData,
    TilesetData,
)
from Source.enums import (
    CharacterStatus,
    CharacterRelativePosition,
    EffectName,
    FruitName,
    TilesetName
)


class Map:

    def __init__(self,
            mapData: dict,
            playerData: CharacterData,
            tilesetData: dict[TilesetName, TilesetData],
            backgroundData: BackgroundData,
            fruitsData: dict[FruitName: FruitData],
            effectData: dict[EffectName: EffectData]
        ) -> None:
        self.setupMap(playerData, mapData, tilesetData, fruitsData, effectData)
        self.background = Background(backgroundData)
        return None

    def setupMap(self,
            playerData: CharacterData,
            mapData: dict,
            tilesetData: dict[TilesetName, TilesetData],
            fruitsData: dict[FruitName: FruitData],
            effectData: dict[EffectName: EffectData]
        ) -> None:
        self.staticTiles = pygame.sprite.Group()
        self.fruits = pygame.sprite.Group()
        self.collectFruitEffects = pygame.sprite.Group()
        self.collectFruitData = effectData[EffectName.CollectFruit]
        for layer in mapData['layers']:
            if layer["type"] == "Tile":
                tileset = tilesetData[TilesetName(layer['tileset'])]
                for rowIndex, row in enumerate(layer['data']):
                    for colIndex, tileIndex in enumerate(row):
                        if tileIndex == -1: continue
                        position = (
                            colIndex * mapData['tileWidth'],
                            (rowIndex + 1) * mapData['tileHeight']
                        )
                        if layer['class'] == 'StaticTile':
                            tile = StaticTile(
                                position=position,
                                surface=tileset.surfaces[tileIndex],
                                canCling=layer['canCling']
                            )
                        elif layer['class'] == 'OneWayCollisionStaticTile':
                            tile = OneWayCollisionStaticTile(
                                position=position,
                                surface=tileset.surfaces[tileIndex],
                                hitbox=layer['hitbox'],
                                canCling=layer['canCling']
                            )
                        self.staticTiles.add(tile)
            elif layer["type"] == "Object":
                if layer['class'] == "Player":
                    coordinateX = np.where(layer['data'] != -1)[1]
                    coordinateY = np.where(layer['data'] != -1)[0]
                    if len(coordinateX) > 1 or len(coordinateY) > 1:
                        raise ValueError("More than one player")
                    elif len(coordinateX) == 1 and len(coordinateY) == 1:
                        coordinateX = coordinateX[0]
                        coordinateY = coordinateY[0]
                        position = (
                            coordinateX * mapData['tileWidth'],
                            (coordinateY + 1) * mapData['tileHeight']
                        )
                        self.player = pygame.sprite.GroupSingle()
                        self.player.add(
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
                    else:
                        pass
                elif layer['class'] == "Fruit":
                    for rowIndex, row in enumerate(layer['data']):
                        for colIndex, tileIndex in enumerate(row):
                            if tileIndex == -1: continue
                            position = (
                                colIndex * mapData['tileWidth'],
                                (rowIndex + 1) * mapData['tileHeight']
                            )
                            self.fruits.add(Fruit(position, fruitsData[random.choice(list(FruitName))]))
        return None

    def handlePlayerHorizontalMovementCollision(self) -> list[Tile]:
        self.player.sprite.horizontalMove()
        horizontalCollisionTiles = [
            tile for tile in self.staticTiles.sprites()
            if tile.isCollide(self.player.sprite)
        ]
        canCling = False
        for tile in horizontalCollisionTiles:
            if tile.canCling:
                canCling = True
            if self.player.sprite.velocity.x < 0:
                self.player.sprite.hitbox.left = tile.rect.right
            elif self.player.sprite.velocity.x > 0:
                self.player.sprite.hitbox.right = tile.rect.left
        return canCling, horizontalCollisionTiles

    def handlePlayerVerticalMovementCollision(self) -> list[Tile]:
        self.player.sprite.veticalMove()
        verticalColitionTiles = [
            tile for tile in self.staticTiles.sprites()
            if tile.isCollide(self.player.sprite)
        ]
        for tile in verticalColitionTiles:
            if self.player.sprite.velocity.y > 0:
                self.player.sprite.hitbox.bottom = tile.rect.top
                self.player.sprite.velocity.y = 0
                # Reset jump on air counter
                self.player.sprite.jumpOnAirCount = 0
                self.player.sprite.relativePosition = CharacterRelativePosition.OnGround
            elif self.player.sprite.velocity.y < 0:
                self.player.sprite.hitbox.top = tile.rect.bottom
                self.player.sprite.velocity.y = 0
        return verticalColitionTiles

    def collectFruit(self) -> None:
        for fruit in self.fruits.sprites():
            if Collition.rectCollision(self.player.sprite.hitbox, fruit.hitbox):
                # NOTE. Add score here
                self.collectFruitEffects.add(Effect(
                    position=fruit.hitbox.center,
                    effectData=self.collectFruitData,
                    relativePosition='center'
                ))
                fruit.kill()
        return None

    def handlePlayerMovementCollision(self) -> None:
        self.player.sprite.trackingPosition = self.player.sprite.hitbox.midbottom
        canCling, horizontalCollisionTiles = self.handlePlayerHorizontalMovementCollision()
        verticalColitionTiles = self.handlePlayerVerticalMovementCollision()
        self.player.sprite.rect.midbottom = self.player.sprite.hitbox.midbottom

        if horizontalCollisionTiles:
            if (
                self.player.sprite.relativePosition == CharacterRelativePosition.OnAir
                and self.player.sprite.status == CharacterStatus.Fall and canCling
            ):
                self.player.sprite.velocity.y = 0
                self.player.sprite.relativePosition = CharacterRelativePosition.OnWall
            elif not verticalColitionTiles and not canCling:
                self.player.sprite.relativePosition = CharacterRelativePosition.OnAir
        elif not verticalColitionTiles:
            self.player.sprite.relativePosition = CharacterRelativePosition.OnAir
        return None

    def draw(self, screen) -> None:
        self.background.draw(screen)
        self.staticTiles.draw(screen)
        self.fruits.draw(screen)
        self.player.draw(screen)
        self.player.sprite.effects.draw(screen)
        self.collectFruitEffects.draw(screen)
        return None

    def update(self) -> None:
        self.background.scroll()
        self.handlePlayerMovementCollision()
        self.collectFruit()
        self.player.update()
        self.fruits.update()
        self.collectFruitEffects.update()
        return None
