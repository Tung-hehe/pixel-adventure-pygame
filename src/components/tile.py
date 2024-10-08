import pygame

from .character import Character

from .sprite import Sprite
from ..enums import (
    Axis,
    Direction,
)


class Tile(Sprite):

    def __init__(self,
            position: tuple[float, float],
            surface: pygame.Surface,
        ) -> None:
        super().__init__()
        self.image = surface
        self.rect = self.image.get_frect(bottomleft=position)
        return None

    def handle_player_collision(self, player: Character, axis: Axis) -> None:
        raise NotImplementedError('Not implemented')

    def check_player_contact(self, player: Character, direction: Direction) -> None:
        raise NotImplementedError('Not implemented')

class Terrain(Tile):

    def __init__(self,
            position: tuple[float, float],
            surface: pygame.Surface,
        ) -> None:
        super().__init__(position, surface)
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
        else:
            return self.rect.colliderect(player.contact_rect[direction]) and self.rect.top <= player.hitbox.top

class Platform(Tile):

    def __init__(self,
            position: tuple[float, float],
            surface: pygame.Surface,
        ) -> None:
        super().__init__(position, surface)
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

class StaticPlatform(Platform):

    def __init__(self,
            position: tuple[float, float],
            surface: pygame.Surface,
        ) -> None:
        super().__init__(position, surface)
        return None
