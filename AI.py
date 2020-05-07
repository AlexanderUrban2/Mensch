import Player


# can later be checked with: issubclass(AI, Player.Player)
class AI (Player.Player):
    turn_time_delay: float
    difficulty: int

    def __init__(self, player_number: int, turn_time_delay: int, difficulty: int):
        super().__init__(player_number)
        self.turn_time_delay = turn_time_delay
        self.difficulty = difficulty
