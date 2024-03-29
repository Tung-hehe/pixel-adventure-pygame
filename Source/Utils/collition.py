import pygame


class Collition:

    @classmethod
    def rectCollision(cls, firstRect: pygame.Rect, secondRect: pygame.Rect) -> bool:
        return firstRect.colliderect(secondRect)

    @classmethod
    def oneWayCollisionWithObject(cls, rect: pygame.Rect, obj: pygame.sprite.Sprite) -> bool:
        if not rect.colliderect(obj.hitbox):
            return False
        if obj.velocity.y <= 0:
            return False
        if obj.trackingPosition[1] <= rect.midtop[1] <= obj.hitbox.midbottom[1]:
            return True
        return False
