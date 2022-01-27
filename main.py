"""
Modèle de départ pour la programmation Arcade.
Il suffit de modifier les méthodes nécessaires à votre jeu.
"""
import arcade

from player import Player, Direction
import game_constants as gc


class MyGame(arcade.Window):
    """
    La classe principale de l'application

    NOTE: Vous pouvez effacer les méthodes que vous n'avez pas besoin.
    Si vous en avez besoin, remplacer le mot clé "pass" par votre propre code.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.BLACK)

        # Si vous avez des listes de sprites, il faut les créer ici et les
        # initialiser à None.
        self.player = None
        # Used to turn the ship
        self.turn_left_pressed = False
        self.turn_right_pressed = False
        # Used to accelerate or decelerate the ship
        self.decelerate_pressed = False
        self.accelerate_pressed = False

        # Little helper to prevent multiple acceleration with only one key_press.
        self.action_done = False

        self.player_list = None

    def setup(self):
        """
        Configurer les variables de votre jeu ici. Il faut appeler la méthode une nouvelle
        fois si vous recommencer une nouvelle partie.
        """
        # C'est ici que vous allez créer vos listes de sprites et vos sprites.
        # C'est aussi ici que vous charger les sons de votre jeu.
        self.player = Player()
        self.player.center_x = 400
        self.player.center_y = 400
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        # arcade.Schedule pour programmer des "events"

    def on_draw(self):
        """
        C'est la méthode que Arcade invoque à chaque "frame" pour afficher les éléments
        de votre jeu à l'écran.
        """

        # Cette commande permet d'effacer l'écran avant de dessiner. Elle va dessiner l'arrière
        # plan selon la couleur spécifié avec la méthode "set_background_color".
        arcade.start_render()

        # Invoquer la méthode "draw()" de vos sprites ici.

        self.player_list.draw()
        self.player.bullet_list.draw()

        angle_message = f"Player angle is {self.player.angle}, Player radians is {self.player.radians}"
        arcade.draw_text(angle_message, 10, 10, arcade.color.WHITE_SMOKE, 18)

    def on_update(self, delta_time):
        """
        Toute la logique pour déplacer les objets de votre jeu et de
        simuler sa logique vont ici. Normalement, c'est ici que
        vous allez invoquer la méthode "update()" sur vos listes de sprites.
        Paramètre:
            - delta_time : le nombre de milliseconde depuis le dernier update.
        """

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
        self.player.bullet_list.update()

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
        print(key)
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
