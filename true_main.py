import Player
import GameField
import pygame
import Dice
import time
import Engine
import StartScreen
import Rules
import Help
import Screen
import ImagePack


pygame.init()
pygame.font.init()


def create_players():
    player_list = [Player.Player(i + 1, True) for i in range(4)]
    return player_list


player_list = create_players()
my_font = pygame.font.SysFont("Arial", 50)
text_font = pygame.font.SysFont("Arial", 30)
start_screen_font = pygame.font.Font("Iveseenthatfacebefore.ttf",30)

image_pack = ImagePack.ImagePack()

gamefield = GameField.GameField(text_font)

screen = Screen.Screen()

rules = Rules.Rules(screen,start_screen_font, "Rule.txt")
help = Help.Help(screen,start_screen_font, "Help.txt")
start_screen = StartScreen.StartScreen(screen, rules, start_screen_font)

start_screen.start_game()

engine = Engine.Engine(player_list, gamefield, rules, help)

current_payer = 0
run = True


while run:
    
    engine.player_turn(current_payer)
    current_payer += 1
    if current_payer >= 4:
        current_payer = 0

