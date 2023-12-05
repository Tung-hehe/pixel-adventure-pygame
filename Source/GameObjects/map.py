import pygame

from .background import Background
from .character import Character
from .tile import StaticTile

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

    def horizontalMovementCollision(self) -> None:
        player = self.player.sprite
        player.horizontalMove()
        for tile in self.tiles.sprites():
            if tile.rect.colliderect(player.hitbox):
                if player.direction.x == -1:
                    player.hitbox.left = tile.rect.right
                elif player.direction.x == 1:
                    player.hitbox.right = tile.rect.left
                # if player.relativePosition == CharacterRelativePosition.OnAir and player.status == CharacterStatus.Fall:
                #     player.direction.x = 0
                #     player.direction.y = 0
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
                    # Reset jump on air counter
                    player.jumpOnAirCount = 0
                    player.relativePosition = CharacterRelativePosition.OnGround
                elif player.direction.y < 0:
                    player.hitbox.top = tile.rect.bottom
                    player.direction.y = 0
                player.rect.midbottom = player.hitbox.midbottom
        isOnGround = player.relativePosition == CharacterRelativePosition.OnGround
        if (isOnGround and player.direction.y < 0) or player.direction.y > 0:
            player.relativePosition = CharacterRelativePosition.OnAir
        return None

    def update(self, screen) -> None:
        self.background.scroll()
        self.background.draw(screen)

        self.tiles.draw(screen)

        self.player.update()
        self.horizontalMovementCollision()
        self.verticalMovementCollision()
        self.player.draw(screen)
        return None
