import pygame


class Sprite(pygame.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()
        return None

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect.topleft)
        return None
