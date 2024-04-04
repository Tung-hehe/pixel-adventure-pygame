import pygame

from .character import Character
from Source.Utils import Collition
from Source.Enums import (
    CharacterRelativePosition,
    CharacterStatus
)


class Tile(pygame.sprite.Sprite):

    def __init__(self, canCling: bool) -> None:
        super().__init__()
        self.canCling = canCling
        return None

    def horizontalCollisionWithPlayer(self, player: Character) -> None:
        if (
            player.relativePosition == CharacterRelativePosition.OnAir
            and player.status == CharacterStatus.Fall and self.canCling
        ):
            player.velocity.y = 0
            player.relativePosition = CharacterRelativePosition.OnWall
        if player.velocity.x < 0:
            player.hitbox.left = self.rect.right
        elif player.velocity.x > 0:
            player.hitbox.right = self.rect.left
        return None

    def verticalCollisionWithPlayer(self, player: Character) -> None:
        if player.velocity.y > 0:
            player.hitbox.bottom = self.rect.top
            player.velocity.y = 0
            # Reset jump on air counter
            player.jumpOnAirCount = 0
            player.relativePosition = CharacterRelativePosition.OnGround
        elif player.velocity.y < 0:
            player.hitbox.top = self.rect.bottom
            player.velocity.y = 0
        return None


class StaticTile(Tile):

    def __init__(self, position: tuple, surface: pygame.Surface, canCling: bool) -> None:
        super().__init__(canCling)
        self.image = surface
        self.rect = self.image.get_rect(bottomleft=position)
        return None

    def isCollide(self, object: pygame.sprite.Sprite) -> bool:
        return Collition.rectCollision(self.rect, object.hitbox)


class OneWayCollisionStaticTile(StaticTile):

    def __init__(self,
            position: tuple,
            surface: pygame.Surface,
            hitbox: tuple,
            canCling: bool
        ) -> None:
        super().__init__(position, surface, canCling)
        self.rect.width = hitbox[0]
        self.rect.height = hitbox[1]
        return None

    def isCollide(self, object: pygame.sprite.Sprite) -> bool:
        return Collition.oneWayCollisionWithObject(self.rect, object)


class DynamicType(Tile):

    def __init__(self, animations: dict, canCling: bool) -> None:
        super().__init__(canCling)
        self.animations = animations
        return None


class FallingFlatform(DynamicType):

    def __init__(self):
        pass
