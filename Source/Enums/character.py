from enum import Enum


class CharacterName(Enum):
    PinkMan = 'PinkMan'
    MaskDude = 'MaskDude'
    NinjaFrog = 'NinjaFrog'
    VirtualGuy = 'VirtualGuy'


class CharacterStatus(Enum):
    ClingWall = 'ClingWall'
    Fall = 'Fall'
    Hit = 'Hit'
    Idle = 'Idle'
    Jump = 'Jump'
    JumpOnAir = 'JumpOnAir'
    Run = 'Run'


class CharacterFacing(Enum):
    Right = 'Right'
    Left = 'Left'


class CharacterRelativePosition(Enum):
    OnGround = 'OnGround'
    OnAir = 'OnAir'
    OnWall = 'OnWall'
    OnObject = 'OnObject'
