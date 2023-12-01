from Source.enums import (
    CharacterName,
    BackgroundName
)


class CharacterSettings:
    def __init__(self,
            runSpeed: float,
            gravity: float,
            jumpSpeed: float,
            hitboxWidth: int,
            hitboxHeight: int,
            animationSpeed: float,
            limitJumpOnAir: int,
            jumpOnAirSpeed: list[float],
        ) -> None:
        self.runSpeed = runSpeed
        self.gravity = gravity
        self.jumpSpeed = jumpSpeed
        self.hitboxWidth = hitboxWidth
        self.hitboxHeight = hitboxHeight
        self.animationSpeed = animationSpeed
        assert limitJumpOnAir == len(jumpOnAirSpeed)
        self.limitJumpOnAir = limitJumpOnAir
        self.jumpOnAirSpeed = jumpOnAirSpeed
        return None


class BackgroundSettings:
    def __init__(self, scrollSpeed: float):
        assert 0 <= scrollSpeed <= 1
        self.scrollSpeed = scrollSpeed


class Settings:

    def __init__(self):
        self.characters = self.getAllCharacterSettings()
        self.backgrounds = self.getAllBackgroundSettings()
        return None

    def getAllCharacterSettings(self) -> dict[CharacterName, CharacterSettings]:
        charactersSettings = {
            characterName: CharacterSettings(
                runSpeed=5,
                gravity=0.8,
                jumpSpeed=-16,
                hitboxWidth=40,
                hitboxHeight=50,
                animationSpeed=0.25,
                limitJumpOnAir=1,
                jumpOnAirSpeed=[-14]
            ) for characterName in CharacterName
        }
        return charactersSettings

    def getAllBackgroundSettings(self) -> dict[BackgroundName, BackgroundSettings]:
        bacgroundsSettings = {
            backgroundName: BackgroundSettings(
                scrollSpeed=0.02
            ) for backgroundName in BackgroundName
        }
        return bacgroundsSettings
