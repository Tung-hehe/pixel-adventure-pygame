import random

from pathlib import Path

import pygame

from .character import Character
from .effect import Particle
from .timer import Timer

from ..enums import (
    Axis,
    Direction,
    PlatformStatus,
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
            if player.is_collision_with_static_object(self.rect, Direction.Right):
                player.hitbox.right = self.rect.left
            elif player.is_collision_with_static_object(self.rect, Direction.Left):
                player.hitbox.left = self.rect.right
        elif axis == Axis.Vertical:
            if player.is_collision_with_static_object(self.rect, Direction.Bottom):
                player.hitbox.bottom = self.rect.top
                player.jump_counter = 0
            elif player.is_collision_with_static_object(self.rect, Direction.Top):
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
            if player.is_collision_with_static_object(self.rect, Direction.Bottom):
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
    accelerator = 0.2
    max_velocity = 30
    particle_spawn_timer = 200
    turn_off_timer = 300
    gravity = 1200
    particle_velocity_range = (0.35, 0.45)
    particle_spawn_range = 20
    particle_velocity_range = [0.3, 0.5]
    particle_exist_timer = 400
    particle_scale_range = [1, 1.3]
    particle_alpha_range = [50, 100]
    def __init__(self,
            position: tuple[float, float],
            images: list[pygame.Surface],
            rect_orientation: str,
            particle_image: pygame.Surface
        ):
        self.images = images
        self.particle_image = particle_image
        self.frame = 0
        self.status = PlatformStatus.On
        surface = self.images[self.status][0]
        super().__init__(position, surface, rect_orientation)
        self.dust = pygame.sprite.Group()
        self.velocity = pygame.Vector2()
        self.direction = 1
        self.particle_spawn_timer = Timer(self.particle_spawn_timer, self.spawn_dust_particle, True)
        self.turn_off_timer = Timer(self.turn_off_timer, self.turn_off, False)
        self.particle_spawn_timer.activate()
        self.tracking_rect = self.rect.copy()
        self.limit = pygame.display.get_window_size()[1]
        return None

    def turn_off(self) -> None:
        self.frame = 0
        self.status = PlatformStatus.Off
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

    def handle_player_collision(self, player: Character, axis: Axis) -> None:
        if player.skip_platform:
            return None
        if axis == Axis.Horizontal:
            """Platform only supports semi-collision"""
        elif axis == Axis.Vertical:
            if player.is_collision_with_moving_object(self.rect, self.tracking_rect, Direction.Bottom):
                player.hitbox.bottom = self.rect.top
                player.jump_counter = 0
                player.velocity.y = 0
                if self.status == PlatformStatus.On and not self.turn_off_timer.active:
                    self.turn_off_timer.activate()
        else:
            raise ValueError(f'Invalid axis {axis}')
        return None

    def check_player_contact(self, player: Character, direction: Direction) -> bool:
        assert direction != Direction.Top
        if direction == Direction.Bottom:
            if self.rect.colliderect(player.contact_rect[direction]):
                player.following_object = self
            return self.rect.colliderect(player.contact_rect[direction])
        return False

    def move(self, dt) -> None:
        if self.status == PlatformStatus.On:
            self.velocity.y += self.direction * self.accelerator
            if abs(self.velocity.y) >= self.max_velocity:
                self.direction *= -1
            self.rect.y += self.velocity.y * dt
        else:
            self.velocity.y += self.gravity / 2 * dt
            self.rect.y += self.velocity.y * dt
            self.velocity.y += self.gravity / 2 * dt
        return None

    def spawn_dust_particle(self) -> None:
        position = self.rect.center[0] + random.uniform(-self.particle_spawn_range, self.particle_spawn_range)
        velocity = random.uniform(self.particle_velocity_range[0], self.particle_velocity_range[1])
        particle = Particle(
            surface=self.particle_image,
            position=(position, self.rect.bottom),
            veltocity=pygame.Vector2(0, velocity),
            timer=self.particle_exist_timer,
            scale=random.uniform(self.particle_scale_range[0], self.particle_scale_range[1]),
            alpha=random.randint(self.particle_alpha_range[0], self.particle_alpha_range[1])
        )
        self.dust.add(particle)
        return None

    def update(self, dt) -> None:
        self.tracking_rect.midbottom = self.rect.midbottom
        self.frame += self.animation_speed * dt
        frame_index = int(self.frame) % len(self.images[self.status])
        self.image = self.images[self.status][frame_index]
        if self.status == PlatformStatus.On:
            self.particle_spawn_timer.update()
        self.turn_off_timer.update()
        self.dust.update()
        if self.rect.top >= self.limit:
            self.kill()
        return None
