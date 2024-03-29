import pygame

from Source.Utils import Collition


class Tile(pygame.sprite.Sprite):

    def __init__(self, position: tuple, surface: pygame.Surface, canCling: bool) -> None:
        super().__init__()
        self.image = surface
        self.rect = self.image.get_rect(bottomleft=position)
        self.canCling = canCling
        return None

    def isCollide(self, object: pygame.sprite.Sprite) -> bool:
        return Collition.rectCollision(self.rect, object.hitbox)

class StaticTile(Tile):

    def __init__(self, position: tuple, surface: pygame.Surface, canCling: bool) -> None:
        super().__init__(position, surface, canCling)
        return None

class OneWayCollisionStaticTile(StaticTile):

    def __init__(self, position: tuple, surface: pygame.Surface, hitbox: tuple, canCling: bool) -> None:
        super().__init__(position, surface, canCling)
        self.rect.width = hitbox[0]
        self.rect.height = hitbox[1]
        return None

    def isCollide(self, object: pygame.sprite.Sprite) -> bool:
        return Collition.oneWayCollisionWithObject(self.rect, object)
