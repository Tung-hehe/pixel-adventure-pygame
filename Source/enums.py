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
    DoubleJump = 'DoubleJump'
    WallJump = 'WallJump'

class CharacterFacing(Enum):
    Right = 'Right'
    Left = 'Left'

class CharacterRelativePosition(Enum):
    OnGround = 'OnGround'
    OnCeil = 'OnCeil'
    OnAir = 'OnAir'
    OnLeftWall = 'OnLeftWall'
    OnRightWall = 'OnRightWall'
