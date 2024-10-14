from pathlib import Path

import pygame

from ..enums import (
    Axis,
    Direction,
    CharacterName,
    CharacterStatus,
    Direction,
)
from ..utils import Utils


class Character(pygame.sprite.Sprite):

    # Constants
    animation_speed = 20
    max_velocity = 250
    accerleration = 3
    jump_velocity = 375
    air_jump_velocity = 400
    wall_jump_velocity = pygame.Vector2(400, 200)
    wall_jump_accerleration = 3
    max_consecutive_jump = 2
    gravity = 1000
    wall_friction = 900
    image_size = (64, 64)
    hitbox_size = (36, 50)

    def __init__(self,
            images: dict[CharacterStatus: dict[Direction, list[pygame.Surface]]],
        ) -> None:
        super().__init__()
        # Render
        self.images = images
        self.image = pygame.Surface(self.image_size)
        self.rect = self.image.get_frect()
        self.frame = 0

        # Collision
        self.hitbox = pygame.FRect((0, 0), self.hitbox_size)
        self.tracking_rect = self.hitbox.copy()
        self.skip_platform = False
        self.contact_rect = {
            Direction.Right: pygame.FRect((0, 0), (1, self.hitbox.height)),
            Direction.Left: pygame.FRect((0, 0), (1, self.hitbox.height)),
            Direction.Bottom: pygame.FRect((0, 0), (self.hitbox.width, 1)),
        }
        self.contact_checker = {direction: False for direction in self.contact_rect.keys()}

        # Movement
        self.velocity = pygame.Vector2()
        self.jump_counter = 0
        self.accerleration_direction = {Direction.Right: False, Direction.Left: False}
        self.wall_jumping = False

        # Status
        self.status = None
        self.facing = Direction.Right
        return None

    @classmethod
    def load_images(cls,
            root_path: Path,  character_name: CharacterName
        ) -> dict[CharacterStatus: dict[Direction, list[pygame.Surface]]]:
        images = {
            status: {facing: [] for facing in Direction}
            for status in CharacterStatus
        }
        path = root_path/ f'assets/images/characters/{character_name.value}'
        for status in images.keys():
            status_path = path / f'{status.value}.png'
            images[status][Direction.Right] = Utils.read_spritesheet(
                path=status_path, width=cls.image_size[0], height=cls.image_size[1]
            )
            images[status][Direction.Left] = [
                pygame.transform.flip(
                    surface=image, flip_x=True, flip_y=False
                ) for image in images[status][Direction.Right]
            ]
        return images

    def set_init_postion(self, position: tuple[float]) -> None:
        self.rect.topleft = position
        self.hitbox.midbottom = self.rect.midbottom
        self.tracking_rect.midbottom = self.hitbox.midbottom
        self.update_collision_direction_checker_rect()
        return None

    def handle_input_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.accerleration_direction[Direction.Left] = True
            elif event.key == pygame.K_d:
                self.accerleration_direction[Direction.Right] = True
            elif event.key == pygame.K_s:
                self.skip_platform = True
            elif event.key == pygame.K_w:
                self.jump()
        else:
            if event.key == pygame.K_a:
                self.accerleration_direction[Direction.Left] = False
            elif event.key == pygame.K_d:
                self.accerleration_direction[Direction.Right] = False
            elif event.key == pygame.K_s:
                self.skip_platform = False
        return None

    def jump(self) -> None:
        if self.jump_counter >= self.max_consecutive_jump:
            return None
        self.frame = 0
        self.jump_counter = self.jump_counter + 1
        if self.status == CharacterStatus.WallSlide:
            self.wall_jumping = True
            self.velocity.y = -self.wall_jump_velocity.y
            if self.facing == Direction.Right:
                self.velocity.x = self.wall_jump_velocity.x
            else:
                self.velocity.x = -self.wall_jump_velocity.x
        else:
            if self.jump_counter == 1:
                self.velocity.y = -self.jump_velocity
            else:
                self.velocity.y = -self.air_jump_velocity
        return None

    def horizontal_move(self, dt: float) -> None:
        if not self.wall_jumping:
            accerleration_sign = (
                self.accerleration_direction[Direction.Right] - self.accerleration_direction[Direction.Left]
            )
            self.velocity.x += self.accerleration * accerleration_sign
            self.velocity.x = min(abs(self.velocity.x), self.max_velocity) * accerleration_sign
        else:
            if self.facing == Direction.Right:
                self.velocity.x -= self.wall_jump_accerleration
                if self.velocity.x <= 0:
                    self.wall_jumping = False
            else:
                self.velocity.x += self.wall_jump_accerleration
                if self.velocity.x >= 0:
                    self.wall_jumping = False
        self.hitbox.x += self.velocity.x * dt
        return None

    def vertical_move(self, dt: float) -> None:
        if self.status != CharacterStatus.WallSlide:
            self.velocity.y += self.gravity / 2 * dt
            self.hitbox.y += self.velocity.y * dt
            self.velocity.y += self.gravity / 2 * dt
        else:
            self.velocity.y += (self.gravity - self.wall_friction) / 2 * dt
            self.hitbox.y += self.velocity.y * dt
            self.velocity.y += (self.gravity - self.wall_friction) / 2 * dt
        return None

    def move(self, dt: float, axis: Axis) -> None:
        if axis == Axis.Horizontal:
            self.horizontal_move(dt)
        elif axis == Axis.Vertical:
            self.vertical_move(dt)
        else:
            raise ValueError(f'Invalid axis {axis}')
        return None

    def update_collision_direction_checker_rect(self) -> None:
        self.contact_rect[Direction.Right].midleft = self.hitbox.midright
        self.contact_rect[Direction.Left].midright = self.hitbox.midleft
        self.contact_rect[Direction.Bottom].midtop = self.hitbox.midbottom
        return None

    def update_status(self) -> None:
        if not self.wall_jumping:
            if self.accerleration_direction[Direction.Right]:
                self.facing = Direction.Right
            elif self.accerleration_direction[Direction.Left]:
                self.facing = Direction.Left
        if self.contact_checker[Direction.Bottom]:
            if self.velocity.x == 0: self.status = CharacterStatus.Idle
            else: self.status = CharacterStatus.Run
        else:
            if self.velocity.y < 0:
                if self.jump_counter == 1: self.status = CharacterStatus.Jump
                elif self.jump_counter > 1: self.status = CharacterStatus.AirJump
                else:
                    raise ValueError('Jump counter must be greater than 0 if vertical velocity smaller than 0')
            else:
                if self.contact_checker[Direction.Right] ^ self.contact_checker[Direction.Left]:
                    self.status = CharacterStatus.WallSlide
                    if self.contact_checker[Direction.Right]: self.facing = Direction.Left
                    else: self.facing = Direction.Right
                    self.jump_counter = 0
                else:
                    self.status = CharacterStatus.Fall
        return None

    def update_image(self, dt: float) -> None:
        self.frame += self.animation_speed * dt
        frame_index = int(self.frame) % len(self.images[self.status][self.facing])
        self.image = self.images[self.status][self.facing][frame_index]
        if self.frame >= len(self.images[self.status][self.facing]):
            self.frame = 0
        return None

    def update(self, dt: float) -> None:
        self.update_collision_direction_checker_rect()
        self.rect.midbottom = self.hitbox.midbottom
        self.tracking_rect.midbottom = self.hitbox.midbottom
        self.update_status()
        self.update_image(dt)
        return None

    def is_collision(self, object_rect: pygame.FRect, direction: Direction) -> bool:
        if direction == Direction.Right:
            return self.hitbox.right >= object_rect.left and self.tracking_rect.right <= object_rect.left
        elif direction == Direction.Left:
            return self.hitbox.left <= object_rect.right and self.tracking_rect.left >= object_rect.right
        elif direction == Direction.Top:
            return self.hitbox.top <= object_rect.bottom and self.tracking_rect.top >= object_rect.bottom
        elif direction == Direction.Bottom:
            return self.hitbox.bottom >= object_rect.top and self.tracking_rect.bottom <= object_rect.top
        else:
            raise ValueError(f'Invalid dicrection {direction}')

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect.topleft)
        return None
