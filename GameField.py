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
    ingame_sound_on_button: pygame.image
    ingame_sound_off_button: pygame.image

    ingame_rules_button_rect: pygame.rect
    ingame_help_button_rect: pygame.rect
    ingame_sound_button_rect: pygame.rect

    """
                desc: 
                    - init
                param:
                    - font: pygame.font -> font to be used when drawing text on the screen
                return:
                    - none
    """
    def __init__(self, font: pygame.font):
        self.screen_class = Screen.Screen()

        self.init_images()

        self.font = font

        self.init_game_field_variables()

        self.build_game_screen()

    """
                desc: 
                    - initialize the images with the file paths stored in 'image_pack.txt'
                param:
                    - none
                return:
                    - none
    """
    def init_images(self):
        with open('image_pack.txt') as json_file:
            data = json.load(json_file)
        self.background_image = pygame.image.load(data["background_image_game"])
        self.ingame_help_button = pygame.image.load(data["ingame_help_button"])
        self.ingame_rules_button = pygame.image.load(data["ingame_rules_button"])
        self.ingame_sound_on_button = pygame.image.load(data["sound_on_button"])
        self.ingame_sound_off_button = pygame.image.load(data["sound_off_button"])

    def init_game_field_variables(self):
        self.screen_width = self.screen_class.screen_width
        self.screen_height = self.screen_class.screen_height

        self.screen_size_multiplier = self.screen_height / 11

    """
                desc: 
                    - scale the images and get rectangles of specific ones
                param:
                    - none
                return:
                    - none
    """
    def build_game_screen(self):
        self.background_image = pygame.transform.smoothscale(self.background_image, (self.screen_width, self.screen_height))
        self.ingame_rules_button = pygame.transform.smoothscale(self.ingame_rules_button, (int(self.screen_size_multiplier * 1.5), int(self.screen_size_multiplier)))
        self.ingame_help_button = pygame.transform.smoothscale(self.ingame_help_button, (int(self.screen_size_multiplier * 1.5), int(self.screen_size_multiplier)))
        self.ingame_sound_on_button = pygame.transform.smoothscale(self.ingame_sound_on_button, (int(self.screen_size_multiplier * 1), int(self.screen_size_multiplier * 1)))
        self.ingame_sound_off_button = pygame.transform.smoothscale(self.ingame_sound_off_button, (int(self.screen_size_multiplier * 1), int(self.screen_size_multiplier * 1)))

        self.ingame_rules_button_rect = self.ingame_rules_button.get_rect(topleft=(int(self.screen_size_multiplier*2.5), int(self.screen_size_multiplier*0.1)))
        self.ingame_help_button_rect = self.ingame_help_button.get_rect(topleft=(int(self.screen_size_multiplier*7), int(self.screen_size_multiplier*0.1)))
        self.ingame_sound_button_rect = self.ingame_sound_on_button.get_rect(topleft=(int(self.screen_size_multiplier * 2.5), int(self.screen_size_multiplier * 9.75)))

        self.screen = self.screen_class.screen

    """
                desc: 
                    - draw the images on the screen
                param:
                    - none
                return:
                    - none
    """
    def show_screen(self):
        self.screen.blit(self.background_image, (0, 0))
        self.show_image(self.ingame_rules_button, 2.5, 0.1)
        self.show_image(self.ingame_help_button, 7, 0.1)
        # blit the button accordingly if music is (not) playing
        if pygame.mixer.music.get_busy():
            self.show_image(self.ingame_sound_on_button, 2.5, 9.75)
        else:
            self.show_image(self.ingame_sound_off_button, 2.5, 9.75)

        pygame.display.update()

    """
                desc: 
                    - draw image at a specific location; coordinates represent the fields of a 11*11 matrix
                param:
                    - image: pygame.image -> image to be drawn
                    - x_coordinate: int -> x-coordinate for the position
                    - y_coordinate: int -> y-coordinate for the position 
                return:
                    - none
    """
    # Coordinates are equivalent to the fields of a 11*11 matrix
    def show_image(self, image: pygame.image, x_coordinate: float, y_coordinate: float):
        if x_coordinate != 0:
            x_coordinate = int(self.screen_size_multiplier * x_coordinate)
        if y_coordinate != 0:
            y_coordinate = int(self.screen_size_multiplier * y_coordinate)

        self.screen.blit(image, (x_coordinate, y_coordinate))

    """
                desc: 
                    - show text info under/above the current player's yard 
                param:
                    - player_number: int -> position of the current player in the engines player_list[]
                    - text: str -> text to be drawn
                return:
                    - none
    """
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

    """
                desc: 
                    - draw text, the text gets split into multiple parts in order to prevent it from being drawn over 
                      the playing area
                param:
                    - text - str
                    - x_coordinate - int
                    - y_coordinate - int
                return:
                    - none
    """
    def blit_text(self, text, x_coordinate, y_coordinate):
        with open('text_color_pack.txt') as json_file:
            data = json.load(json_file)
        color = data["text_info_color"]
        # define color

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
