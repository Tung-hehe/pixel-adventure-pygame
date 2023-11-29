from pathlib import Path

import pygame

from Source.Utils import Utils


class Player(pygame.sprite.Sprite):

    def __init__(self, position: tuple) -> None:
        super().__init__()

        # Player status
        self.status = 'idle'
        self.facingRight = True
        self.onGround = False
        # self.onCeiling = False
        # self.onWallLeft = False
        # self.onWallRight = False

        # Player image
        self.getAnimations()
        self.frameIndex = 0
        self.animationSpeed = 0.25
        self.image = self.animations[self.status][self.frameIndex]
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = pygame.Rect(position, (40, 50))
        self.hitbox.midbottom = self.rect.midbottom

        # Player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 5
        self.gravity = 0.8
        self.smoothSpeed = 0.4
        self.jumpSpeed = -16


    def getAnimations(self) -> None:
        currentDirPath = Path(__file__).absolute().parents[1]
        characterFolder = 'Assets/Image/MainCharacters/PinkMan'
        characterAnimationsPath = currentDirPath / characterFolder

        self.animations = {'idle':[], 'run':[], 'jump': [], 'fall': []}
        for animation in self.animations.keys():
            characterAnimationPath = characterAnimationsPath / animation
            self.animations[animation] = Utils.getSurfaceListFromSpritesheets(path=characterAnimationPath)

    def getEvent(self) -> None:
        # Get event
        keys = pygame.key.get_pressed()

        # Move event
        if keys[pygame.K_d]:
            self.direction.x = 1
            self.facingRight = True
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.facingRight = False
        else:
            self.direction.x = 0
        # Jump event
        if keys[pygame.K_w] and self.onGround:
            self.jump()

    def getStatus(self) -> None:
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > self.gravity:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def animate(self):
        animation = self.animations[self.status]

        self.frameIndex += self.animationSpeed
        if self.frameIndex >= len(animation):
            self.frameIndex = 0

        image = animation[int(self.frameIndex)]
        if self.facingRight:
            self.image = image
        else:
            self.image = pygame.transform.flip(
                surface=image, flip_x=True, flip_y=False
            )

    def move(self) -> None:
        self.rect.x += self.direction.x * self.speed
        self.hitbox.x += self.direction.x * self.speed

    def jump(self) -> None:
        self.direction.y = self.jumpSpeed

    def applyGravity(self) -> None:
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
        self.hitbox.y += self.direction.y

    def update(self) -> None:
        self.getEvent()
        self.getStatus()
        self.animate()
