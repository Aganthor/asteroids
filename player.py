from enum import Enum
import math

import arcade

import game_constants as gc


class Direction(Enum):
    LEFT = 1
    RIGHT = 2


class Player(arcade.Sprite):
    MAX_LIVES = 3
    PLAYER_SCALE = 0.5
    MAX_SPEED = 1.5
    BULLET_SPEED = 5.0

    def __init__(self):
        super().__init__(":resources:images/space_shooter/playerShip1_green.png", Player.PLAYER_SCALE)

        self.lives = Player.MAX_LIVES
        self.speed = 0.0

        self.bullet_list = arcade.SpriteList()

    def fire_bullet(self):
        bullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png", 0.5)
        bullet.center_x = self.center_x  # + self.width / 1.5
        bullet.center_y = self.center_y  # + self.height / 1.5

        bullet.angle = self.angle
        bullet.turn_left()

        bullet.change_x = -math.sin(math.radians(self.angle)) * Player.BULLET_SPEED
        bullet.change_y = math.cos(math.radians(self.angle)) * Player.BULLET_SPEED

        self.bullet_list.append(bullet)

    def rotate_ship(self, direction):
        if direction == Direction.LEFT:
            self.turn_left(1.5)
        if direction == Direction.RIGHT:
            self.turn_right(1.5)

    def accelerate(self):
        self.speed = min(self.speed + 0.005, Player.MAX_SPEED)

    def decelerate(self):
        self.speed = max(self.speed - 0.005, -Player.MAX_SPEED)

    def update(self):
        super().update()

        self.strafe(self.speed)

        # Clamp the speed to MAX_SPEED
        if abs(self.change_x) > Player.MAX_SPEED:
            self.change_x = -Player.MAX_SPEED if self.change_x < 0.0 else Player.MAX_SPEED
        if abs(self.change_y) > Player.MAX_SPEED:
            self.change_y = -Player.MAX_SPEED if self.change_y < 0.0 else Player.MAX_SPEED

        # Are we out of bounds? If so, move to other side of screen.
        if self.center_y + self.height / 1.5 > gc.SCREEN_HEIGHT:
            self.center_y = 0 + self.height
        if self.center_y < self.height / 2:
            self.center_y = gc.SCREEN_HEIGHT - self.height
        if self.center_x < 0:
            self.center_x = gc.SCREEN_WIDTH - self.width
        if self.center_x + self.width / 1.5 > gc.SCREEN_WIDTH:
            self.center_x = 0 + self.width

        # Check to see if bullets go out of bounds.
        for bullet in self.bullet_list:
            bullet.update()
            if bullet.center_x > gc.SCREEN_WIDTH or bullet.center_x < 0:
                bullet.remove_from_sprite_lists()
            if bullet.center_y > gc.SCREEN_HEIGHT or bullet.center_y < 0:
                bullet.remove_from_sprite_lists()