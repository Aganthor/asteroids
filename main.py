"""
Modèle de départ pour la programmation Arcade.
Il suffit de modifier les méthodes nécessaires à votre jeu.
"""
import random
import arcade

from player import Player, Direction
import game_constants as gc
from explosion import ExplosionAnimation
from game_state import GameState
from asteroid import Asteroid, AsteroidSize


class MyGame(arcade.Window):
    """
    La classe principale de l'application

    NOTE: Vous pouvez effacer les méthodes que vous n'avez pas besoin.
    Si vous en avez besoin, remplacer le mot clé "pass" par votre propre code.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.BLACK)

        self.player = None
        # Used to turn the ship
        self.turn_left_pressed = False
        self.turn_right_pressed = False
        # Used to accelerate or decelerate the ship
        self.decelerate_pressed = False
        self.accelerate_pressed = False

        # Little helper to prevent multiple acceleration with only one key_press.
        self.action_done = False
        self.explosion_animation = None

        self.player_list = None
        self.asteroids_list = None

        self.game_state = GameState.RUNNING

        self.player_score = 0

    def setup(self):
        """
        Configurer les variables de votre jeu ici. Il faut appeler la méthode une nouvelle
        fois si vous recommencer une nouvelle partie.
        """
        # C'est ici que vous allez créer vos listes de sprites et vos sprites.
        # C'est aussi ici que vous charger les sons de votre jeu.
        self.player = Player()
        self.player.center_x = gc.SCREEN_WIDTH / 2
        self.player.center_y = gc.SCREEN_HEIGHT / 2
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        self.asteroids_list = arcade.SpriteList()
        self.explosion_animation = ExplosionAnimation()

        # arcade.Schedule pour programmer des "events"
        arcade.schedule(self.spawn_asteroids, 3)

    def spawn_asteroids(self, delta_time):
        """_summary_

        Args:
            delta_time (_type_): _description_
        """
        asteroid_size = random.randrange(3)
        asteroid = None
        if asteroid_size == 0:
            # There are 4 different types of big asteroids.
            big_one = random.randrange(1, 5)
            filename = f":resources:images/space_shooter/meteorGrey_big{big_one}.png"
            asteroid = Asteroid(filename, 0.5, AsteroidSize.LARGE)
        elif asteroid_size == 1:
            med_one = random.randrange(1, 3)
            filename = f":resources:images/space_shooter/meteorGrey_med{med_one}.png"            
            asteroid = Asteroid(filename, 0.5, AsteroidSize.MEDIUM)
        elif asteroid_size == 2:
            small_one = random.randrange(1, 3)
            filename = f":resources:images/space_shooter/meteorGrey_small{small_one}.png"            
            asteroid = Asteroid(filename, 0.5, AsteroidSize.SMALL)

        asteroid.center_x = random.randrange(0 + int(asteroid.width), gc.SCREEN_WIDTH - int(asteroid.width))
        asteroid.center_y = random.randrange(0 + int(asteroid.height), gc.SCREEN_HEIGHT - int(asteroid.height))

        while self.player.collides_with_point(((asteroid.center_x, asteroid.center_y))):
            asteroid.center_x = random.randrange(0 + int(asteroid.width), gc.SCREEN_WIDTH - int(asteroid.width))
            asteroid.center_y = random.randrange(0 + int(asteroid.height), gc.SCREEN_HEIGHT - int(asteroid.height))

        self.asteroids_list.append(asteroid)


    def on_draw(self):
        """
        C'est la méthode que Arcade invoque à chaque "frame" pour afficher les éléments
        de votre jeu à l'écran.
        """
        arcade.start_render()

        if self.game_state == GameState.PLAYER_EXPLOSION:
            self.explosion_animation.draw()
        elif self.game_state == GameState.RUNNING:
            self.player_list.draw()
            self.player.bullet_list.draw()
            self.asteroids_list.draw()
            arcade.draw_text(f"Score : {self.player_score}", 10, gc.SCREEN_HEIGHT - 15, arcade.color.AERO_BLUE)
            arcade.draw_text(f"Lives : {self.player.lives}", gc.SCREEN_WIDTH - 100, gc.SCREEN_HEIGHT - 15, arcade.color.AERO_BLUE)
        elif self.game_state == GameState.GAME_OVER:
            pass

        arcade.draw_text(f"Ship speed is {self.player.speed}", 10, 30, arcade.color.WHITE_SMOKE, 16)
        arcade.draw_text(f"Bullet qty is {len(self.player.bullet_list)}", 10, 10, arcade.color.WHITE_SMOKE, 16)
        arcade.draw_text(f"Asteroid count = {len(self.asteroids_list)}", 300, 10, arcade.color.RED, 16)

    def on_update(self, delta_time):
        """
        Toute la logique pour déplacer les objets de votre jeu et de
        simuler sa logique vont ici. Normalement, c'est ici que
        vous allez invoquer la méthode "update()" sur vos listes de sprites.
        Paramètre:
            - delta_time : le nombre de milliseconde depuis le dernier update.
        """
        if self.game_state == GameState.RUNNING:
            # Player movement
            if self.turn_left_pressed and not self.turn_right_pressed:
                self.player.rotate_ship(Direction.LEFT)
            elif self.turn_right_pressed and not self.turn_left_pressed:
                self.player.rotate_ship(Direction.RIGHT)
            elif self.accelerate_pressed and not self.decelerate_pressed:
                if not self.action_done:
                    self.player.accelerate()
                    self.action_done = True
            elif self.decelerate_pressed and not self.accelerate_pressed:
                if not self.action_done:
                    self.player.decelerate()
                    self.action_done = True

            self.player_list.update()

            # Check for collision between ship and asteroids
            player_hit = arcade.check_for_collision_with_list(self.player, self.asteroids_list)
            if len(player_hit) > 0:
                self.explosion_animation.center_x = self.player.center_x
                self.explosion_animation.center_y = self.player.center_y
                self.game_state = GameState.PLAYER_EXPLOSION
                self.player.lives -= 1
                if not self.player.is_alive():
                    self.game_state  =GameState.GAME_OVER
                return
                
            # Check to see if collision between bullets and asteroids.
            for bullet in self.player.bullet_list:
                asteroid_hit_list = arcade.check_for_collision_with_list(bullet, self.asteroids_list)
                for asteroid in asteroid_hit_list:
                    self.player_score += asteroid.get_score()
                    asteroid.kill()
                    bullet.kill()
        elif self.game_state == GameState.PLAYER_EXPLOSION:
            self.explosion_animation.on_update(delta_time)
            if self.explosion_animation.is_animation_over():
                #self.explosion_animation.kill()
                self.game_state = GameState.RUNNING

    def on_key_press(self, key, key_modifiers):
        """
        Cette méthode est invoquée à chaque fois que l'usager tape une touche
        sur le clavier.
        Paramètres:
            - key: la touche enfoncée
            - key_modifiers: est-ce que l'usager appuie sur "shift" ou "ctrl" ?

        Pour connaître la liste des touches possibles:
        http://arcade.academy/arcade.key.html
        """
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.turn_left_pressed = True
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.turn_right_pressed = True
        if key == arcade.key.UP or key == arcade.key.W:
            self.accelerate_pressed = True
        if key == arcade.key.DOWN or key == arcade.key.S:
            self.decelerate_pressed = True
        if key == arcade.key.SPACE:
            self.player.fire_bullet()

    def on_key_release(self, key, key_modifiers):
        """
        Méthode invoquée à chaque fois que l'usager enlève son doigt d'une touche.
        Paramètres:
            - key: la touche relâchée
            - key_modifiers: est-ce que l'usager appuie sur "shift" ou "ctrl" ?
        """
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.turn_left_pressed = False
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.turn_right_pressed = False
        if key == arcade.key.UP or key == arcade.key.W:
            self.accelerate_pressed = False
            self.action_done = False
        if key == arcade.key.DOWN or key == arcade.key.S:
            self.decelerate_pressed = False
            self.action_done = False

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Méthode invoquée lorsque l'usager clique un bouton de la souris.
        Paramètres:
            - x, y: coordonnées où le bouton a été cliqué
            - button: le bouton de la souris appuyé
            - key_modifiers: est-ce que l'usager appuie sur "shift" ou "ctrl" ?
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Méthode invoquée lorsque l'usager relâche le bouton cliqué de la souris.
        Paramètres:
            - x, y: coordonnées où le bouton a été relâché
            - button: le bouton de la souris relâché
            - key_modifiers: est-ce que l'usager appuie sur "shift" ou "ctrl" ?
        """
        pass


def main():
    """ Main method """
    game = MyGame(gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT, gc.SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
