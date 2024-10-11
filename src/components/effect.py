import pygame

from ..enums import EffectName
from ..utils import Utils


class AnimatedEffect:

    image_size = {
        EffectName.Appearing: (84, 96),
        EffectName.Collected: (64, 64),
        EffectName.Desappearing: (84, 96),
    }

    @classmethod
    def load_images(cls, root_path, effect_name: EffectName):
        path = root_path / f'assets/images/effects/{effect_name.value}.png'
        return Utils.read_spritesheet(
            path=path, width=cls.image_size[effect_name][0], height=cls.image_size[effect_name][1]
        )
