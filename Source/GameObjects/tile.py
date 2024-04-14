import pygame

from .character import Character
from Source.Utils import (
    Collition,
    TilesetData
)
from Source.Enums import (
    CharacterRelativePosition,
    CharacterStatus,
    DynamicTileStatus
)


class Tile(pygame.sprite.Sprite):

    def __init__(self, canCling: bool) -> None:
        super().__init__()
        self.canCling = canCling
        self.canFollow = False
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

    def update(self) -> None:
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


class DynamicTile(Tile):

    def __init__(self, tilesetData: TilesetData, canCling: bool) -> None:
        super().__init__(canCling)
        self.data = tilesetData
        self.frameIndex = 0
        return None


class FallingPlatform(DynamicTile):

    def __init__(self,
            position: tuple,
            tilesetData: TilesetData,
            status: DynamicTileStatus
        ) -> None:
        super().__init__(tilesetData, False)
        self.status = DynamicTileStatus[status]
        self.image = self.data.animations[self.status][0]
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = self.data.acceleration
        self.rect = self.image.get_rect(topleft=position)
        self.flag = None
        self.canFollow = True
        return None

    def isCollide(self, object: pygame.sprite.Sprite) -> bool:
        return Collition.oneWayCollisionWithObject(self.rect, object)

    def updateImage(self) -> None:
        animation = self.data.animations[self.status]
        self.frameIndex += self.data.animationSpeed
        if self.frameIndex >= len(animation):
            self.frameIndex = 0
        self.image = animation[int(self.frameIndex)]
        return None

    def verticalCollisionWithPlayer(self, player: Character) -> None:
        super().verticalCollisionWithPlayer(player)
        self.status = DynamicTileStatus.Off
        # if self.flag is None:
        #     self.flag = pygame.time.get_ticks()
        return None

    def updateStatus(self) -> None:
        # if self.flag and pygame.time.get_ticks() - self.flag > self.data.duration:
        #     self.status = DynamicTileStatus.Off
        return None

    def updatePosition(self) -> None:
        if self.status == DynamicTileStatus.On:
            if self.velocity.y >= self.data.oscillation:
                self.acceleration = -self.data.acceleration
            elif self.velocity.y <= -self.data.oscillation:
                self.acceleration = self.data.acceleration
            self.velocity.y += self.acceleration
        elif self.status == DynamicTileStatus.Off:
            self.velocity.y += self.data.gravity
        else:
            raise ValueError('Unknown status')
        self.rect.y += self.velocity.y
        return None

    def update(self) -> None:
        self.updateImage()
        self.updatePosition()
        return None
