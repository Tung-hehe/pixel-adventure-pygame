from pathlib import Path

from Source.enums import CharacterNames


class CharacterSettings:
    def __init__(self,
            runSpeed: float,
            fallSpeed: float,
            jumpSpeed: float,
            hitboxWidth: int,
            hitboxHeight: int,
            animationSpeed: float,
            spriteWidth: int,
            spriteHeight: int,
            spritesheetsFolderPath: Path,
        ) -> None:
        self.runSpeed = runSpeed
        self.fallSpeed = fallSpeed
        self.jumpSpeed = jumpSpeed
        self.hitboxWidth = hitboxWidth
        self.hitboxHeight = hitboxHeight
        self.animationSpeed = animationSpeed
        self.spriteWidth = spriteWidth
        self.spriteHeight = spriteHeight
        self.spritesheetsFolderPath = spritesheetsFolderPath
        return None

currentDirPath = Path(__file__).absolute().parents[2]

AllCharacterSettings = {
    characterName: CharacterSettings(
        runSpeed=5,
        fallSpeed=0.8,
        jumpSpeed=-16,
        hitboxWidth=40,
        hitboxHeight=50,
        spriteWidth=32,
        spriteHeight=32,
        animationSpeed=0.25,
        spritesheetsFolderPath=currentDirPath/f'Assets/Image/MainCharacters/{characterName.value}',
    ) for characterName in CharacterNames
}
