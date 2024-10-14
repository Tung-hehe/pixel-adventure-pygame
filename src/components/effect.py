import pygame

from .timer import Timer
from ..enums import (
    EffectName,
    ParticleName
)
from ..utils import Utils


class AnimatedEffect:

    image_size = {
        EffectName.Appearing: (84, 96),
        EffectName.Collected: (64, 64),
        EffectName.Disappearing: (84, 96),
    }

    @classmethod
    def load_images(cls, root_path, effect_name: EffectName):
        path = root_path / f'assets/images/effects/{effect_name.value}.png'
        return Utils.read_spritesheet(
            path=path, width=cls.image_size[effect_name][0], height=cls.image_size[effect_name][1]
        )

class Particle(pygame.sprite.Sprite):

    alpha = 80
    def __init__(self,
            surface: pygame.Surface,
            position: tuple[float, float],
            veltocity: pygame.Vector2,
            timer: float = 500,
            scale: float = 1,
        ) -> None:
        super().__init__()
        self.image = surface
        self.velocity = veltocity
        self.timer = Timer(duration=timer)
        pygame.transform.scale(self.image, (scale * self.image.width, scale * self.image.height))
        self.rect = self.image.get_frect()
        self.rect.topleft = position
        self.timer.activate()
        return None

    @classmethod
    def load_image(cls, root_path, particle_name: ParticleName):
        path = root_path / f'assets/images/effects/particle/{particle_name.value}.png'
        image = pygame.image.load(path).convert_alpha()
        image.set_alpha(cls.alpha)
        return image

    def update(self) -> None:
        self.rect.center += self.velocity
        self.timer.update()
        if not self.timer.active:
            self.kill()
        return None
