# pawn_number und player_number werden benutzt um Zugehörigkeiten zu identifizieren, asuzuwählen mit welchem Pawn
# gelaufen wird und um dynamisch die Startposition zu ermitteln


class Pawn:

    image = "x"
    current_position: int
    pawn_number: int
    player_number: int
    color: (int, int, int)

    def __init__(self, pawn_number: int, player_number: int, color: (int, int, int)):
        self.pawn_number = pawn_number
        self.current_position = player_number * 100 + pawn_number * 10
        self.color = color

    def move_pawn_out_of_house(self):
        self.current_position = (self.player_number - 1) * 10

    def move_pawn(self, steps: int):
        for i in range(steps):
            self.current_position += 1
            if self.current_position > 39:
                self.current_position = 0
