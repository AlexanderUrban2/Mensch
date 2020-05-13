import json
import pygame
import GameField
import random


class Dice:
    image_list: []
    gamefield: GameField
    image: pygame.image
    coordinates = (5, 5)
    surface_dice: pygame.Surface

    def __init__(self, gamefield: GameField):
        self.gamefield = gamefield
        self.image_list = []
        self.init_images()
        self.surface_dice = pygame.Surface((self.gamefield.screen_size_multiplier, self.gamefield.screen_size_multiplier),
                                           pygame.SRCALPHA)

    def init_images(self):
        with open('image_pack.txt') as json_file:
            data = json.load(json_file)
        for i in range(0, 6):
            self.image_list.append(pygame.image.load(data["dice_image_" + str(i + 1)]))
            self.image_list[i] = pygame.transform.smoothscale(self.image_list[i], (self.gamefield.screen_width // 11, self.gamefield.screen_height // 11))

    def roll_dice(self) -> int:
        number = random.randint(1, 6)
        self.update_dice_image(self.image_list[number - 1])
        self.draw_dice_on_game_field()
        return number

    def draw_dice_on_game_field(self):
        self.gamefield.show_image(self.surface_dice, 5, 5)
        pygame.display.update()

    def update_dice_image(self, image):
        background_middle = pygame.display.get_surface().get_size()[0] // 11 * 5
        self.surface_dice.blit(self.gamefield.background_image, (-background_middle, -background_middle))
        self.draw_dice_on_game_field()
        self.surface_dice.blit(image, (0, 0))
