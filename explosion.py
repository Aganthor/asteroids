"""
[summary]
Simple module to declare our animation class for an explosion.
https://gamedev.stackexchange.com/questions/44118/how-to-slow-down-a-sprite-that-updates-every-frame
Used this site to implement a slower animation.
"""
import arcade


class ExplosionAnimation(arcade.Sprite):
    EXPLOSION_SCALE = 0.45
    ANIMATION_SPEED = 10.0
    MAX_CYCLE_TIME = 2

    def __init__(self):
        super().__init__()

        self.textures = [
            arcade.load_texture("assets/Explosion/explosion00.png"),
            arcade.load_texture("assets/Explosion/explosion01.png"),
            arcade.load_texture("assets/Explosion/explosion02.png"),
            arcade.load_texture("assets/Explosion/explosion03.png"),
            arcade.load_texture("assets/Explosion/explosion04.png"),
            arcade.load_texture("assets/Explosion/explosion05.png"),
            arcade.load_texture("assets/Explosion/explosion06.png"),
            arcade.load_texture("assets/Explosion/explosion07.png"),
            arcade.load_texture("assets/Explosion/explosion08.png")
        ]

        self.scale = self.EXPLOSION_SCALE
        self.current_texture = 0
        self.set_texture(self.current_texture)

        # Animation speed related
        self.animation_update_time = 1.0 / ExplosionAnimation.ANIMATION_SPEED
        self.time_since_last_swap = 0.0
        self.number_of_cycle = 0

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
                self.number_of_cycle += 1
            self.time_since_last_swap = 0.0

    def is_animation_over(self):
        return self.number_of_cycle == ExplosionAnimation.MAX_CYCLE_TIME

    def reset(self):
        self.number_of_cycle = 0
