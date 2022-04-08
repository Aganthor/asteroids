from random import randrange
from enum import Enum

import arcade

import game_constants as gc


class AsteroidSize(Enum):
    SMALL = 0,
    MEDIUM = 1,
    BIG = 2,
    NOT_SPECIFIED = 3


class Asteroid(arcade.Sprite):
    SPEED = 3.0

    def __init__(self, player_ref, create_from_split=False, asteroid_size=AsteroidSize.NOT_SPECIFIED):
        """
        Class to represent an asteroid.
        :param player_ref: Used to prevent a spawn on the player ship.
        :param create_from_split: Are we creating specific sized asteroids?
        :param asteroid_size: if create_from_split, will be the asteroid size to create.
        """
        self.score = 0
        self.size = None

        filename = ""
        size = -1

        if create_from_split:
            if asteroid_size == AsteroidSize.SMALL:
                size = 2
            elif asteroid_size == AsteroidSize.MEDIUM:
                size = 1
            else:
                size = 0
        else:
            size = randrange(3)

        if size == 0:
            # There are 4 different types of big asteroids.
            big_one = randrange(1, 5)
            filename = f":resources:images/space_shooter/meteorGrey_big{big_one}.png"
            self.score = 500
            self.size = AsteroidSize.BIG
        elif size == 1:
            med_one = randrange(1, 3)
            filename = f":resources:images/space_shooter/meteorGrey_med{med_one}.png"
            self.score = 300
            self.size = AsteroidSize.MEDIUM
        elif size == 2:
            small_one = randrange(1, 3)
            filename = f":resources:images/space_shooter/meteorGrey_small{small_one}.png"
            self.score = 100
            self.size = AsteroidSize.SMALL

        super().__init__(filename, 0.5)

        self.center_x = randrange(0 + int(self.width), gc.SCREEN_WIDTH - int(self.width))
        self.center_y = randrange(0 + int(self.height), gc.SCREEN_HEIGHT - int(self.height))

        # Does it spawn on the player? If so, move it.
        while player_ref.collides_with_point((self.center_x, self.center_y)):
            print("Bang! Spawns on ship...")
            self.center_x = randrange(0 + int(self.width), gc.SCREEN_WIDTH - int(self.width))
            self.center_y = randrange(0 + int(self.height), gc.SCREEN_HEIGHT - int(self.height))

    def on_update(self, delta_time: float = 1 / 60):
        """
        Used to move the asteroid
        :param delta_time: elapsed time since last update.
        :return:
        """
        self.center_x += self.change_x
        self.center_y += self.change_y

        # If the asteroid goes out of bounds, warp it to the other side.
        if self.center_x + self.width > gc.SCREEN_WIDTH:
            self.center_x = 0
            #self.change_x *= -1
        if self.center_x - self.width < 0:
            self.center_x = gc.SCREEN_WIDTH
            #self.change_x *= -1

