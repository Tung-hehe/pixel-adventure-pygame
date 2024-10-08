import random
import sys

from pathlib import Path

import pygame

from .components import (
    Background,
    Character,
    Map
)
from .enums import (
    BackgroundName,
    CharacterName
)


class Game:

    # Constants
    game_name = "Pixel adventure"
    start_map = "data/maps/map_01.tmx"
    screen_size = (1024, 576)

    def __init__(self) -> None:
        pygame.init()
        self.root_path = Path(__file__).absolute().parents[1]
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption(self.game_name)
        self.clock = pygame.time.Clock()
        character_name = random.choice(list(CharacterName))
        character_images = Character.read_images(
            self.root_path / f'assets/images/characters/{character_name.value}'
        )
        player = Character(character_images)
        character_name = random.choice(list(CharacterName))
        character_images = Character.read_images(
            self.root_path / f'assets/images/characters/{character_name.value}'
        )
        background_name = random.choice(list(BackgroundName))
        background_image = Background.read_image(
            self.root_path / f'assets/images/backgrounds/{background_name.value}.png'
        )
        background = Background(background_image)
        self.map = Map()
        self.map.setup(self.root_path / self.start_map, player, background)
        return None

    def change_map(self) -> None:
        return None

    def quit(self) -> None:
        pygame.quit()
        sys.exit()
        return None

    def run(self) -> None:
        while 1:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.quit()
                if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
                    if event.key == pygame.K_ESCAPE: self.quit()
                    if event.key in [pygame.K_a, pygame.K_d, pygame.K_s, pygame.K_w]:
                        self.map.handle_input_event(event)
            self.screen.fill('black')
            self.map.update(dt)
            self.map.draw(self.screen)
            pygame.display.update()
        return None
