import Player
import GameField
import pygame
import Engine
import StartScreen
import Rules
import Help
import Screen
import AI
import Victory

pygame.init()
pygame.font.init()
pygame.mixer.init()


def create_players(player_count: int, ai_turn_time_delay: int, ai_difficulty: int):
    player_list = [Player.Player(i + 1) for i in range(player_count)]
    ai_list = [AI.AI(i + 1, ai_turn_time_delay, ai_difficulty) for i in range(player_count, 4)]
    for ai in ai_list:
        player_list.append(ai)
    return player_list


theme_list = ("default", "dark", "meme")

my_font = pygame.font.SysFont("Arial", 50)
text_font = pygame.font.SysFont("Arial", 30)
start_screen_font = pygame.font.Font("Iveseenthatfacebefore.ttf", 30)

# players/pawns need the gamefield to appropriately resize the pawn images
gamefield = GameField.GameField(text_font)

screen = Screen.Screen()

start_screen = StartScreen.StartScreen(screen, start_screen_font, theme_list)

player_count = start_screen.start_game()
# create new gamefield with updated theme
gamefield = GameField.GameField(text_font)
help = Help.Help(screen, start_screen_font, "Help.txt")
rules = Rules.Rules(screen, start_screen_font, "Rule.txt")

AI_TURN_TIME_DELAY = 1  # in seconds
AI_DIFFICULTY = 1  # currently the only difficulty
player_list = create_players(player_count, AI_TURN_TIME_DELAY, AI_DIFFICULTY)

engine = Engine.Engine(player_list, gamefield, rules, help)

victory = Victory.Victory(screen, engine, start_screen_font)


current_player = 0
has_won = False

while has_won == False:
    
    has_won = engine.player_turn(current_player)
    current_player += 1
    if current_player >= 4:
        current_player = 0

if current_player == 0:
    current_player = 3
else:
    current_player -= 1

victory.victory(current_player)

print("finish")

