import Player
import GameField
import pygame
import Dice
import time
import Engine


pygame.init()
pygame.font.init()


def create_players():
    player_list = [Player.Player(i + 1, True) for i in range(4)]
    return player_list


player_list = create_players()
my_font = pygame.font.SysFont("Comic Sans MS", 30)

background_image = pygame.image.load('GameField.jpg')
gamefield = GameField.GameField(background_image, my_font)

engine = Engine.Engine(player_list, gamefield)

turn = 0
run = True

while run:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                for i in range(10):
                    number = engine.dice.roll_dice()
                    time.sleep(0.005)

                turn += 1
                if turn >= 4:
                    turn = 0

                print(number)
