import pygame
import Screen
import json


class GameField:
    screen_width: float
    screen_height: float

    screen_size_multiplier: float

    screen_class: Screen
    screen: pygame.display
    font: pygame.font

    background_image: pygame.image
    ingame_rules_button: pygame.image
    ingame_help_button: pygame.image

    ingame_rules_button_rect: pygame.rect
    ingame_help_button_rect: pygame.rect

    def __init__(self, font: pygame.font):
        self.screen_class = Screen.Screen()

        self.init_images()

        self.font = font

        self.init_game_field_variables()

        self.build_game_screen()

    def init_images(self):
        with open('image_pack.txt') as json_file:
            data = json.load(json_file)
        self.background_image = pygame.image.load(data["background_image_game"])
        self.ingame_help_button = pygame.image.load(data["ingame_help_button"])
        self.ingame_rules_button = pygame.image.load(data["ingame_rules_button"])

    def init_game_field_variables(self):
        self.screen_width = self.screen_class.screen_width
        self.screen_height = self.screen_class.screen_height

        self.screen_size_multiplier = self.screen_height / 11

    def build_game_screen(self):
        self.background_image = pygame.transform.smoothscale(self.background_image, (self.screen_width, self.screen_height))
        self.ingame_rules_button = pygame.transform.smoothscale(self.ingame_rules_button, (int(self.screen_size_multiplier * 1.5), int(self.screen_size_multiplier)))
        self.ingame_help_button = pygame.transform.smoothscale(self.ingame_help_button, (int(self.screen_size_multiplier * 1.5), int(self.screen_size_multiplier)))

        self.ingame_rules_button_rect = self.ingame_rules_button.get_rect(topleft=(int(self.screen_size_multiplier*2.5), int(self.screen_size_multiplier*0.1)))
        self.ingame_help_button_rect = self.ingame_help_button.get_rect(topleft=(int(self.screen_size_multiplier*7), int(self.screen_size_multiplier*0.1)))

        self.screen = self.screen_class.screen

    def show_screen(self):
        self.screen.blit(self.background_image, (0, 0))
        self.screen.blit(self.ingame_rules_button, (int(self.screen_size_multiplier*2.5), int(self.screen_size_multiplier*0.1)))
        self.screen.blit(self.ingame_help_button, (int(self.screen_size_multiplier*7), int(self.screen_size_multiplier*0.1)))
        pygame.display.update()

    # Koordinaten entsprechen den Feldern einer 11*11 Matrix
    # die Funktion funktioniert auch mit einem Surface!
    def show_image(self, image: pygame.image, x_coordinate: int, y_coordinate: int):
        if x_coordinate != 0:
            x_coordinate = self.screen_size_multiplier * x_coordinate
        if y_coordinate != 0:
            y_coordinate = self.screen_size_multiplier * y_coordinate

        self.screen.blit(image, (x_coordinate, y_coordinate))

    def show_text(self, text: str, color, x_coordinate: int, y_coordinate: int):
        if x_coordinate != 0:
            x_coordinate = self.screen_size_multiplier * x_coordinate
        if y_coordinate != 0:
            y_coordinate = self.screen_size_multiplier * y_coordinate

        self.screen.blit(self.font.render(text, False, color), (x_coordinate + 20, y_coordinate))
        pygame.display.update()

    def show_text_info(self, player_number: int, text: str):

        if player_number == 0:
            self.blit_text(text, 0, 2)
        elif player_number == 1:
            self.blit_text(text, 7, 2)
        elif player_number == 2:
            self.blit_text(text, 7, 7)
        elif player_number == 3:
            self.blit_text(text, 0, 7)
        else:
            pass

    def blit_text(self, text, x_coordinate, y_coordinate, color=pygame.Color('black')):

        if x_coordinate != 0:
            x_coordinate = self.screen_size_multiplier * x_coordinate
        if y_coordinate != 0:
            y_coordinate = self.screen_size_multiplier * y_coordinate

        pos = (x_coordinate, y_coordinate)

        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
        space = self.font.size(' ')[0]  # The width of a space.
        if int(self.screen_size_multiplier * 4) < x_coordinate:
            max_width = int(self.screen_width)
        else:
            max_width = int(self.screen_size_multiplier * 4)
        for line in words:
            for word in line:
                word_surface = self.font.render(word, 0, color)
                word_width, word_height = word_surface.get_size()
                if x_coordinate + word_width >= max_width:
                    x_coordinate = pos[0]  # Reset the x.
                    y_coordinate += word_height  # Start on new row.
                self.screen.blit(word_surface, (x_coordinate, y_coordinate))
                x_coordinate += word_width + space
            x_coordinate = pos[0]  # Reset the x.
            y_coordinate += word_height  # Start on new row.
            pygame.display.update()
