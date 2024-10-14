from pathlib import Path

import random

import pygame
import pytmx

from .tile import (
    FallingPlatform,
    Platform,
    Terrain,
)
from .background import Background
from .character import Character
from .effect import (
    AnimatedEffect,
    Particle
)
from .item import Fruit
from ..enums import (
    Axis,
    Direction,
    ParticleName,
    EffectName,
    FruitName,
)


class Map:

    def __init__(self, root_path: Path) -> None:
        self.root_path = root_path
        self.static_tiles = pygame.sprite.Group()
        self.dynamic_tiles = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.player = None
        self.background = None
        self.objects_images = {
            'effect': self.load_effect_images(),
            'particle': self.load_particle_images()
        }
        return None

    def load_effect_images(self) -> dict[EffectName, pygame.Surface]:
        return {
            effect_name: AnimatedEffect.load_images(self.root_path, effect_name)
            for effect_name in EffectName
        }

    def load_particle_images(self) -> dict[ParticleName, pygame.Surface]:
        return {
            particle_name: Particle.load_image(self.root_path, particle_name)
            for particle_name in ParticleName
        }

    def setup(self, map_data_path: str, player: Character, background: Background) -> None:
        map_data_path = self.root_path / map_data_path
        map_data = pytmx.load_pygame(map_data_path)
        self.background = background
        self.static_tiles.empty()
        self.items.empty()
        for layer in map_data.layers:
            if 'terrain' in layer.name:
                self.set_up_terrain(layer, map_data.tilewidth, map_data.tileheight)
            elif layer.name == 'static_platform':
                self.set_up_static_platform(layer, map_data.tilewidth, map_data.tileheight)
            elif layer.name == 'falling_platform':
                self.set_up_falling_platform(layer)
            elif layer.name == 'character':
                self.set_up_player(layer, player)
            elif layer.name == 'fruit':
                self.set_up_fruit(layer)
        return None

    def set_up_terrain(self, layer: pytmx.pytmx.TiledTileLayer, tilewidth: float, tileheight: float) -> None:
        slidable = 'slidable' in layer.name
        for x, y, surface in layer.tiles():
            self.static_tiles.add(Terrain((x * tilewidth, y * tileheight), surface, slidable))
        return None

    def set_up_static_platform(self, layer: pytmx.pytmx.TiledTileLayer, tilewidth: float, tileheight: float) -> None:
        for x, y, surface in layer.tiles():
            self.static_tiles.add(
                Platform((x * tilewidth, (y + 1) * tileheight), surface, 'bottomleft')
            )
        return None

    def set_up_falling_platform(self, layer: pytmx.pytmx.TiledTileLayer) -> None:
        if layer.name not in self.objects_images:
            self.objects_images[layer.name] = FallingPlatform.load_images(self.root_path)
        for position in layer:
            self.dynamic_tiles.add(FallingPlatform(
                (position.x, position.y), self.objects_images[layer.name], 'topleft')
            )
        return None

    def set_up_player(self, layer: pytmx.pytmx.TiledGroupLayer, player: Character) -> None:
        assert len(layer) == 1
        self.player = player
        self.player.set_init_postion((layer[0].x, layer[0].y))
        return None

    def set_up_fruit(self, layer: pytmx.pytmx.TiledGroupLayer) -> None:
        if layer.name not in self.objects_images:
            self.objects_images |= {
                fruit_name: Fruit.load_images(self.root_path, fruit_name)
                for fruit_name in FruitName
            }
        fruit_name = random.choice(list(FruitName))
        for position in layer:
            fruit_name = random.choice(list(FruitName))
            self.items.add(Fruit(
                (position.x, position.y),
                self.objects_images[fruit_name],
                self.objects_images['effect'][EffectName.Collected]
            ))
        return None

    def handle_player_tile_collision(self, axis: Axis) -> None:
        for tile in self.static_tiles.sprites() + self.dynamic_tiles.sprites():
            if not tile.rect.colliderect(self.player.hitbox):
                continue
            tile.handle_player_collision(self.player, axis)
        return None

    def handle_player_item_collision(self) -> None:
        for item in self.items.sprites():
            item.handle_player_collision(self.player)
        return None

    def handle_player_contact(self) -> None:
        # Reset contact_checker
        for direction in Direction:
            if direction != Direction.Top:
                self.player.contact_checker[direction] = False
        for tile in self.static_tiles.sprites() + self.dynamic_tiles.sprites():
            for direction in Direction:
                if direction == Direction.Top:
                    continue
                if tile.check_player_contact(self.player, direction):
                    self.player.contact_checker[direction] = True
        return None

    def handle_input_event(self, event):
        self.player.handle_input_event(event)
        return None

    def update(self, dt: float) -> None:
        self.player.move(dt, Axis.Horizontal)
        self.handle_player_tile_collision(Axis.Horizontal)
        self.player.move(dt, Axis.Vertical)
        self.handle_player_tile_collision(Axis.Vertical)
        self.handle_player_contact()
        self.handle_player_item_collision()
        self.background.update(dt)
        self.dynamic_tiles.update(dt)
        self.player.update(dt)
        self.items.update(dt)
        return None

    def draw(self, screen: pygame.Surface) -> None:
        self.background.draw(screen)
        self.static_tiles.draw(screen)
        self.dynamic_tiles.draw(screen)
        self.player.draw(screen)
        self.items.draw(screen)
        return None
