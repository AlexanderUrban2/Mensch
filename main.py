import Player
import GameField
import pygame
import Engine
import StartScreen
import Rules
import Help
import Screen
import ImagePack
import AI
import Victory


pygame.init()
pygame.font.init()


def create_players(player_count: int, ai_turn_time_delay: int, ai_difficulty: int):
    player_list = [Player.Player(i + 1) for i in range(player_count)]
    ai_list = [AI.AI(i + 1, ai_turn_time_delay, ai_difficulty) for i in range(player_count, 4)]
    for ai in ai_list:
        player_list.append(ai)
    #ai = AI.AI(4, 1, 1)
    #player_list.append(ai)
    return player_list


my_font = pygame.font.SysFont("Arial", 50)
text_font = pygame.font.SysFont("Arial", 30)
start_screen_font = pygame.font.Font("Iveseenthatfacebefore.ttf", 30)

image_pack = ImagePack.ImagePack()

gamefield = GameField.GameField(text_font)

screen = Screen.Screen()



rules = Rules.Rules(screen, start_screen_font, "Rule.txt")
help = Help.Help(screen, start_screen_font, "Help.txt")
start_screen = StartScreen.StartScreen(screen, rules, start_screen_font)

player_count = start_screen.start_game()

ai_turn_time_delay = 1  # in seconds
ai_difficulty = 1
player_list = create_players(player_count, ai_turn_time_delay, ai_difficulty)

engine = Engine.Engine(player_list, gamefield, rules, help)

victory = Victory.Victory(screen, engine, start_screen_font)



current_player = 0
run = True


while run:
    
    run = engine.player_turn(current_player)
    current_player += 1
    if current_player >= 4:
        current_player = 0

if current_player == 0:
    current_player = 3
else:
    current_player -= 1

victory.victory(current_player)

print("finish")
#Bugs:
# Man muss erst einen Pawn auswählen obwohl man gar keinen moven kann
# erst checken ob iwas geht und dann ggf nächster spieler
# code ist leicht unübersichtlich