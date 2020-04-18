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
my_font = pygame.font.SysFont("Arial", 50)
text_font = pygame.font.SysFont("Arial", 30)

background_image = pygame.image.load('GameField.jpg')
gamefield = GameField.GameField(background_image, text_font)

engine = Engine.Engine(player_list, gamefield)

current_payer = 0
run = True

while run:
    engine.player_turn(current_payer)
    current_payer += 1
    if current_payer >= 4:
        current_payer = 0
'''
while run:
    #engine.draw_pawns()
    # keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                number = engine.roll_dice()
                if number == 6:
                    engine.move_pawn_out_of_house(current_payer)
                else:
                    engine.move_pawn(current_payer, number)
                current_payer += 1
                if current_payer >= 4:
                    current_payer = 0

                print(number)
'''