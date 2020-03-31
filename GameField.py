import ctypes
import pygame


class GameField:
    screen_width: float
    screen_height: float

    screen_size_multiplier: float

    game_field_size: float

    game_field_distance_to_border: float

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

        self.game_field_distance_to_border = (self.screen_width * 1.04827 - self.screen_width) / 2

        self.game_field_size = self.screen_width - 2 * self.game_field_distance_to_border

        self.screen_size_multiplier = self.screen_height / 11

    def build_game_screen(self):
        self.background_image = pygame.transform.smoothscale(self.background_image, (self.screen_width, self.screen_height))
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Mensch ärgere dich nicht")

    def show_screen(self):
        self.screen.blit(self.background_image, (0, 0))
        pygame.display.update()

    # Koordinaten entsprechen den Feldern einer 11*11 Matrix
    def show_image(self, image: pygame.image, x_coordinate: int, y_coordinate: int):
        if x_coordinate != 0:
            x_coordinate = self.screen_size_multiplier * x_coordinate
        if y_coordinate != 0:
            y_coordinate = self.screen_size_multiplier * y_coordinate

        self.screen.blit(self.background_image, (0, 0))
        self.screen.blit(image, (x_coordinate, y_coordinate))
        pygame.display.update()

    def show_text(self, text: str, color, x_coordinate: int, y_coordinate: int):
        if x_coordinate != 0:
            x_coordinate = self.screen_size_multiplier * x_coordinate
        if y_coordinate != 0:
            y_coordinate = self.screen_size_multiplier * y_coordinate

        self.font.render(text, False, color, (x_coordinate, y_coordinate))
        pygame.display.update()
