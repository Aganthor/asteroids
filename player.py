from enum import Enum
import arcade

import game_constants as gc


class Direction(Enum):
    LEFT = 1
    RIGHT = 2


class Player(arcade.Sprite):
    MAX_LIVES = 3
    PLAYER_SCALE = 0.5
    MAX_SPEED = 1.5

    def __init__(self):
        super().__init__(":resources:images/space_shooter/playerShip1_green.png", Player.PLAYER_SCALE)

        self.lives = Player.MAX_LIVES
        self.speed = 0.0

    def rotate_ship(self, direction):
        if direction == Direction.LEFT:
            self.turn_left(1.5)
        if direction == Direction.RIGHT:
            self.turn_right(1.5)

    def accelerate(self):
        self.speed = min(self.speed + 0.005, Player.MAX_SPEED)
        print(f"Accelerate speed -> {self.speed}")

    def decelerate(self):
        self.speed = max(self.speed - 0.0005, 0.0)
        print(f"Decelerate speed -> {self.speed}")
        if self.speed == 0.0:
            self.stop()

    def update(self):
        super().update()
        #print(f"Player coord {self.center_x}, {self.center_y}")

        print(f"Player angle = {self.angle}")
        self.strafe(self.speed)

        if self.center_y + self.height > gc.SCREEN_HEIGHT:
            pass



