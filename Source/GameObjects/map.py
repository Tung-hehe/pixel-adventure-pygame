import pygame

from .character import Character
from .tile import Tile

from Source.Utils import (
    CharacterSettings,
    CharacterAssets
)
from Source.enums import CharacterRelativePosition


class Map:

    def __init__(self,
            map: list,
            tileSize: tuple,
            playerSettings: CharacterSettings,
            playerAssets: CharacterAssets
        ) -> None:
        self.map = self.setupMap(map, tileSize, playerSettings, playerAssets)
        return None

    def setupMap(self,
            map: list,
            tileSize: tuple,
            playerSettings: CharacterSettings,
            playerAssets: CharacterAssets
        ) -> None:
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        for rowIndex, row in enumerate(map):
            for colIndex, tile in enumerate(row):
                position = (colIndex * tileSize[0], rowIndex * tileSize[1])
                if tile == 'X':
                    tile = Tile(position, tileSize)
                    self.tiles.add(tile)

                if tile == 'P':
                    player = Character(position=position, settings=playerSettings, assets=playerAssets)
                    self.player.add(player)
        return None

    def horizontalMovementCollision(self) -> None:
        player = self.player.sprite
        player.horizontalMove()
        for tile in self.tiles.sprites():
            if tile.rect.colliderect(player.hitbox):
                if player.direction.x == -1:
                    player.hitbox.left = tile.rect.right
                elif player.direction.x == 1:
                    player.hitbox.right = tile.rect.left
                player.rect.midbottom = player.hitbox.midbottom
        return None

    def verticalMovementCollision(self) -> None:
        player = self.player.sprite
        player.veticalMove()
        for tile in self.tiles.sprites():
            if tile.rect.colliderect(player.hitbox):
                if player.direction.y > 0:
                    player.hitbox.bottom = tile.rect.top
                    player.direction.y = 0
                    player.relativePosition = CharacterRelativePosition.OnGround
                elif player.direction.y < 0:
                    player.hitbox.top = tile.rect.bottom
                    player.direction.y = 0
                player.rect.midbottom = player.hitbox.midbottom
        isOnGround = player.relativePosition == CharacterRelativePosition.OnGround
        if (isOnGround and player.direction.y < 0) or player.direction.y > 1:
            player.relativePosition = CharacterRelativePosition.OnAir
        return None

    def update(self, screen) -> None:
        self.tiles.draw(screen)
        self.player.update()
        self.horizontalMovementCollision()
        self.verticalMovementCollision()
        self.player.draw(screen)
        return None
