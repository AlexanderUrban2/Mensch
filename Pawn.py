# pawn_number und player_number werden benutzt um Zugehörigkeiten zu identifizieren, asuzuwählen mit welchem Pawn
# gelaufen wird und um dynamisch die Startposition zu ermitteln


class Pawn:
    image: str
    current_position: int
    pawn_number: int
    player_number: int
    color: (int, int, int)

    def __init__(self, pawn_number: int, player_number: int, color: (int, int, int)):
        self.pawn_number = pawn_number
        self.player_number = player_number
        self.current_position = player_number * 100 + pawn_number * 10
        self.color = color
        self.image = str(self.pawn_number)

    def move_pawn_out_of_house(self):
        self.current_position = (self.player_number - 1) * 10

    def move_pawn_to_house(self, player_number: int, pawn_number: int):
        self.current_position = (player_number + 1) * 100 + pawn_number * 10  
        #player number +1 aber oben -1


    #selbe funktion von Engine.py ???
    def move_pawn(self, steps: int):
        for i in range(steps):
            self.current_position += 1
            if self.current_position > 39:
                self.current_position = 0

    def move_pawn_one_step(self):
        self.current_position += 1
        if self.current_position > 39:
            self.current_position = 0
