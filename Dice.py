import pygame
import GameField
import random


class Dice:
    image_list: []
    gamefield: GameField
    image: pygame.image
    coordinates = (5, 5)

    def __init__(self, gamefield: GameField):
        self.gamefield = gamefield
        self.image_list = []
        self.init_dice()

    def init_dice(self):
        for i in range(0, 6):
            self.image_list.append(pygame.image.load('Dice' + str(i + 1) + '.png'))
            self.image_list[i] = pygame.transform.smoothscale(self.image_list[i], (self.gamefield.screen_width // 11, self.gamefield.screen_height // 11))

    def roll_dice(self) -> int:
        number = random.randint(1, 6)
        self.gamefield.show_image(self.image_list[number - 1], self.coordinates[0], self.coordinates[1], "dice")
        return number
