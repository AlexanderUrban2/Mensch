import ctypes
import pygame

class Screen:
    screen_width: float
    screen_height: float
    screen: pygame.display

    def __init__(self, background_image: pygame.image):
        
        self.background_image = background_image

        self.init_screen()
        self.create_screen()


    def init_screen(self):
        user32 = ctypes.windll.user32

        self.screen_width = int(user32.GetSystemMetrics(1) * 0.9)
        self.screen_height = int(user32.GetSystemMetrics(1) * 0.9)


    def create_screen(self):
        self.background_image = pygame.transform.smoothscale(self.background_image, (self.screen_width, self.screen_height))
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Mensch Ärgere dich nicht")
        self.screen.blit(self.background_image, (0, 0))
        pygame.display.update()

    