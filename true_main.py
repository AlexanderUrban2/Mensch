import Player
import GameField
import pygame
import time


player = Player.Player(1, True)
background_image = pygame.image.load('GameField.jpg')
gamefield = GameField.GameField(background_image)
gamefield.build_game_screen()
