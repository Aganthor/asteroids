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
    BULLET_SPEED = 1.0

    def __init__(self):
        super().__init__(":resources:images/space_shooter/playerShip1_green.png", Player.PLAYER_SCALE)

        self.lives = Player.MAX_LIVES
        self.speed = 0.0

        self.bullet_list = arcade.SpriteList()

    def fire_bullet(self):
        bullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png", 0.5)
        bullet.center_x = self.center_x #+ self.width / 1.5
        bullet.center_y = self.center_y #+ self.height / 1.5

        """
        bullet_sprite.change_y = \
            math.cos(math.radians(player_sprite.angle)) * bullet_speed
        bullet_sprite.change_x = \
            -math.sin(math.radians(player_sprite.angle)) \
            * bullet_speed        
        """
        #bullet.radians = math.radians(self.angle)
        bullet.change_x = -math.sin(math.radians(self.angle)) * Player.BULLET_SPEED
        bullet.change_y = math.cos(math.radians(self.angle)) * Player.BULLET_SPEED

        self.bullet_list.append(bullet)

    def rotate_ship(self, direction):
        if direction == Direction.LEFT:
            self.turn_left(1.5)
            # if self.angle > 360:
            #     self.angle = 0
        if direction == Direction.RIGHT:
            self.turn_right(1.5)
            # self.angle = abs(self.angle)
            # if self.angle > 360:
            #     self.angle = 0

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

        self.strafe(self.speed)

        if self.center_y + self.height / 1.5 > gc.SCREEN_HEIGHT:
            # Si change_x est négatif, je tourne vers la gauche en montant
            # Si change_x est positif, je tourne vers la droite en montant
            self.center_y = 0 + self.height
        if self.center_y < self.height / 2:
            self.center_y = gc.SCREEN_HEIGHT - self.height
        if self.center_x < self.width / 2:
            self.change_x *= -1
        if self.center_x + self.width / 1.5 > gc.SCREEN_WIDTH:
            self.change_x *= -1

        for bullet in self.bullet_list:
            bullet.update()





