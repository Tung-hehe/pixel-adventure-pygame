import pygame

from Source.Utils import EffectData


class Effect(pygame.sprite.Sprite):

    def __init__(self,
            position: tuple,
            effectData: EffectData,
            relativePosition: str = "midbottom",
            rotation: int = 0,
            loop: int = 1,
        ) -> None:
        super().__init__()
        self.loop = loop
        self.data = effectData
        self.rotation = rotation
        self.image = self.data.animation[0]
        self.frameIndex = 0
        self.rect = self.image.get_rect(**{relativePosition: position})
        return None

    def updateImage(self) -> None:
        self.frameIndex += self.data.setting['animationSpeed']
        if self.frameIndex >= len(self.data.animation):
            self.frameIndex = 0
            self.loop -= 1
        self.image = self.data.animation[int(self.frameIndex)]
        self.image = pygame.transform.rotate(self.image, self.rotation)
        return None

    def update(self) -> None:
        self.updateImage()
        if self.loop == 0:
            self.kill()
        return None
