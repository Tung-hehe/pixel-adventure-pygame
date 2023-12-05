import pygame

from Source.Utils import BackgroundData


class Background(pygame.sprite.Sprite):

    def __init__(self, data: BackgroundData) -> None:
        self.data = data
        self.position = -1
        return None

    def scroll(self) -> None:
        self.position += self.data.scrollSpeed
        if self.position >= 0:
            self.position = -1
        return None

    def draw(self, screen: pygame.Surface) -> None:
        screenWidth = screen.get_width()
        screenHeight = screen.get_height()
        currentPosition = self.position * self.data.height
        cols = screenWidth // self.data.width
        while currentPosition < screenHeight:
            for col in range(cols):
                screen.blit(self.data.image, (col*self.data.width, currentPosition))
            currentPosition += self.data.height
        return None
