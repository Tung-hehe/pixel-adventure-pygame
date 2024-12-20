import json

from pathlib import Path

import pygame


class Utils:

    @classmethod
    def read_json(cls, path: Path) -> dict[str, dict]:
        with open(path, 'r') as f:
            dataDict = json.load(f)
        return dataDict

    @classmethod
    def read_spritesheet(cls,
            path: Path, width: int, height: int, scale: int = 1
        ) -> list[pygame.Surface]:
        assert width > 0
        assert height > 0
        assert scale > 0

        spritesheets = pygame.image.load(path).convert_alpha()
        nFrame = spritesheets.get_width() // width

        surfaceList = []
        for frame in range(nFrame):
            # pygame.SRCALPHA to invisible background
            surface = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
            surface.blit(spritesheets, (0, 0), (width * frame, 0, width, height))
            if scale > 1:
                surface = pygame.transform.scale(surface, (width * scale, height * scale))
            surfaceList.append(surface)
        return surfaceList


class Comparison:

    @classmethod
    def equal(cls, lhs: float|int, rhs: float|int, *, epsilon: float = 1e-3) -> bool:
        """Is lhs equal to rhs? """
        return -epsilon <= lhs - rhs <= epsilon

    @classmethod
    def greaterThanOrEqualTo(cls, lhs: float|int, rhs: float|int, *, epsilon: float = 1e-3) -> bool:
        """Is lhs greater than or equal to rhs? """
        return lhs >= rhs - epsilon

    @classmethod
    def lessThanOrEqualTo(cls, lhs: float|int, rhs: float|int, *, epsilon: float = 1e-3) -> bool:
        """Is lhs less than or equal to rhs? """
        return lhs <= rhs + epsilon
