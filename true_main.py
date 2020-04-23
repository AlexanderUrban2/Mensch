import Player
import GameField
import pygame
import Dice
import time
import Engine
import StartScreen
import Rules


pygame.init()
pygame.font.init()


def create_players():
    player_list = [Player.Player(i + 1, True) for i in range(4)]
    return player_list


player_list = create_players()
my_font = pygame.font.SysFont("Arial", 50)
text_font = pygame.font.SysFont("Arial", 30)
start_screen_font = pygame.font.Font("Iveseenthatfacebefore.ttf",30)

background_image_gamefield = pygame.image.load('GameField.jpg')
background_image_start_screen = pygame.image.load('StartScreen.jpg')
back_arrow_image = pygame.image.load('BackArrow.png')
gamefield = GameField.GameField(background_image_gamefield, text_font)

rule = Rules.Rules(background_image_start_screen, back_arrow_image, start_screen_font, "Rule.txt")
start_screen = StartScreen.StartScreen(background_image_start_screen, start_screen_font, rule)
#rule_screen mitgeben

start_screen.start_game()

engine = Engine.Engine(player_list, gamefield)
#rule_screen mitgeben

current_payer = 0
run = True


while run:
    
    engine.player_turn(current_payer)
    current_payer += 1
    if current_payer >= 4:
        current_payer = 0

