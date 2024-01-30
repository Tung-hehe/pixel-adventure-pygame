from pathlib import Path

import pygame

from .background import Background
from .character import Character
from .tile import (
    Tile,
    StaticTile,
    OneWayCollisionStaticTile
)

from Source.Utils import (
    BackgroundData,
    CharacterData,
    TilesetData
)
from Source.enums import (
    CharacterStatus,
    CharacterRelativePosition,
    TilesetName,
)


class Map:

    def __init__(self,
            mapData: dict,
            playerData: CharacterData,
            tilesetData: dict[TilesetName, TilesetData],
            backgroundData: BackgroundData
        ) -> None:
        self.setupMap(mapData, tilesetData)
        self.background = Background(backgroundData)
        self.player = pygame.sprite.GroupSingle()
        self.player.add(Character(position=mapData['playerPosition'], data=playerData))
        return None

    def setupMap(self, mapData: dict, tilesetData: dict[TilesetName, TilesetData]) -> None:
        self.staticTiles = pygame.sprite.Group()
        self.oneWayCollisionStaticTile = pygame.sprite.Group()
        for layer in mapData['layers']:
            for rowIndex, row in enumerate(layer['data']):
                for colIndex, tileIndex in enumerate(row):
                    if tileIndex == -1: continue
                    position = (colIndex * mapData['tileWidth'], rowIndex * mapData['tileHeight'])
                    if layer['class'] == 'StaticTile':
                        tile = StaticTile(
                            position, tilesetData[TilesetName(layer['tileset'])].surfaces[tileIndex]
                        )
                        self.staticTiles.add(tile)
                    elif layer['class'] == 'OneWayCollisionStaticTile':
                        tile = OneWayCollisionStaticTile(
                            position, tilesetData[TilesetName(layer['tileset'])].surfaces[tileIndex], layer['hitbox']
                        )
                        self.oneWayCollisionStaticTile.add(tile)
        return None

    def handlePlayerHorizontalMovementCollision(self) -> list[Tile]:
        self.player.sprite.horizontalMove()
        horizontalCollisionTiles = [
            tile for tile in self.staticTiles.sprites()
            if tile.rect.colliderect(self.player.sprite.hitbox)
        ]
        for tile in horizontalCollisionTiles:
            if self.player.sprite.velocity.x < 0:
                self.player.sprite.hitbox.left = tile.rect.right
            elif self.player.sprite.velocity.x > 0:
                self.player.sprite.hitbox.right = tile.rect.left
        return horizontalCollisionTiles

    def handlePlayerVerticalMovementCollision(self) -> list[Tile]:
        self.player.sprite.veticalMove()
        verticalColitionTiles = [
            tile for tile in self.staticTiles.sprites()
            if tile.rect.colliderect(self.player.sprite.hitbox)
        ]

        # Collision with one way colision static tile (only from top)
        for tile in self.oneWayCollisionStaticTile.sprites():
            if not tile.rect.colliderect(self.player.sprite.hitbox):
                continue
            if self.player.sprite.velocity.y <= 0:
                continue
            if self.player.sprite.trackingPosition[1] <= tile.rect.midbottom[1] <= self.player.sprite.hitbox.midbottom[1]:
                verticalColitionTiles.append(tile)

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

    def handlePlayerMovementCollision(self) -> None:
        self.player.sprite.trackingPosition = self.player.sprite.hitbox.midbottom
        horizontalCollisionTiles = self.handlePlayerHorizontalMovementCollision()
        verticalColitionTiles = self.handlePlayerVerticalMovementCollision()
        self.player.sprite.rect.midbottom = self.player.sprite.hitbox.midbottom

        if horizontalCollisionTiles:
            if self.player.sprite.relativePosition == CharacterRelativePosition.OnAir:
                if self.player.sprite.status == CharacterStatus.Fall:
                    self.player.sprite.velocity.y = 0
                    self.player.sprite.relativePosition = CharacterRelativePosition.OnWall
        elif not verticalColitionTiles:
            self.player.sprite.relativePosition = CharacterRelativePosition.OnAir
        return None

    def draw(self, screen) -> None:
        self.background.draw(screen)
        self.staticTiles.draw(screen)
        self.oneWayCollisionStaticTile.draw(screen)
        self.player.draw(screen)
        return None

    def update(self) -> None:
        self.background.scroll()
        self.handlePlayerMovementCollision()
        self.player.update()
        return None
