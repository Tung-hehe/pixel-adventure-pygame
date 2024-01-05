import pygame

from .background import Background
from .character import Character
from .tile import (
    Tile,
    StaticTile
)

from Source.Utils import (
    CharacterData,
    TilesetData,
    BackgroundData
)
from Source.enums import (
    CharacterStatus,
    CharacterRelativePosition
)


class Map:

    def __init__(self,
            map: list,
            playerData: CharacterData,
            tilesetData: TilesetData,
            backgroundData: BackgroundData
        ) -> None:
        self.setupMap(map, playerData, tilesetData)
        self.background = Background(backgroundData)
        return None

    def setupMap(self,
            map: list,
            playerData: CharacterData,
            tilesetData: TilesetData,
        ) -> None:
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        tileSize = (16, 16)
        for rowIndex, row in enumerate(map):
            for colIndex, tileIndex in enumerate(row):
                if tileIndex != -1:
                    position = (colIndex * tileSize[0], rowIndex * tileSize[1])
                    tile = StaticTile(position, tilesetData.surfaces[tileIndex])
                    self.tiles.add(tile)

        player = Character(position=(100, 100), data=playerData)
        self.player.add(player)
        return None

    def handlePlayerHorizontalMovementColition(self) -> list[Tile]:
        self.player.sprite.horizontalMove()
        horizontalCollisionTiles = [
            tile for tile in self.tiles.sprites()
            if tile.rect.colliderect(self.player.sprite.hitbox)
        ]
        for tile in horizontalCollisionTiles:
            if self.player.sprite.velocity.x < 0:
                self.player.sprite.hitbox.left = tile.rect.right
            elif self.player.sprite.velocity.x > 0:
                self.player.sprite.hitbox.right = tile.rect.left
        return horizontalCollisionTiles

    def handlePlayerVerticalMovementColition(self) -> list[Tile]:
        self.player.sprite.veticalMove()
        verticalColitionTiles = [
            tile for tile in self.tiles.sprites()
            if tile.rect.colliderect(self.player.sprite.hitbox)
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

    def handlePlayerMovementCollision(self) -> None:
        horizontalCollisionTiles = self.handlePlayerHorizontalMovementColition()
        verticalColitionTiles = self.handlePlayerVerticalMovementColition()
        self.player.sprite.rect.midbottom = self.player.sprite.hitbox.midbottom

        if horizontalCollisionTiles:
            if self.player.sprite.relativePosition == CharacterRelativePosition.OnAir:
                if self.player.sprite.status == CharacterStatus.Fall:
                    self.player.sprite.velocity.y = 0
                    self.player.sprite.relativePosition = CharacterRelativePosition.OnWall
        elif not verticalColitionTiles:
            self.player.sprite.relativePosition = CharacterRelativePosition.OnAir
        return None

    def update(self, screen) -> None:
        self.background.scroll()
        self.background.draw(screen)

        self.tiles.draw(screen)

        self.handlePlayerMovementCollision()
        self.player.update()
        self.player.draw(screen)
        return None
