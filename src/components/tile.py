from pathlib import Path

import pygame

from .character import Character

from ..enums import (
    Axis,
    Direction,
    PlatformStatus
)
from ..utils import Utils


class Tile(pygame.sprite.Sprite):

    def __init__(self,
            position: tuple[float, float],
            surface: pygame.Surface,
            rect_orientation: str = 'topleft'
        ) -> None:
        super().__init__()
        self.image = surface
        self.rect = self.image.get_frect(**{rect_orientation: position})
        return None

    def handle_player_collision(self, player: Character, axis: Axis) -> None:
        raise NotImplementedError('Not implemented')

    def check_player_contact(self, player: Character, direction: Direction) -> None:
        raise NotImplementedError('Not implemented')


class Terrain(Tile):

    def __init__(self,
            position: tuple[float, float],
            surface: pygame.Surface,
            slidable: bool = False
        ) -> None:
        super().__init__(position, surface)
        self.slidable = slidable
        return None

    def handle_player_collision(self, player: Character, axis: Axis) -> None:
        if axis == Axis.Horizontal:
            if player.is_collision(self.rect, Direction.Right):
                player.hitbox.right = self.rect.left
            elif player.is_collision(self.rect, Direction.Left):
                player.hitbox.left = self.rect.right
        elif axis == Axis.Vertical:
            if player.is_collision(self.rect, Direction.Bottom):
                player.hitbox.bottom = self.rect.top
                player.jump_counter = 0
            elif player.is_collision(self.rect, Direction.Top):
                player.hitbox.top = self.rect.bottom
            player.velocity.y = 0
        else:
            raise ValueError(f'Invalid axis {axis}')
        return None

    def check_player_contact(self, player: Character, direction: Direction) -> bool:
        assert direction != Direction.Top
        if direction == Direction.Bottom:
            return self.rect.colliderect(player.contact_rect[direction])
        elif self.slidable:
            return self.rect.colliderect(player.contact_rect[direction]) and self.rect.top <= player.hitbox.top
        else:
            return False


class Platform(Tile):

    def __init__(self,
            position: tuple[float, float],
            surface: pygame.Surface,
            rect_orientation: str
        ) -> None:
        super().__init__(position, surface, rect_orientation)
        return None

    def handle_player_collision(self, player: Character, axis: Axis) -> None:
        if player.skip_platform:
            return None
        if axis == Axis.Horizontal:
            """Platform only supports semi-collision"""
        elif axis == Axis.Vertical:
            if player.is_collision(self.rect, Direction.Bottom):
                player.hitbox.bottom = self.rect.top
                player.jump_counter = 0
                player.velocity.y = 0
        else:
            raise ValueError(f'Invalid axis {axis}')
        return None

    def check_player_contact(self, player: Character, direction: Direction) -> bool:
        assert direction != Direction.Top
        if direction == Direction.Bottom:
            return self.rect.colliderect(player.contact_rect[direction])
        return False


class FallingPlatform(Platform):

    animation_speed = 10
    image_size = (64, 20)
    def __init__(self,
            position: tuple[float, float],
            images: list[pygame.Surface],
            rect_orientation: str
        ):
        self.images = images
        self.frame = 0
        self.status = PlatformStatus.On
        surface = self.images[self.status][0]
        super().__init__(position, surface, rect_orientation)
        self.dust = pygame.sprite.Group()
        return None

    @classmethod
    def load_images(cls, root_path: Path) -> None:
        path = root_path/ f'assets/images/tilesets/falling_platform'
        images = {
            status: Utils.read_spritesheet(
                path=path/f'{status.value}.png',
                width=cls.image_size[0],
                height=cls.image_size[1]
            ) for status in PlatformStatus
        }
        return images

    def update(self, dt):
        self.frame += self.animation_speed * dt
        frame_index = int(self.frame) % len(self.images)
        self.image = self.images[self.status][frame_index]
        return None
