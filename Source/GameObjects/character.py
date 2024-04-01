import pygame

from .effect import Effect
from Source.Utils import (
    CharacterData,
    EffectData
)
from Source.enums import (
    CharacterStatus,
    CharacterFacing,
    CharacterRelativePosition,
    EffectName,
)


class Character(pygame.sprite.Sprite):

    def __init__(self,
            position: tuple[int, int],
            startState: dict,
            data: CharacterData,
            effectsData: dict[EffectName: EffectData]
        ) -> None:
        super().__init__()
        self.data = data
        # Player status
        self.status = CharacterStatus[startState["status"]]
        self.jumpOnAirCount = 0
        self.facing = CharacterFacing[startState["facing"]]
        self.relativePosition = CharacterRelativePosition[startState["relativePosition"]]
        self.trackingPosition = position
        self.effectsData = effectsData
        self.effects = pygame.sprite.Group()
        # Player image
        self.frameIndex = 0
        self.image = self.data.animations[self.status][self.frameIndex]
        #Player velocity
        self.velocity = pygame.math.Vector2(0, 0)
        # Player hitbox
        self.rect = self.image.get_rect(bottomleft=position)
        self.hitbox = pygame.Rect(position, (data.hitboxWidth, data.hitboxHeight))
        self.hitbox.midbottom = self.rect.midbottom
        return None

    def handleEvent(self) -> None:
        # Get event
        keys = pygame.key.get_pressed()
        # Move event
        if keys[pygame.K_d]:
            self.velocity.x = self.data.runSpeed
            self.facing = CharacterFacing.Right
        elif keys[pygame.K_a]:
            self.velocity.x = -self.data.runSpeed
            self.facing = CharacterFacing.Left
        else:
            if self.relativePosition != CharacterRelativePosition.OnWall:
                self.velocity.x = 0
        # Jump event
        if keys[pygame.K_w]:
            self.jump()
        return None

    def jump(self) -> None:
        if self.relativePosition == CharacterRelativePosition.OnAir:
            if self.status == CharacterStatus.Fall and self.jumpOnAirCount < self.data.limitJumpOnAir:
                if self.status != CharacterStatus.JumpOnAir:
                    self.effects.add(Effect(self.rect.midbottom, self.effectsData[EffectName.Jump]))
                self.status = CharacterStatus.JumpOnAir
                self.velocity.y = self.data.jumpOnAirSpeed[self.jumpOnAirCount]
                self.jumpOnAirCount += 1
        else:
            if self.relativePosition == CharacterRelativePosition.OnWall:
                if self.facing == CharacterFacing.Left:
                    self.facing = CharacterFacing.Right
                    self.velocity.x = self.data.bounceOffWall
                    relativePosition = 'midleft'
                    rotation = -90
                else:
                    self.facing = CharacterFacing.Left
                    self.velocity.x = - self.data.bounceOffWall
                    relativePosition = 'midright'
                    rotation = 90
                self.effects.add(Effect(
                    position=getattr(self.hitbox, relativePosition),
                    effectData=self.effectsData[EffectName.Jump],
                    relativePosition=relativePosition,
                    rotation=rotation
                ))
                self.velocity.y = self.data.jumpOffWall
            else:
                if self.status != CharacterStatus.Jump:
                    self.effects.add(Effect(self.rect.midbottom, self.effectsData[EffectName.Jump]))
                self.velocity.y = self.data.jumpSpeed
        return None

    def updateStatus(self) -> None:
        if self.velocity.y < 0:
            if self.status != CharacterStatus.JumpOnAir:
                self.status = CharacterStatus.Jump
        elif self.velocity.y > 0:
            if self.relativePosition == CharacterRelativePosition.OnAir:
                self.status = CharacterStatus.Fall
            elif self.relativePosition == CharacterRelativePosition.OnWall:
                self.status = CharacterStatus.ClingWall
                if self.frameIndex in self.data.spawnClingWallDustFrames:
                    if self.facing == CharacterFacing.Left:
                        relativePosition = 'topleft'
                        rotation = -90
                    else:
                        relativePosition = 'topright'
                        rotation = 90
                    self.effects.add(Effect(
                        getattr(self.hitbox, relativePosition),
                        self.effectsData[EffectName.Run],
                        relativePosition=relativePosition,
                        rotation=rotation
                    ))
        else:
            if self.velocity.x != 0:
                if self.relativePosition == CharacterRelativePosition.OnGround:
                    if self.status == CharacterStatus.Fall:
                        self.effects.add(Effect(
                            self.rect.midbottom,
                            self.effectsData[EffectName.Land],
                        ))
                    self.status = CharacterStatus.Run
                    if self.frameIndex in self.data.spawnRunDustFrames:
                        if self.facing == CharacterFacing.Right:
                            relativePosition = 'bottomleft'
                        else:
                            relativePosition = 'bottomright'
                        self.effects.add(Effect(
                            getattr(self.hitbox, relativePosition),
                            self.effectsData[EffectName.Run],
                            relativePosition=relativePosition,
                        ))
                elif self.relativePosition == CharacterRelativePosition.OnWall:
                    self.status = CharacterStatus.ClingWall
            else:
                if self.status == CharacterStatus.Fall:
                    self.effects.add(Effect(
                        self.rect.midbottom,
                        self.effectsData[EffectName.Land]
                    ))
                self.status = CharacterStatus.Idle
        return None

    def updateImage(self):
        animation = self.data.animations[self.status]
        self.frameIndex += self.data.animationSpeed
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
        self.rect.x += self.velocity.x
        self.hitbox.x += self.velocity.x
        return None

    def veticalMove(self) -> None:
        if self.relativePosition == CharacterRelativePosition.OnWall:
            self.velocity.y += self.data.gravity - self.data.wallFriction
        else:
            self.velocity.y += self.data.gravity
        self.rect.y += self.velocity.y
        self.hitbox.y += self.velocity.y
        return None

    def update(self) -> None:
        self.handleEvent()
        self.updateStatus()
        self.updateImage()
        self.effects.update()
        return None
