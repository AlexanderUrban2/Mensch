import GameField
import Player
import Dice
import MapGamefieldToPosition
import pygame
import time


class Engine:
    player_list: []
    game_field: GameField
    dice: Dice

    def __init__(self, players: [Player, Player, Player, Player], gamefield: GameField):
        self.player_list = players
        self.game_field = gamefield
        self.dice = Dice.Dice(self.game_field)

        self.refresh_ui()

    def refresh_ui(self):
        self.game_field.show_screen()

        self.draw_pawns()

    def draw_pawns(self):
        for player in self.player_list:
            for pawn in player.pawn_list:
                x = MapGamefieldToPosition.get_coordinates(pawn.current_position)[0]
                y = MapGamefieldToPosition.get_coordinates(pawn.current_position)[1]
                self.game_field.show_text(pawn.image, pawn.color, x, y)

    def roll_dice(self):
        number = self.dice.roll_dice()
        self.draw_pawns()
        pygame.display.update()
        return number

    def move_pawn_out_of_house(self, current_player: int):
        for pawn in self.player_list[current_player].pawn_list:
            if pawn.current_position > 40:
                pawn.move_pawn_out_of_house()
                self.refresh_ui()
                return

    # bewegt momentan immer den ersten pawn den es findet, geht aber ziemlich einfach indem man ne pawn_number benutzt
    def move_pawn(self, current_player: int, steps: int):
        for pawn in self.player_list[current_player].pawn_list:
            if pawn.current_position < 40:
                for i in range(steps):
                    pawn.move_pawn_one_step()
                    self.refresh_ui()
                    time.sleep(0.1)
                return
