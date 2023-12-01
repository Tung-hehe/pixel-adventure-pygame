import pygame

from Source.Utils import (
    BackgroundAssets,
    BackgroundSettings
)


class Background(pygame.sprite.Sprite):

    def __init__(self,
            backgroundAssets: BackgroundAssets,
            backgroundSettings: BackgroundSettings,
        ) -> None:
        self.assets = backgroundAssets
        self.settings = backgroundSettings
        self.width = self.assets.image.get_width()
        self.height = self.assets.image.get_height()
        self.position = -1
        return None

    def scroll(self) -> None:
        self.position += self.settings.scrollSpeed
        if self.position >= 0:
            self.position = -1
        return None

    def draw(self, screen: pygame.Surface) -> None:
        screenWidth = screen.get_width()
        screenHeight = screen.get_height()
        currentPosition = self.position * self.height
        cols = screenWidth // self.width
        while currentPosition < screenHeight:
            for col in range(cols):
                screen.blit(self.assets.image, (col*self.width, currentPosition))
            currentPosition += self.height
        return None
