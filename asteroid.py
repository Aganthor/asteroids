from enum import Enum
import arcade


class AsteroidSize(Enum):
    SMALL = 0
    MEDIUM = 1
    LARGE = 2


class Asteroid(arcade.Sprite):
    def __init__(self, filename, scale, size):
        super().__init__(filename, scale)

        self.size = size

    def get_score(self):
        if self.size == AsteroidSize.SMALL:
            return 500
        elif self.size == AsteroidSize.MEDIUM:
            return 1000
        else:
            return 1500
