import GameField
import Player
import Dice
import pygame
import time
import Rules
import Help
import random
import SoundHelper


class Engine:
    player_list: []
    game_field: GameField
    dice: Dice
    all_sprites: pygame.sprite.RenderPlain()
    rules: Rules
    help: Help

    sound_helper: SoundHelper

    rules_button_rect: pygame.rect
    help_button_rect: pygame.rect

    def __init__(self, players: [Player, Player, Player, Player], gamefield: GameField, rules: Rules, help: Help):
        self.sound_helper = SoundHelper.SoundHelper()
        self.player_list = players
        self.game_field = gamefield
        self.dice = Dice.Dice(self.game_field)
        self.all_sprites = pygame.sprite.RenderPlain()
        self.rules = rules
        self.help = help

        self.rules_button_rect = gamefield.ingame_rules_button_rect
        self.help_button_rect = gamefield.ingame_help_button_rect

        self.get_all_sprites()
        self.refresh_ui()

        #tmp = 0
        #for pawn in self.player_list[0].pawn_list:
        #        if tmp == 0:
        #            pawn.current_position = 39
        #            tmp = 1020
        #        else:
        #            pawn.current_position = tmp
        #            tmp += 10

        #tmp = 0
        #for counter in range(4):
        #    if counter == 0:
        #        tmp = 39
        #    else: 
        #        tmp = 9
        #        tmp +=  10 * (counter-1)
        #    for pawn in self.player_list[counter].pawn_list: 
        #        if pawn.pawn_number == 1:
        #            pawn.current_position = tmp

    def get_all_sprites(self):
        for player in self.player_list:
            for pawn in player.pawn_list:
                self.all_sprites.add(pawn)

    def refresh_ui(self):
        self.game_field.show_screen()
        self.draw_pawns()
        self.dice.draw_dice_on_game_field()
        pygame.display.update()

    def draw_pawns(self):
        self.all_sprites.update()
        self.all_sprites.draw(self.game_field.screen)

    def roll_dice(self):
        for i in range(10):
            number = self.dice.roll_dice()
            time.sleep(0.02)
        return number
    
    # rollt den würfel und updated nur das aussehen der frames im "würfelbereich"
    def move_pawn_out_of_house(self, current_player: int):
        for pawn in self.player_list[current_player].pawn_list:
            if pawn.is_in_players_yard():
                pawn.move_pawn_out_of_house()
                self.check_hit(current_player, pawn.pawn_number)
                self.refresh_ui()
                return

    def move_pawn(self, current_player: int, pawn_number: int, steps: int):
        for pawn in self.player_list[current_player].pawn_list:
            if pawn.pawn_number == pawn_number:
                for i in range(steps):
                    pawn.move_pawn_one_step()
                    self.refresh_ui()
                    time.sleep(0.1)
                self.check_hit(current_player, pawn_number)  
                self.refresh_ui()
                return

    def player_turn(self, current_player: int):
        if self.player_list[current_player].__class__.__name__ == "AI":
            self.player_turn_ai(current_player)
        elif self.player_list[current_player].__class__.__name__ == "Player":
            self.player_turn_human(current_player)
        
        return self.player_list[current_player].has_won()

    def is_move_possible(self, current_player: int, pawn_number: int, steps: int) -> bool:
        pawn = self.player_list[current_player].pawn_list[pawn_number - 1]

        # check if the pawn is still in the player's yard
        if pawn.is_in_players_yard():
            return False

        if current_player == 0:
            field_before_house = 39
        else:
            field_before_house = 39 - (4-current_player) * 10

        current_position = pawn.current_position

        # if the pawn is in the finishing squares check if it can move there
        if pawn.is_in_finishing_squares():
            return self.is_move_possible_in_finishing_squares(current_player, pawn.pawn_number, steps)

        # check if the pawn will enter the finishing squares
        for i in range(steps + 1):
            final_position = current_position + i
            if final_position == field_before_house:
                # check if the move is possible in the finishing squares with the remaining steps
                return self.is_move_possible_in_finishing_squares(current_player, pawn_number, steps - i)

        # check if the pawn moves over the final field of the playing field and set it back to 0
        if final_position > 39:
            final_position = current_position + steps - 40

        # check if the pawn would land on a field occupied by a pawn of the same player
        for pawn in self.player_list[current_player].pawn_list: 
            if pawn.pawn_number != pawn_number:
                if pawn.current_position == final_position:
                    return False

        return True

    # this function should only be called if a token is on the field in front of the finishing squares
    # or in the finishing squares
    # the steps parameter should only be the steps taken IN the finishing squares
    def is_move_possible_in_finishing_squares(self, current_player: int, pawn_number: int, steps: int) -> bool:
        pawn = self.player_list[current_player].pawn_list[pawn_number - 1]

        # if the pawn is not yet in the finishing squares set it on an imaginary finishing square 0
        # this is basically the field in front of the finishing squares
        if not pawn.is_in_finishing_squares():
            current_position = pawn.player_number * 1000
        else:
            current_position = pawn.current_position

        final_position = current_position + steps * 10
        if final_position > pawn.player_number * 1000 + 40:  # there are four finishing squares; x050 is out of bounds
            return False
        else:
            pawns_in_finishing_squares = self.player_list[current_player].get_pawns_in_finishing_squares()
            if not pawns_in_finishing_squares:  # if there are no pawns in the list, the move is possible
                return True

            for pawn_to_check in pawns_in_finishing_squares:
                if pawn_to_check.pawn_number != pawn.pawn_number:
                    # you can't jump over pawns in the finishing squares or land on the same position
                    if current_position < pawn_to_check.current_position <= final_position:
                        return False
            return True

    def is_any_move_possible(self, current_player: int, steps: int) -> bool:
        for pawn in self.player_list[current_player].pawn_list:
            # check if the pawn can be moved
            if self.is_move_possible(current_player, pawn.pawn_number, steps):
                return True
        # no pawn could be moved -> return False
        return False

    def check_hit(self, current_player: int, pawn_number: int):
        current_position = 0
        for pawn in self.player_list[current_player].pawn_list:
            if pawn.pawn_number == pawn_number:
                current_position = pawn.current_position
        for player in self.player_list:
            for pawn in player.pawn_list:
                if player.player_number - 1 != current_player:
                    if pawn.current_position == current_position:
                        # play sound when a pawn gets hit
                        #airhorn_sound = pygame.mixer.Sound('music/hit_enemy_pawn.wav')
                        #pygame.mixer.Sound.play(airhorn_sound)
                        self.sound_helper.play_sound("hit_enemy_pawn_sound")

                        pawn.move_pawn_to_house()
                        return

    def move_pawn_from_starting_square(self, current_player: int, pawn_number: int, steps: int):
        for pawn in self.player_list[current_player].pawn_list:
            if pawn.pawn_number == pawn_number:
                for i in range(steps):
                    pawn.move_pawn_one_step()
                    self.refresh_ui()
                    time.sleep(0.1)
                self.check_hit_from_starting_square(current_player, pawn_number)  
                self.refresh_ui()

    def check_hit_from_starting_square(self, current_player: int, pawn_number: int):
        current_position = 0
        for pawn in self.player_list[current_player].pawn_list:
            if pawn.pawn_number == pawn_number:
                current_position = pawn.current_position
        for player_counter in range(4): 
            for pawn in self.player_list[player_counter].pawn_list: 
                if player_counter == current_player and pawn.pawn_number == pawn_number:
                    pass
                else:
                    if pawn.current_position == current_position:

                        if player_counter == current_player:
                            self.sound_helper.play_sound("hit_own_pawn_sound")
                        else:
                            self.sound_helper.play_sound("hit_enemy_pawn_sound")

                        pawn.move_pawn_to_house()
                        break

    # mit 1, 2, 3, 4 kann ausgewählt werde, welcher pawn auf dem Spielfeld bewegt werden soll
    def player_turn_human(self, current_player: int):
        tries = 0
        turn = True

        while turn:
            if self.player_list[current_player].has_pawn_on_game_field():
                self.game_field.show_text_info(current_player, "Press space to roll the die!")
            else:
                self.game_field.show_text_info(current_player, "Press space to roll the die! (Turn " + str(tries + 1) + " of 3)")
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    rolled_number = self.roll_dice()

                    if rolled_number == 6 and self.player_list[current_player].has_pawn_in_yard():
                        self.move_pawn_out_of_house(current_player)
                        self.game_field.show_text_info(current_player, "Press space to roll the die!")
                        self.wait_for_space_pressed(current_player)
                        rolled_number = self.roll_dice()
                        self.move_pawn_from_starting_square(current_player, self.player_list[current_player].get_pawn_number_on_start_field(), rolled_number)
                        self.game_field.show_text_info(current_player, "Moved token from starting square!")
                        if rolled_number != 6:
                            turn = False
                        else:
                            self.refresh_ui()
                        break

                    elif self.player_list[current_player].has_pawn_on_game_field():
                        if not self.is_any_move_possible(current_player, rolled_number):
                            self.refresh_ui()
                            self.game_field.show_text_info(current_player, "Unfortunate!")
                            # no move is possible -> the turn ends
                            # play an error sound
                            self.sound_helper.play_sound("unfortunate_sound")
                            return

                        select = True
                        self.refresh_ui()

                        self.game_field.show_text_info(current_player, "Press the number key of the token you want to move!")
                        while select:
                            pawn_number = self.select_pawn()
                            for pawn in self.player_list[current_player].pawn_list:
                                if pawn.pawn_number == pawn_number:
                                    if self.is_move_possible(current_player, pawn_number, rolled_number):
                                        select = False
                                        break
                                    else:
                                        self.refresh_ui()
                                        self.game_field.show_text_info(current_player, "You can't move this token!")                            
                        self.move_pawn(current_player, pawn_number, rolled_number)
                        if rolled_number != 6:
                            # no six means your turn ends after a pawn is moved
                            return
                        self.refresh_ui()
                        break

                    else:
                        tries += 1
                        if tries >= 3:
                            turn = False
                        self.refresh_ui()
                        break
                elif event.type == pygame.MOUSEBUTTONDOWN and self.rules_button_rect.collidepoint(pygame.mouse.get_pos()):
                    self.rules.show_screen()
                    self.refresh_ui()
                elif event.type == pygame.MOUSEBUTTONDOWN and self.help_button_rect.collidepoint(pygame.mouse.get_pos()):
                    self.help.show_screen()
                    self.refresh_ui()
                elif event.type == pygame.MOUSEBUTTONDOWN and self.game_field.ingame_sound_button_rect.collidepoint(pygame.mouse.get_pos()):
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.stop()
                        self.sound_helper.stop_channel()
                        self.refresh_ui()
                    else:
                        pygame.mixer.music.load('music/background_music.wav')
                        pygame.mixer.music.play(-1)
                        self.sound_helper.resume_channel()
                        self.refresh_ui()

                elif event.type == pygame.QUIT:
                    exit()

    def player_turn_ai(self, current_player: int):
        tries = 0
        turn = True
        time_previous = time.time()

        while turn:
            # time.time() is in seconds!!
            time_now = time.time()

            if self.player_list[current_player].has_pawn_on_game_field():
                self.game_field.show_text_info(current_player, "AI turn :)")
            else:
                self.game_field.show_text_info(current_player, "AI turn :)   (Turn " + str(tries + 1) + " of 3)")

            # if the turn_time_delay is over start the turn
            if time_now - time_previous >= self.player_list[current_player].turn_time_delay:
                rolled_number = self.roll_dice()

                if rolled_number == 6 and self.player_list[current_player].has_pawn_in_yard():
                    self.move_pawn_out_of_house(current_player)

                    # I don't like this, but another loop would be worse
                    # and otherwise the AI could be too fast for a player if they aren't paying attention
                    time.sleep(0.5)

                    time_previous = time.time()

                    rolled_number = self.roll_dice()
                    self.move_pawn_from_starting_square(current_player, self.player_list[
                        current_player].get_pawn_number_on_start_field(), rolled_number)
                    self.game_field.show_text_info(current_player, "Moved token from starting square!")

                    if rolled_number != 6:
                        # the turn ends if a pawn was moved and no 6 was rolled
                        return
                    else:
                        self.refresh_ui()

                elif self.player_list[current_player].has_pawn_on_game_field():
                    if not self.is_any_move_possible(current_player, rolled_number):
                        self.refresh_ui()
                        self.game_field.show_text_info(current_player, "Unfortunate!")
                        # your turn ends if no pawn can be moved
                        # play an error sound
                        self.sound_helper.play_sound("unfortunate_sound")
                        return

                    time_previous = time_now

                    selecting = True
                    self.refresh_ui()

                    while selecting:
                        if self.player_list[current_player].difficulty == 1:
                            pawn_number = random.randint(1, 4)
                            for pawn in self.player_list[current_player].pawn_list:
                                if pawn.pawn_number == pawn_number:
                                    if self.is_move_possible(current_player, pawn_number, rolled_number):
                                        selecting = False
                                        break
                        else:
                            # implement other difficulties
                            pass
                    # as above... makes the game easier to follow
                    time.sleep(0.5)
                    self.move_pawn(current_player, pawn_number, rolled_number)
                    if rolled_number != 6:
                        # no 6 means your turn ends
                        return
                    self.refresh_ui()

                else:
                    time_previous = time.time()
                    tries += 1
                    if tries >= 3:
                        turn = False
                    self.refresh_ui()

            else:
                time_now = time.time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and self.rules_button_rect.collidepoint(pygame.mouse.get_pos()):
                    self.rules.show_screen()
                    self.refresh_ui()
                elif event.type == pygame.MOUSEBUTTONDOWN and self.help_button_rect.collidepoint(pygame.mouse.get_pos()):
                    self.help.show_screen()
                    self.refresh_ui()
                elif event.type == pygame.MOUSEBUTTONDOWN and self.game_field.ingame_sound_button_rect.collidepoint(pygame.mouse.get_pos()):
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.stop()
                        self.sound_helper.stop_channel()
                        self.refresh_ui()
                    else:
                        pygame.mixer.music.load('music/background_music.wav')
                        pygame.mixer.music.play(-1)
                        self.sound_helper.resume_channel()
                        self.refresh_ui()

    def select_pawn(self) -> int:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        return 1
                    elif event.key == pygame.K_2:
                        return 2
                    elif event.key == pygame.K_3:
                        return 3
                    elif event.key == pygame.K_4:
                        return 4
                if event.type == pygame.QUIT:
                    exit()

    def wait_for_space_pressed(self, current_player: int):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return True
                elif event.type == pygame.MOUSEBUTTONDOWN and self.rules_button_rect.collidepoint(pygame.mouse.get_pos()):
                    self.rules.show_screen()
                    self.refresh_ui()
                    self.game_field.show_text_info(current_player, "Press space to roll the die!")
                elif event.type == pygame.MOUSEBUTTONDOWN and self.help_button_rect.collidepoint(pygame.mouse.get_pos()):
                    self.help.show_screen()
                    self.refresh_ui()
                    self.game_field.show_text_info(current_player, "Press space to roll the die!")
                if event.type == pygame.QUIT:
                    exit()
