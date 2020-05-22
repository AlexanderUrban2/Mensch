import Player
import GameField
import pygame
import Engine
import StartScreen
import Rules
import Help
import Screen
import AI
import ImagePack
import Victory
'''
meme:
hit_enemy_pawn: Airh Horn Sound, permitted under Creative Commons (CC-by), Autor: Gingka Akiyama
https://lmms.io/lsp/?action=show&file=11017

unfortunate_sound: 8-bit error, permitted under Creative Commons 0 Licence
https://freesound.org/people/SamsterBirdies/sounds/363920/

victory_sound: youtube Audio-Mediathek

Stock audio - Free sound effects, loops and music.
 
Licence: The drum loop is permitted for commercial use under license Creative Commons "Attribution 4.0 International Licence"
Link to licence: https://creativecommons.org/licenses/by/4.0/legalcode
All following sound effects are permitted under the same licence:

default:
background_music: Bossa Nova Drum With Bass And Synth Rhythm, Artist: Alexander, posted by: Alexander
http://www.orangefreesounds.com/bossa-nova-drum-with-bass-and-synth-rhythm/

hit_enemy_pawn: Pop Sound Effect, Artist: Alexander, posted by: Alexander
http://www.orangefreesounds.com/pop-sound-effect/

hit_own_pawn: Fail Sound, Artist: Alexander, posted by: Alexander
http://www.orangefreesounds.com/fail-sound/

unfortunate_sound: Wrong Answer Sound Effect, Artist: Alexander, posted by: Alexander
http://www.orangefreesounds.com/wrong-answer-sound-effect/

victory_sound: Win Fanfare Sound, Artist: Alexander, posted by: Alexander
http://www.orangefreesounds.com/win-fanfare-sound/

meme:
background_musicmusic: Spongebob remix, Artist: /, posted by: Alexander
http://www.orangefreesounds.com/spongebob-remix/

hit_own_pawn: Roblox Death Sound, Artist: / , posted by: Alexander
http://www.orangefreesounds.com/roblox-death-sound/
'''


pygame.init()
pygame.font.init()
pygame.mixer.init()

pygame.mixer.music.load('music/background_music.wav')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(.03)


def create_players(player_count: int, ai_turn_time_delay: int, ai_difficulty: int):
    player_list = [Player.Player(i + 1) for i in range(player_count)]
    ai_list = [AI.AI(i + 1, ai_turn_time_delay, ai_difficulty) for i in range(player_count, 4)]
    for ai in ai_list:
        player_list.append(ai)
    return player_list


# current image packs: default, test
images = ImagePack.ImagePack("default")

my_font = pygame.font.SysFont("Arial", 50)
text_font = pygame.font.SysFont("Arial", 30)
start_screen_font = pygame.font.Font("Iveseenthatfacebefore.ttf", 30)

gamefield = GameField.GameField(text_font)

screen = Screen.Screen()

rules = Rules.Rules(screen, start_screen_font, "Rule.txt")
help = Help.Help(screen, start_screen_font, "Help.txt")
start_screen = StartScreen.StartScreen(screen, rules, start_screen_font)

player_count = start_screen.start_game()

AI_TURN_TIME_DELAY = 1  # in seconds
AI_DIFFICULTY = 1
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
#Bugs:
# code ist leicht unübersichtlich
