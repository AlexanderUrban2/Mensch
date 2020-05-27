import Pawn
import colors
import pygame


class Player:
    player_number: int
    pawn_list = list

    def __init__(self, player_number: int):
        self.player_number = player_number

        self.pawn_list = [Pawn.Pawn(i + 1, self.player_number) for i in range(4)]

    def has_won(self) -> bool:
        for pawn in self.pawn_list:
            if not pawn.is_in_finishing_squares():
                return False
        return True

    """
    test:
        tmp = 0
        for pawn in self.player_list[0].pawn_list:
                if tmp == 0:
                    pawn.current_position = 110
                    tmp = 11
                else:
                    pawn.current_position = tmp
                    tmp += 1
        #set 1 pawn in starting yard and 3 on gamefield

        result = self.player_list[0].has_pawn_in_yard()
        Assert.isTrue(result)

        # player has pawn in yard --> test fails if method returns false
    """
    def has_pawn_in_yard(self) -> bool:
        for pawn in self.pawn_list:
            if pawn.is_in_players_yard():
                return True
        return False

    def has_pawn_on_game_field(self) -> bool:
        for pawn in self.pawn_list:
            if not pawn.is_in_players_yard():
                return True
        return False

    def get_pawns_in_finishing_squares(self) -> [Pawn.Pawn]:
        pawns = []
        for pawn in self.pawn_list:
            if pawn.is_in_finishing_squares():
                pawns.append(pawn)
        return pawns

    def get_pawn_number_on_start_field(self) -> int:
        for pawn in self.pawn_list:
            if pawn.current_position == (pawn.player_number - 1) * 10:
                return pawn.pawn_number
        return 0
