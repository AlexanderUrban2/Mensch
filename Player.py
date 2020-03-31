import Pawn
import colors


class Player:
    player_number: int
    user_controlled: bool
    pawn_list = list
    color: (int, int, int)

    def __init__(self, player_number: int, user_controlled: bool):
        self.player_number = player_number
        self.user_controlled = user_controlled

        self.color = colors.colors[player_number]

        self.pawn_list = [Pawn.Pawn(i + 1, self.player_number, self.color) for i in range(4)]
