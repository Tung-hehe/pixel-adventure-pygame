from pathlib import Path

import pygame
import pytmx

from .tile import (
    StaticPlatform,
    Terrain,
)
from .background import Background
from .character import Character
from ..enums import (
    Axis,
    Direction,
)


class Map:

    def __init__(self) -> None:
        self.tiles = []
        self.player = None
        self.background = None
        return None

    def setup(self,
            map_data_path: Path,
            player: Character,
            background: Background
        ) -> None:
        map_data = pytmx.load_pygame(map_data_path)
        self.background = background
        for layer in map_data.layers:
            if layer.name == 'terrain':
                for x, y, surface in layer.tiles():
                    self.tiles.append(Terrain((
                        x * map_data.tilewidth,
                        (y + 1) * map_data.tileheight
                    ), surface))
            elif layer.name == 'static_platform':
                for x, y, surface in layer.tiles():
                    self.tiles.append(StaticPlatform((
                        x * map_data.tilewidth,
                        (y + 1) * map_data.tileheight
                    ), surface))
            elif layer.name == 'character':
                assert len(layer) == 1
                self.player = player
                self.player.set_init_postion((layer[0].x, layer[0].y))
        return None

    def handle_player_tile_collision(self, axis: Axis) -> None:
        for tile in self.tiles:
            if not tile.rect.colliderect(self.player.hitbox):
                continue
            tile.handle_player_collision(self.player, axis)
        return None

    def handel_player_contact(self) -> None:
        for direction in Direction:
            if direction == Direction.Top:
                continue
            self.player.contact_checker[direction] = False
        for tile in self.tiles:
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
        self.background.update(dt)
        self.player.move(dt, Axis.Horizontal)
        self.handle_player_tile_collision(Axis.Horizontal)
        self.player.move(dt, Axis.Vertical)
        self.handle_player_tile_collision(Axis.Vertical)
        self.handel_player_contact()
        self.player.update()
        self.player.update_image(dt)
        return None

    def draw(self, screen: pygame.Surface) -> None:
        self.background.draw(screen)
        for tile in self.tiles:
            tile.draw(screen)
        self.player.draw(screen)
        return None
