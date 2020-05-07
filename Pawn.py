import pygame
import MapGamefieldToPosition
# pawn_number und player_number werden benutzt um Zugehörigkeiten zu identifizieren, asuzuwählen mit welchem Pawn
# gelaufen wird und um dynamisch die Startposition zu ermitteln


class Pawn(pygame.sprite.Sprite):
    image: pygame.image
    rect: pygame.rect
    current_position: int
    pawn_number: int
    player_number: int
    color: (int, int, int)

    def __init__(self, pawn_number: int, player_number: int, color: (int, int, int)):
        pygame.sprite.Sprite.__init__(self)
        self.pawn_number = pawn_number
        self.player_number = player_number
        self.current_position = player_number * 100 + pawn_number * 10
        self.color = color
        self.create_image()

        self.rect = self.image.get_rect()

    def create_image(self):
        height = pygame.display.get_surface().get_size()[0] // 11
        width = pygame.display.get_surface().get_size()[0] // 11
        self.image = pygame.Surface([height, width], pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))

        radius = height // 3
        pygame.draw.circle(self.image, self.color, (height // 2, width // 2), radius, radius)
        font = pygame.font.Font(None, radius)
        text = font.render(str(self.pawn_number), True, (0, 0, 0))
        self.image.blit(text, (height //2 - text.get_width() // 2, width // 2 - text.get_height() // 2))

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

    def update(self):
        x = MapGamefieldToPosition.get_coordinates(self.current_position)[0]
        y = MapGamefieldToPosition.get_coordinates(self.current_position)[1]
        display_size_x = pygame.display.get_surface().get_size()[0]
        display_size_y = pygame.display.get_surface().get_size()[1]
        self.rect.x = x * (display_size_x // 11) + display_size_x/216
        self.rect.y = y * (display_size_y // 11) + display_size_y/216
        return
