import pygame

from player import Player
from tiles import Tile

class Level:

    def __init__(self, map: list, tileSize: tuple, playerSize: tuple) -> None:
        self.map = self.setupMap(map, tileSize, playerSize)

    def setupMap(self, map: list, tileSize: tuple, playerSize: tuple) -> None:
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        for rowIndex, row in enumerate(map):
            for colIndex, tile in enumerate(row):

                if tile == 'X':
                    tilePosition = (colIndex * tileSize[0], rowIndex * tileSize[1])
                    tile = Tile(tilePosition, tileSize)
                    self.tiles.add(tile)

                if tile == 'P':
                    playerPosition = (colIndex * playerSize[0], rowIndex * playerSize[1])
                    player = Player(playerPosition, playerSize)
                    self.player.add(player)

    def horizontalMovementCollision(self) -> None:
        player = self.player.sprite
        player.move()

        for tile in self.tiles.sprites():
            if tile.rect.colliderect(player.rect):
                if player.direction.x == -1:
                    player.rect.left = tile.rect.right
                elif player.direction.x == 1:
                    player.rect.right = tile.rect.left

    def verticalMovementCollision(self) -> None:
        player = self.player.sprite
        player.applyGravity()

        for tile in self.tiles.sprites():
            if tile.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = tile.rect.top
                    player.direction.y = 0
                elif player.direction.y < 0:
                    player.rect.top = tile.rect.bottom
                    player.direction.y = 0

    def update(self, screen) -> None:
        self.tiles.draw(screen)
        self.player.update()
        self.horizontalMovementCollision()
        self.verticalMovementCollision()
        self.player.draw(screen)
