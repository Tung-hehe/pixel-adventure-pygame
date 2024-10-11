from pathlib import Path

import random

import pygame
import pytmx

from .tile import (
    StaticPlatform,
    Terrain,
)
from .background import Background
from .character import Character
from .effect import AnimatedEffect
from .item import Fruit
from ..enums import (
    Axis,
    Direction,
    EffectName,
    FruitName,
)


class Map:

    def __init__(self, root_path: Path) -> None:
        self.root_path = root_path
        self.tiles = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.player = None
        self.background = None
        self.objects_images = {'effect': self.load_effect_images()}
        return None

    def load_effect_images(self) -> None:
        effect_images = {
            effect_name: AnimatedEffect.load_images(self.root_path, effect_name) for effect_name in EffectName
        }
        return effect_images

    def setup(self, map_data_path: str, player: Character, background: Background) -> None:
        map_data_path = self.root_path / map_data_path
        map_data = pytmx.load_pygame(map_data_path)
        self.background = background
        self.tiles.empty()
        self.items.empty()
        for layer in map_data.layers:
            if layer.name == 'terrain':
                self.set_up_terrain(layer, map_data.tilewidth, map_data.tileheight)
            elif layer.name == 'static_platform':
                self.set_up_static_platform(layer, map_data.tilewidth, map_data.tileheight)
            elif layer.name == 'character':
                self.set_up_player(layer, player)
            elif layer.name == 'fruit':
                self.set_up_fruit(layer)
        return None

    def set_up_terrain(self, layer: pytmx.pytmx.TiledTileLayer, tilewidth: float, tileheight: float) -> None:
        for x, y, surface in layer.tiles():
            self.tiles.add(Terrain((x * tilewidth, (y + 1) * tileheight), surface))
        return None

    def set_up_static_platform(self, layer: pytmx.pytmx.TiledTileLayer, tilewidth: float, tileheight: float) -> None:
        for x, y, surface in layer.tiles():
            self.tiles.add(StaticPlatform((x * tilewidth, (y + 1) * tileheight), surface))
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
        for tile in self.tiles.sprites():
            if not tile.rect.colliderect(self.player.hitbox):
                continue
            tile.handle_player_collision(self.player, axis)
        return None

    def handle_player_item_collision(self) -> None:
        for item in self.items.sprites():
            item.handle_player_collision(self.player)
        return None

    def handel_player_contact(self) -> None:
        for direction in Direction:
            if direction == Direction.Top:
                continue
            self.player.contact_checker[direction] = False
        for tile in self.tiles.sprites():
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
        self.handel_player_contact()
        self.handle_player_item_collision()
        self.background.update(dt)
        self.player.update(dt)
        self.items.update(dt)
        return None

    def draw(self, screen: pygame.Surface) -> None:
        self.background.draw(screen)
        self.tiles.draw(screen)
        self.player.draw(screen)
        self.items.draw(screen)
        return None
