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


class TilesetName(Enum):
    Terrain = 'Terrain'


class BackgroundName(Enum):
    Blue = 'Blue'
    Brown = 'Brown'
    Gray = 'Gray'
    Green = 'Green'
    Pink = 'Pink'
    Purple = 'Purple'
    Yellow = 'Yellow'

class FruitName(Enum):
    Apple = 'Apple'
    Bananas = 'Bananas'
    Cherries = 'Cherries'
    Kiwi = 'Kiwi'
    Melon = 'Melon'
    Orange = 'Orange'
    Pineapple = 'Pineapple'
    Strawberry = 'Strawberry'

class EffectName(Enum):
    Run = "Run"
    Jump = "Jump"
    Land = "Land"
    CollectFruit = "CollectFruit"


class EnemyName(Enum):
    AngryPig = 'AngryPig'
    Bat = 'Bat'
    Bee = 'Bee'
    BlueBird = 'BlueBird'
    Bunny = 'Bunny'
    Chameleon = 'Chameleon'
    Chicken = 'Chicken'
    Duck = 'Duck'
    FatBird = 'FatBird'
    Ghost = 'Ghost'
    Mushroom = 'Mushroom'
    Plant = 'Plant'
    Radish = 'Radish'
    Rino = 'Rino'
    BigRock = 'BigRock'
    MediumRock = 'MediumRock'
    SmallRock = 'SmallRock'
    Skull = 'Skull'
    Slime = 'Slime'
    Snail = 'Snail'
    Trunk = 'Trunk'
    Turtle = 'Turtle'
