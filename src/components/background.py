from pathlib import Path

import pygame

from .sprite import Sprite


class Background(Sprite):

    image_size = (128, 128)
    scroll_speed = 1

    def __init__(self, image: pygame.Surface) -> None:
        self.image = image
        self.start_position = -1
        return None

    @classmethod
    def read_image(cls, path: Path) -> pygame.Surface:
        image = pygame.image.load(path).convert_alpha()
        image = pygame.transform.scale(image, cls.image_size)
        return image

    def update(self, dt: float) -> None:
        self.start_position += self.scroll_speed * dt
        if self.start_position >= 0:
            self.start_position = -1
        return None

    def draw(self, screen: pygame.Surface) -> None:
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        current_position = self.start_position * self.image_size[1]
        cols = screen_width // self.image_size[0]
        while current_position < screen_height:
            for col in range(cols):
                screen.blit(self.image, (col * self.image_size[0], current_position))
            current_position += self.image_size[1]
        return None