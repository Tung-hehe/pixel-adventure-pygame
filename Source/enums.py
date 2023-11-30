from enum import Enum


class CharacterNames(Enum):
    PinkMan = 'PinkMan'
    MaskDude = 'MaskDude'
    NinjaFrog = 'NinjaFrog'
    VirtualGuy = 'VirtualGuy'


class CharacterStatus(Enum):
    Idle = 'Idle'
    Run = 'Run'
    Jump = 'Jump'
    Fall = 'Fall'
    Hit = 'Hit'
    JumpOnAir = 'JumpOnAir'
    ClingWal = 'ClingWall'

class CharacterFacing(Enum):
    Right = 'Right'
    Left = 'Left'

class CharacterRelativePosition(Enum):
    OnGround = 'OnGround'
    OnAir = 'OnAir'
    OnWall = 'OnWall'

class TilesetNames(Enum):
    Terrain = 'Terrain'
