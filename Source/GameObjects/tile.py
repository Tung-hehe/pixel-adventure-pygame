import pygame


class Tile(pygame.sprite.Sprite):

    def __init__(self, position: tuple, surface: pygame.Surface) -> None:
        super().__init__()
        self.image = surface
        self.rect = self.image.get_rect(topleft=position)
        return None

    def isCollide(self, object: pygame.sprite.Sprite) -> bool:
        return self.rect.colliderect(object.hitbox)

class StaticTile(Tile):

    def __init__(self, position: tuple, surface: pygame.Surface) -> None:
        super().__init__(position, surface)

class OneWayCollisionStaticTile(StaticTile):

    def __init__(self, position: tuple, surface: pygame.Surface, hitbox: tuple) -> None:
        super().__init__(position, surface)
        self.rect = pygame.Rect(position, hitbox)

    def isCollide(self, object: pygame.sprite.Sprite) -> bool:
        if not self.rect.colliderect(object.hitbox):
            return False
        if object.velocity.y <= 0:
            return False
        if object.trackingPosition[1] <= self.rect.midtop[1] <= object.hitbox.midbottom[1]:
            return True
