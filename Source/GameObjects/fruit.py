import pygame

from Source.Utils import FruitData


class Fruit(pygame.sprite.Sprite):

    def __init__(self, position: tuple, fruitData: FruitData) -> None:
        super().__init__()
        self.data = fruitData
        self.image = self.data.animation[0]
        self.frameIndex = 0
        self.rect = self.image.get_rect(bottomleft=position)
        self.hitbox = pygame.Rect(position, self.data.hitbox)
        self.hitbox.center = self.rect.center
        return None

    def updateImage(self):
        self.frameIndex += self.data.animationSpeed
        if self.frameIndex >= len(self.data.animation):
            self.frameIndex = 0
        self.image = self.data.animation[int(self.frameIndex)]
        return None

    def update(self) -> None:
        self.updateImage()
        return None
