import ctypes
import pygame
import ImagePack

class Screen:
    screen_width: float
    screen_height: float

    screen: pygame.display
    image_pack: ImagePack

    def __init__(self):
        self.image_pack = ImagePack.ImagePack()

        self.background_image = self.image_pack.background_image_start_screen

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
        
