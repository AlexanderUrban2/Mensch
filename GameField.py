import ctypes
import pygame
import StartScreen


class GameField:
    screen_width: float
    screen_height: float

    screen_size_multiplier: float

    screen: pygame.display
    font: pygame.font

    background_image: pygame.image

    def __init__(self, background_image: pygame.image, font: pygame.font):
        self.background_image = background_image
        self.font = font

        self.init_game_field_variables()

        self.build_game_screen()

    def init_game_field_variables(self):
        user32 = ctypes.windll.user32

        self.screen_width = int(user32.GetSystemMetrics(1) * 0.9)
        self.screen_height = int(user32.GetSystemMetrics(1) * 0.9)

        self.screen_size_multiplier = self.screen_height / 11

    def build_game_screen(self):
        self.background_image = pygame.transform.smoothscale(self.background_image, (self.screen_width, self.screen_height))
        #ich weiß absolut nicht warum das Funktioniert.... Ziel ist den screen hier dem screen von startgame gelichzusetzen
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

    def show_screen(self):
        self.screen.blit(self.background_image, (0, 0))
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

        if(player_number == 0):
            self.blit_text(text, 0, 2)
        elif(player_number == 1):
            self.blit_text(text, 7, 2)
        elif(player_number == 2):
            self.blit_text(text, 7, 7)
        elif(player_number == 3):
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
        if(int(self.screen_size_multiplier * 4) < x_coordinate):
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

