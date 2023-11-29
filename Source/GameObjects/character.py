from pathlib import Path

import pygame

from Source.Utils import (
    Utils,
    CharacterSettings
)
from Source.enums import (
    CharacterStatus,
    CharacterFacing,
    CharacterRelativePosition,
)


class Character(pygame.sprite.Sprite):

    def __init__(self, position: tuple, settings: CharacterSettings) -> None:
        super().__init__()
        self.initFromConstants(settings)

        # Player status
        self.status = CharacterStatus.Idle
        self.facing = CharacterFacing.Right
        self.relativePosition = CharacterRelativePosition.OnAir

        # Player image
        self.frameIndex = 0
        self.image = self.animations[self.status][self.frameIndex]

        #Player direction
        self.direction = pygame.math.Vector2(0, 0)

        # Player hitbox
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = pygame.Rect(position, (settings.hitboxWidth, settings.hitboxHeight))
        self.hitbox.midbottom = self.rect.midbottom
        return None

    def initFromConstants(self, settings: CharacterSettings) -> None:
        self.runSpeed = settings.runSpeed
        self.fallSpeed = settings.fallSpeed
        self.jumpSpeed = settings.jumpSpeed
        self.animationSpeed = settings.animationSpeed
        self.getAnimations(settings.spritesheetsFolderPath, settings.spriteWidth, settings.spriteHeight)
        return None

    def getAnimations(self, spritesheetsFolderPath: Path, spriteWidth: int, spriteHeight: int) -> None:
        self.animations = {status: [] for status in CharacterStatus}
        for status in self.animations.keys():
            spritesheetPath = spritesheetsFolderPath / f'{status.value}.png'
            self.animations[status] = Utils.getSurfaceListFromSpritesheets(
                spritesheetsPath=spritesheetPath,
                width=spriteWidth, height=spriteHeight, scale=2
            )
        return None

    def handleEvent(self) -> None:
        # Get event
        keys = pygame.key.get_pressed()
        # Move event
        if keys[pygame.K_d]:
            self.direction.x = 1
            self.facing = CharacterFacing.Right
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.facing = CharacterFacing.Left
        else:
            self.direction.x = 0
        # Jump event
        if keys[pygame.K_w] and self.relativePosition == CharacterRelativePosition.OnGround:
            self.direction.y = self.jumpSpeed
        return None

    def updateStatus(self) -> None:
        if self.direction.y < 0:
            self.status = CharacterStatus.Jump
        elif self.direction.y > self.fallSpeed:
            self.status = CharacterStatus.Fall
        else:
            if self.direction.x != 0:
                self.status = CharacterStatus.Run
            else:
                self.status = CharacterStatus.Idle
        return None

    def updateImage(self):
        animation = self.animations[self.status]
        self.frameIndex += self.animationSpeed
        if self.frameIndex >= len(animation):
            self.frameIndex = 0
        if self.facing == CharacterFacing.Right:
            self.image = animation[int(self.frameIndex)]
        elif self.facing == CharacterFacing.Left:
            self.image = pygame.transform.flip(
                surface=animation[int(self.frameIndex)], flip_x=True, flip_y=False
            )
        else:
            raise ValueError(f"Unkown character facing {self.facing}")
        return None

    def horizontalMove(self) -> None:
        self.rect.x += self.direction.x * self.runSpeed
        self.hitbox.x += self.direction.x * self.runSpeed
        return None

    def veticalMove(self) -> None:
        self.direction.y += self.fallSpeed
        self.rect.y += self.direction.y
        self.hitbox.y += self.direction.y
        return None

    def update(self) -> None:
        self.handleEvent()
        self.updateStatus()
        self.updateImage()
        return None
