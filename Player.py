import Pawn
import colors
import pygame


class Player:
    player_number: int
    pawn_list = list
    color: (int, int, int)

    def __init__(self, player_number: int):
        self.player_number = player_number

        self.color = colors.colors[player_number]

        self.pawn_list = [Pawn.Pawn(i + 1, self.player_number, self.color) for i in range(4)]

    def has_pawn_in_house(self) -> bool:
        for pawn in self.pawn_list:
            if pawn.current_position > 40:
                return True
        return False

    def has_pawn_on_game_field(self) -> bool:
        for pawn in self.pawn_list:
            if pawn.current_position < 40 or pawn.current_position > 1000:
                return True
        return False

    def get_pawns_in_finishing_squares(self) -> list:
        pawns = []
        for pawn in self.pawn_list:
            if pawn.current_position > 1000:
                pawns.append(pawn)
        return pawns

    def get_pawn_number_on_start_field(self) -> int:
        for pawn in self.pawn_list:
            if pawn.current_position == (pawn.player_number - 1) * 10:
                return pawn.pawn_number
        return 0
