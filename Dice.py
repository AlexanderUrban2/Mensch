import pygame
import GameField


class Dice:
    image_list: list
    gamefield: GameField.GameField

    def __init__(self, gamefield: GameField.GameField):
        self.gamefield = gamefield
        self.init_dice()

    def init_dice(self):
        for i in range(0, 6):
            self.image_list.append(pygame.image.load('Dice' + str(i + 1) + '.png'))
            self.image_list[i] = pygame.transform.smoothscale(self.image_list[i], (screen_width // 11, screen_height // 11))