from pathlib import Path

import pygame

from .character import Character
from ..enums import FruitName
from ..utils import Utils


class Fruit(pygame.sprite.Sprite):

    # Constant
    image_size = (64, 64)
    hitbox_size = (30, 30)
    animation_speed = 30

    def __init__(self,
            position: tuple[float, float],
            images: list[pygame.Surface],
            collected_images: list[pygame.Surface]
        ) -> None:
        super().__init__()
        self.frame = 0
        self.images = images
        self.collected_images = collected_images
        self.collected = False
        self.image = self.images[self.frame]
        self.rect = self.image.get_frect()
        self.hitbox = pygame.FRect((0, 0), self.hitbox_size)
        self.rect.topleft = position
        self.hitbox.center = self.rect.center
        return None

    @classmethod
    def load_images(cls, root_path: Path, fruit: FruitName) -> list[pygame.Surface]:
        path = root_path / f'assets/images/items/fruits/{fruit.value}.png'
        return Utils.read_spritesheet(
            path=path, width=cls.image_size[0], height=cls.image_size[1]
        )

    def handle_player_collision(self, player: Character) -> None:
        if self.hitbox.colliderect(player.hitbox) and not self.collected:
            self.frame = 0
            self.collected = True
        return None

    def update(self, dt: float):
        self.frame += self.animation_speed * dt
        if not self.collected:
            frame_index = int(self.frame) % len(self.images)
            self.image = self.images[frame_index]
        else:
            frame_index = int(self.frame) % len(self.collected_images)
            self.image = self.collected_images[frame_index]
            if self.frame >= len(self.collected_images):
                self.kill()
        return None
