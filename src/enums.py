from enum import (
    auto, Enum
)


class Axis(Enum):
    Horizontal = auto()
    Vertical = auto()

class BackgroundName(Enum):
    Blue = 'blue'
    Brown = 'brown'
    Gray = 'gray'
    Green = 'green'
    Pink = 'pink'
    Purple = 'purple'
    Yellow = 'yellow'

class CharacterFacing(Enum):
    Left = auto()
    Right = auto()

class CharacterName(Enum):
    MaskDude = 'mask_dude'
    NinjaFrog = 'ninja_frog'
    PinkMan = 'pink_man'
    VirtualGuy = 'virtual_guy'

class CharacterStatus(Enum):
    AirJump = 'air_jump'
    Fall = 'fall'
    Hit = 'hit'
    Idle = 'idle'
    Jump = 'jump'
    Run = 'run'
    WallSlide = 'wall_slide'

class Direction(Enum):
    Left = auto()
    Right = auto()
    Top = auto()
    Bottom = auto()

class Fruit(Enum):
    Apple = 'apple'
    Bananas = 'bananas'
    Cherries = 'cherries'
    Kiwi = 'kiwi'
    Melon = 'melon'
    Orange = 'orange'
    Pineapple = 'pineapple'
    Strawberry = 'strawberry'
