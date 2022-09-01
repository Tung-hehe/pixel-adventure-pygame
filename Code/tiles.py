import pygame

class Tile(pygame.sprite.Sprite):

    def __init__(self, position, size) -> None:
        super().__init__()
        self.image = pygame.Surface(size)
        self.image.fill('#6E85B7')
        self.rect = self.image.get_rect(topleft=position)
