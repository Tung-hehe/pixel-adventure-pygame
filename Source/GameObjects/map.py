import pygame

from .background import Background
from .character import Character
from .Effects import Effect
from .fruit import Fruit
from .layer import Layer
from .tile import (
    OneWayCollisionStaticTile,
    StaticTile,
    Tile
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
        self.staticTiles = pygame.sprite.Group()
        for layer in mapData['layers']:
            layerClass = eval(layer["class"])
            if issubclass(layerClass, StaticTile):
                tileset = tilesetData[TilesetName(layer['tileset'])]
                self.staticTiles.add(Layer.createStaticTileLayer(layer, tileset, mapData))
            elif layerClass == Character:
                self.player = Layer.createPlayerLayer(layer, mapData, playerData, effectData)
            elif layerClass == Fruit:
                self.fruits = Layer.createFruitLayer(layer, mapData, fruitsData)
        return None

    def handlePlayerHorizontalMovementCollision(self) -> tuple[bool, list[Tile]]:
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
