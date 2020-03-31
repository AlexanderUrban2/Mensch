import ctypes
import pygame


class GameField:
    screen_width: float
    screen_height: float

    game_field_size: float

    game_field_distance_to_border: float

    screen: pygame.display

    background_image: pygame.image

    def __init__(self, background_image: pygame.image):
        self.background_image = background_image

        self.init_game_field_variables()

        self.build_game_screen()

    def init_game_field_variables(self):
        user32 = ctypes.windll.user32

        self.screen_width = int(user32.GetSystemMetrics(1) * 0.9)
        self.screen_height = int(user32.GetSystemMetrics(1) * 0.9)

        self.game_field_distance_to_border = (self.screen_width * 1.04827 - self.screen_width) / 2

        self.game_field_size = self.screen_width - 2 * self.game_field_distance_to_border

    def build_game_screen(self):
        pygame.transform.smoothscale(self.background_image, (self.screen_width, self.screen_height))
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Mensch ärgere dich nicht")

    def show_screen(self):
        run = True
        while run:
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            if keys[pygame.K_x]:
                self.screen.blit(self.background_image, (0, 0))
                pygame.display.update()
                run = False

            pygame.display.update()

