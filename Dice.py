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
        self.init_dice()
        self.surface_dice = pygame.Surface((self.gamefield.screen_size_multiplier, self.gamefield.screen_size_multiplier))

    def init_dice(self):
        for i in range(0, 6):
            self.image_list.append(pygame.image.load('Dice' + str(i + 1) + '.png'))
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
        self.surface_dice.fill((0, 0, 0, 0))
        self.surface_dice.blit(image, (0, 0))
