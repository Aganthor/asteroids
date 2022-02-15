import arcade

class Explosion(arcade.Sprite):
    pass

"""
[summary]
Simple module to declare our animation class for the different attack type.
https://gamedev.stackexchange.com/questions/44118/how-to-slow-down-a-sprite-that-updates-every-frame
Used this site to implement a slower animation.
"""
import arcade


class AttackAnimation(arcade.Sprite):
    EXPLOSION_SCALE = 0.50
    ANIMATION_SPEED = 5.0

    def __init__(self):
        super().__init__()

        self.textures = [
            arcade.load_texture("assets/scissors.png"),
            arcade.load_texture("assets/scissors-close.png"),
        ]

        self.scale = self.EXPLOSION_SCALE
        self.current_texture = 0
        self.set_texture(self.current_texture)

        # Animation speed related
        self.animation_update_time = 1.0 / AttackAnimation.ANIMATION_SPEED
        self.time_since_last_swap = 0.0

    def on_update(self, delta_time: float = 1 / 60):
        # Update the animation.
        self.time_since_last_swap += delta_time
        if self.time_since_last_swap > self.animation_update_time:
            self.current_texture += 1
            if self.current_texture < len(self.textures):
                self.set_texture(self.current_texture)
            else:
                self.current_texture = 0
                self.set_texture(self.current_texture)
            self.time_since_last_swap = 0.0
