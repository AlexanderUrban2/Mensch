import GameField
import Player
import Dice
import MapGamefieldToPosition
import pygame


class Engine:
    player_list: []
    game_field: GameField
    dice: Dice

    def __init__(self, players: [Player, Player, Player, Player], gamefield: GameField):
        self.player_list = players
        self.game_field = gamefield
        self.dice = Dice.Dice(self.game_field)

        self.init_ui()

    def init_ui(self):
        self.game_field.show_screen()

        self.draw_pawns()

    def draw_pawns(self):
        for player in self.player_list:
            for pawn in player.pawn_list:
                x = MapGamefieldToPosition.get_coordinates(pawn.current_position)[0]
                y = MapGamefieldToPosition.get_coordinates(pawn.current_position)[1]
                print(x, y)
                self.game_field.show_text(pawn.image, pawn.color, x, y)
