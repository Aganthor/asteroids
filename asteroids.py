from random import randrange

import arcade

import game_constants as gc


class Asteroid(arcade.Sprite):
    def __init__(self, player_ref):
        """
        Class to represent an asteroid in the game.
        """
        self.score = 0

        asteroid_size = randrange(3)
        filename = ""
        if asteroid_size == 0:
            # There are 4 different types of big asteroids.
            big_one = randrange(1, 5)
            filename = f":resources:images/space_shooter/meteorGrey_big{big_one}.png"
            self.score = 500
        elif asteroid_size == 1:
            med_one = randrange(1, 3)
            filename = f":resources:images/space_shooter/meteorGrey_med{med_one}.png"
            self.score = 300
        elif asteroid_size == 2:
            small_one = randrange(1, 3)
            filename = f":resources:images/space_shooter/meteorGrey_small{small_one}.png"
            self.score = 100

        super().__init__(filename, 0.5)

        self.center_x = randrange(0 + int(self.width), gc.SCREEN_WIDTH - int(self.width))
        self.center_y = randrange(0 + int(self.height), gc.SCREEN_HEIGHT - int(self.height))

        # Does it spawn on the player? If so, move it.
        while player_ref.collides_with_point((self.center_x, self.center_y)):
            print("Bang! Spawns on ship...")
            self.center_x = randrange(0 + int(self.width), gc.SCREEN_WIDTH - int(self.width))
            self.center_y = randrange(0 + int(self.height), gc.SCREEN_HEIGHT - int(self.height))

