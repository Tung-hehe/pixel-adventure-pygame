from Source.enums import CharacterNames


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
            frictionwithWall: float
        ) -> None:
        self.runSpeed = runSpeed
        self.gravity = gravity
        self.jumpSpeed = jumpSpeed
        self.hitboxWidth = hitboxWidth
        self.hitboxHeight = hitboxHeight
        self.animationSpeed = animationSpeed
        self.frictionwithWall = frictionwithWall

        assert limitJumpOnAir == len(jumpOnAirSpeed)
        self.limitJumpOnAir = limitJumpOnAir
        self.jumpOnAirSpeed = jumpOnAirSpeed
        return None


class Settings:

    def __init__(self):
        self.characters = self.getAllCharacterSettings()
        return None

    def getAllCharacterSettings(self) -> dict[CharacterNames, CharacterSettings]:
        charactersSettings = {
            characterName: CharacterSettings(
                runSpeed=5,
                gravity=0.8,
                jumpSpeed=-16,
                hitboxWidth=40,
                hitboxHeight=50,
                animationSpeed=0.25,
                limitJumpOnAir=1,
                jumpOnAirSpeed=[-14],
                frictionwithWall=0.6,
            ) for characterName in CharacterNames
        }
        return charactersSettings
