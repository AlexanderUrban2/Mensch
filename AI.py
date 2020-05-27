import Player


# basically the same as a player, but could have different difficulties and make low or fast turns
class AI (Player.Player):
    turn_time_delay: float
    difficulty: int

    """
                desc: 
                    - init
                param:
                    - player_number: int -> well, the player number, used to differentiate between players
                    - turn_time_delay: int -> time before the AI starts to make a turn
                    - difficulty: int -> the difficulty of the AI (random pawn selection, check if it can hit another pawn...)
                                        currently not used (only one difficulty exists)
                return:
                    - none
    """
    def __init__(self, player_number: int, turn_time_delay: int, difficulty: int):
        super().__init__(player_number)
        self.turn_time_delay = turn_time_delay
        self.difficulty = difficulty
