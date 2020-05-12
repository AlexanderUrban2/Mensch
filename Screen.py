import ctypes
import pygame
import json


class Screen:
    screen_width: float
    screen_height: float
    background_image: pygame.image

    screen: pygame.display

    def __init__(self):

        self.init_images()

        self.init_screen()
        self.create_screen()

    def init_images(self):
        with open('image_pack.txt') as json_file:
            data = json.load(json_file)
        self.background_image = pygame.image.load(data["background_image_start_screen"])

    def init_screen(self):
        user32 = ctypes.windll.user32

        self.screen_width = int(user32.GetSystemMetrics(1) * 0.9)
        self.screen_height = int(user32.GetSystemMetrics(1) * 0.9)

    def create_screen(self):
        self.background_image = pygame.transform.smoothscale(self.background_image, (self.screen_width, self.screen_height))
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Mensch Ärgere dich nicht")
