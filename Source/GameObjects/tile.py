import pygame


class Tile(pygame.sprite.Sprite):

    def __init__(self, position, surface: pygame.Surface) -> None:
        super().__init__()
        self.image = surface
        self.rect = self.image.get_rect(topleft=position)
        return None

class StaticTile(Tile):

    def __init__(self, position, surface: pygame.Surface) -> None:
        super().__init__(position, surface)
