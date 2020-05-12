import pygame
import MapGamefieldToPosition
import json
# pawn_number und player_number werden benutzt um Zugehörigkeiten zu identifizieren, asuzuwählen mit welchem Pawn
# gelaufen wird und um dynamisch die Startposition zu ermitteln


class Pawn(pygame.sprite.Sprite):
    image: pygame.image
    rect: pygame.rect
    current_position: int
    pawn_number: int
    player_number: int
    color: (int, int, int)
    pawn_image: pygame.image

    def __init__(self, pawn_number: int, player_number: int, color: (int, int, int)):
        pygame.sprite.Sprite.__init__(self)
        self.pawn_number = pawn_number
        self.player_number = player_number
        self.current_position = player_number * 100 + pawn_number * 10
        self.color = color

        self.init_images()
        self.create_picture()

        self.rect = self.image.get_rect()

    def init_images(self):
        with open('image_pack.txt') as json_file:
            data = json.load(json_file)
        default_path = data["pawn_image"]
        split = default_path.split(".")
        path = split[0] + str(self.player_number) + "." + split[1]
        self.pawn_image = pygame.image.load(path)

    def create_picture(self):
        #  get the size of a field of the 11*11 matrix
        height = pygame.display.get_surface().get_size()[0] // 11
        width = pygame.display.get_surface().get_size()[1] // 11

        # make the surface transparent
        self.image = pygame.Surface([height, width], pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))

        # self.pawn_image = pygame.image.load('images/Pawn_1.png')
        radius = height // 3
        self.pawn_image = pygame.transform.smoothscale(self.pawn_image, (radius * 2, radius * 2))
        self.image.blit(self.pawn_image, (height // 2 - self.pawn_image.get_width() // 2, width // 2 - self.pawn_image.get_height() // 2))
        font = pygame.font.Font(None, radius)
        text = font.render(str(self.pawn_number), True, (0, 0, 0))
        self.image.blit(text, (height // 2 - text.get_width() // 2, width // 2 - text.get_height() // 2))

    def create_image(self):
        #  get the size of a field of the 11*11 matrix
        height = pygame.display.get_surface().get_size()[0] // 11
        width = pygame.display.get_surface().get_size()[1] // 11

        # make the surface transparent
        self.image = pygame.Surface([height, width], pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))

        # draw a circle with a number on the surface
        radius = height // 3
        pygame.draw.circle(self.image, self.color, (height // 2, width // 2), radius, radius)
        font = pygame.font.Font(None, radius)
        text = font.render(str(self.pawn_number), True, (0, 0, 0))
        self.image.blit(text, (height // 2 - text.get_width() // 2, width // 2 - text.get_height() // 2))

    def move_pawn_out_of_house(self):
        self.current_position = (self.player_number - 1) * 10

    def move_pawn_to_house(self):
        self.current_position = self.player_number * 100 + self.pawn_number * 10
        #player number +1 aber oben -1

    def is_in_finishing_squares(self):
        return self.current_position > 1000

    #selbe funktion von Engine.py ???
    def move_pawn(self, steps: int):
        for i in range(steps):
            self.current_position += 1
            if self.current_position > 39:
                self.current_position = 0

    def move_pawn_one_step(self):
        if self.can_move_into_finishing_squares():
            self.current_position = self.player_number * 1000 + 10
        elif self.is_in_finishing_squares():
            self.current_position += 10
        else:
            self.current_position += 1
            if self.current_position > 39:
                self.current_position = 0
    
    def can_move_into_finishing_squares(self) -> bool:
        if self.player_number == 1:
            field_before_finishing_squares = 39
        else:
            field_before_finishing_squares = self.player_number * 10 - 11

        if self.current_position == field_before_finishing_squares:
            return True
        return False

    def is_in_players_yard(self) -> bool:
        return 40 < self.current_position < 1000

    def update(self):
        x = MapGamefieldToPosition.get_coordinates(self.current_position)[0]
        y = MapGamefieldToPosition.get_coordinates(self.current_position)[1]
        display_size_x = pygame.display.get_surface().get_size()[0]
        display_size_y = pygame.display.get_surface().get_size()[1]
        self.rect.x = x * (display_size_x // 11) + display_size_x/216
        self.rect.y = y * (display_size_y // 11) + display_size_y/216
        return
