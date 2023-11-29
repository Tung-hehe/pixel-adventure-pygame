import pygame

from player import Player
from tiles import Tile

class Level:

    def __init__(self, map: list, tileSize: tuple) -> None:
        self.map = self.setupMap(map, tileSize)

    def setupMap(self, map: list, tileSize: tuple) -> None:
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        for rowIndex, row in enumerate(map):
            for colIndex, tile in enumerate(row):
                position = (colIndex * tileSize[0], rowIndex * tileSize[1])
                if tile == 'X':
                    tile = Tile(position, tileSize)
                    self.tiles.add(tile)

                if tile == 'P':
                    player = Player(position)
                    self.player.add(player)

    def horizontalMovementCollision(self) -> None:
        player = self.player.sprite
        player.move()

        for tile in self.tiles.sprites():
            if tile.rect.colliderect(player.hitbox):
                if player.direction.x == -1:
                    player.hitbox.left = tile.rect.right
                elif player.direction.x == 1:
                    player.hitbox.right = tile.rect.left
                player.rect.midbottom = player.hitbox.midbottom

    def verticalMovementCollision(self) -> None:
        player = self.player.sprite
        player.applyGravity()

        for tile in self.tiles.sprites():
            if tile.rect.colliderect(player.hitbox):
                if player.direction.y > 0:
                    player.hitbox.bottom = tile.rect.top
                    player.direction.y = 0
                    player.onGround = True
                elif player.direction.y < 0:
                    player.hitbox.top = tile.rect.bottom
                    player.direction.y = 0
                player.rect.midbottom = player.hitbox.midbottom

        if (player.onGround and player.direction.y < 0) or player.direction.y > 1:
            player.onGround = False

    def update(self, screen) -> None:
        self.tiles.draw(screen)
        self.player.update()
        self.horizontalMovementCollision()
        self.verticalMovementCollision()
        self.player.draw(screen)
