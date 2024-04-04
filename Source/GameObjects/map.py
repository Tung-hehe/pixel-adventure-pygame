import pygame

from .background import Background
from .character import Character
from .Effects import Effect
from .fruit import Fruit
from .layer import Layer
from .tile import *

from Source.Utils import (
    BackgroundData,
    CharacterData,
    Collition,
    EffectData,
    FruitData,
    TilesetData,
)
from Source.Enums import (
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

        self.collectFruitEffects = pygame.sprite.Group()
        self.collectFruitData = effectData[EffectName.CollectFruit]
        return None

    def setupMap(self,
            playerData: CharacterData,
            mapData: dict,
            tilesetData: dict[TilesetName, TilesetData],
            fruitsData: dict[FruitName: FruitData],
            effectData: dict[EffectName: EffectData]
        ) -> None:
        self.tiles = pygame.sprite.Group()
        for layer in mapData['layers']:
            layerClass = eval(layer["class"])
            if issubclass(layerClass, Tile):
                tileset = tilesetData[TilesetName(layer['tileset'])]
                self.tiles.add(Layer.createStaticTileLayer(layer, tileset, mapData))
            elif layerClass == Character:
                self.player = Layer.createPlayerLayer(layer, mapData, playerData, effectData)
            elif layerClass == Fruit:
                self.fruits = Layer.createFruitLayer(layer, mapData, fruitsData)
        return None

    def handlePlayerHorizontalMovementCollision(self) -> list[Tile]:
        self.player.sprite.horizontalMove()
        horizontalCollisionTiles = [
            tile for tile in self.tiles.sprites()
            if tile.isCollide(self.player.sprite)
        ]
        for tile in horizontalCollisionTiles:
            tile.horizontalCollisionWithPlayer(self.player.sprite)
        return horizontalCollisionTiles

    def handlePlayerVerticalMovementCollision(self) -> list[Tile]:
        self.player.sprite.veticalMove()
        verticalColitionTiles = [
            tile for tile in self.tiles.sprites()
            if tile.isCollide(self.player.sprite)
        ]
        for tile in verticalColitionTiles:
            tile.verticalCollisionWithPlayer(self.player.sprite)
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
        horizontalCollisionTiles = self.handlePlayerHorizontalMovementCollision()
        verticalColitionTiles = self.handlePlayerVerticalMovementCollision()
        self.player.sprite.rect.midbottom = self.player.sprite.hitbox.midbottom
        if not verticalColitionTiles:
            if not horizontalCollisionTiles:
                self.player.sprite.relativePosition = CharacterRelativePosition.OnAir
            else:
                if not any([tile.canCling for tile in horizontalCollisionTiles]):
                    self.player.sprite.relativePosition = CharacterRelativePosition.OnAir
        return None

    def draw(self, screen) -> None:
        self.background.draw(screen)
        self.tiles.draw(screen)
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
