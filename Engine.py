# Author: Christoph Böhringer, Alexander Urban
# Date: 05/28/2020
# Version: 11.2

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

    """
                desc: 
                    - init
                param:
                    - players: [Player, Player, Player, PLayer] -> list of all player objects that are participating in
                                                                   the game
                    - gamefield: GameField -> GameField object on which texts, images and the pawns get blit on the screen
                    - rules: Rules -> the rules screen that gets shown when pressing the 'Rules' button
                    - help: Help -> the help screen that gets shown when pressing the 'Help' button
                return:
                    - none
    """
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

    def get_all_sprites(self):
        for player in self.player_list:
            for pawn in player.pawn_list:
                self.all_sprites.add(pawn)

    """
    desc: 
        - refresh game screen completely
    param:
        - none
    return:
        - none
    """
    def refresh_ui(self):
        self.game_field.show_screen()
        self.draw_pawns()
        self.dice.draw_dice_on_game_field()
        pygame.display.update()

    def draw_pawns(self):
        self.all_sprites.update()
        self.all_sprites.draw(self.game_field.screen)

    """
    desc: 
        - roll the die
    param:
        - none
    return:
        - number - int
    """
    def roll_dice(self):
        for i in range(10):
            number = self.dice.roll_dice()
            # wait in order to create an 'animation'
            self.active_sleep(0.02)
        return number
    
    """
    desc: 
        - roll the die and update only the frame of the die
    param:
        - current_player - int
    return:
        - none
    """
    def move_pawn_out_of_house(self, current_player: int):
        for pawn in self.player_list[current_player].pawn_list:
            if pawn.is_in_players_yard():
                pawn.move_pawn_out_of_house()
                self.check_hit(current_player, pawn.pawn_number)
                self.refresh_ui()
                return

    """
            desc: 
                - 
            param:
                - current_player: int -> position of player object in self.player_list[]
                - pawn_number: int -> number of the pawn object that should be moved
                - steps: int -> number of steps the pawn takes
            return:
                - none
    """
    def move_pawn(self, current_player: int, pawn_number: int, steps: int):
        for pawn in self.player_list[current_player].pawn_list:
            if pawn.pawn_number == pawn_number:
                for i in range(steps):
                    pawn.move_pawn_one_step()
                    self.refresh_ui()
                    # wait between each step in order to create an 'animation'
                    self.active_sleep(0.1)
                self.check_hit(current_player, pawn_number)  
                self.refresh_ui()
                return

    def player_turn(self, current_player: int):
        if self.player_list[current_player].__class__.__name__ == "AI":
            self.player_turn_ai(current_player)
        elif self.player_list[current_player].__class__.__name__ == "Player":
            self.player_turn_human(current_player)

        return self.player_list[current_player].has_won()

    """
    desc: 
        - check if move is possible
    param:
        - current_player - int
        - pawn_number - int
        - steps - int
    return:
        - is_move_possible - bool
    ------------
    test:
        tmp = 0
        for pawn in self.player_list[0].pawn_list:
                if tmp == 0:
                    pawn.current_position = 39
                    tmp = 1020
                else:
                    pawn.current_position = tmp
                    tmp += 10
        #set all 4 pawns of the first player into house

        result = is_move_possible(0, 1, 4)
        Assert.isFalse(result)

        # pawn shouldn't be able to move --> test fails if method returns true
    """
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

    """
            desc: 
                - check if a pawn can move in the finishing squares
            param:
                - current_player: int -> position of player object in self.player_list[]
                - pawn_number: int -> number of the pawn object that should be moved
                - steps: int -> number of steps that the pawn takes
            return:
                - none
    """
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

    """
    desc: 
        - check if any move of current player is possible
    param:
        - current_player - int
        - pawn_number - int
        - steps - int
    return:
        - is_any_move_possible - bool
    """
    def is_any_move_possible(self, current_player: int, steps: int) -> bool:
        for pawn in self.player_list[current_player].pawn_list:
            # check if the pawn can be moved
            if self.is_move_possible(current_player, pawn.pawn_number, steps):
                return True
        # no pawn could be moved -> return False
        return False

    """
    desc: 
        - check if this move hits a pawn
    param:
        - current_player - int
        - pawn_number - int
    return:
        - is_hit - bool
    """
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
                        self.sound_helper.play_sound("hit_enemy_pawn_sound")

                        pawn.move_pawn_to_house()
                        return

    # different method because a pawn HAS to be moved from the starting square immediately
    def move_pawn_from_starting_square(self, current_player: int, pawn_number: int, steps: int):
        for pawn in self.player_list[current_player].pawn_list:
            if pawn.pawn_number == pawn_number:
                for i in range(steps):
                    pawn.move_pawn_one_step()
                    self.refresh_ui()
                    # wait in order to create an 'animation'
                    self.active_sleep(0.1)
                self.check_hit_from_starting_square(current_player, pawn_number)  
                self.refresh_ui()

    """
                desc: 
                    - different method because when moving from a player's starting square a pawn can hit 
                      friendly pawns as well as enemy pawns
                param:
                    - current_player: int -> position of player object in self.player_list[]
                    - pawn_number: int -> number of the pawn object on the starting square
                return:
                    - none
    """
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

    """
                desc: 
                    - turn of a human player; space needs to be pressed before rolling the die;
                      player selects the pawn that they want to move with the number 1, 2, 3 and 4 on the keyboard;
                      three tries to roll a six if the player has no pawn on the game field
                param:
                    - current_player: int -> position of the player object in self.player_list[]
                return:
                    - none
    """
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
                    
                    # rolled a six and has a pawn in yard -> move a pawn out of the yard
                    if rolled_number == 6 and self.player_list[current_player].has_pawn_in_yard():
                        self.move_pawn_out_of_house(current_player)
                        self.game_field.show_text_info(current_player, "Press space to roll the die!")
                        self.wait_for_space_pressed(current_player)
                        # rolled a six -> player can roll the die again
                        rolled_number = self.roll_dice()
                        self.move_pawn_from_starting_square(current_player, self.player_list[current_player].get_pawn_number_on_start_field(), rolled_number)
                        self.game_field.show_text_info(current_player, "Moved token from starting square!")
                        if rolled_number != 6:
                            # no six -> turn ends
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

                            # if you rolled a six you get another turn
                            if rolled_number == 6:
                                self.active_sleep(1)
                                self.refresh_ui()
                                self.player_turn_human(current_player)
                            return

                        select = True
                        self.refresh_ui()
                        # select a pawn and check if that pawn can move
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

                self.check_pygame_events(event)

    """
                desc: 
                    - turn of an AI; currently only one difficulty, so pawn selection is random;
                      turn starts after turn_time_delay is over in order to slow down the AI turn so that normal 
                      players can see whats going on; 
                      no space press needed, rest is same as player_turn_human
                param:
                    - current_player: int -> position of player object in self.player_list[]
                return:
                    - none
    """
    def player_turn_ai(self, current_player: int):
        tries = 0
        turn = True
        time_previous = time.time()

        while turn:
            # time.time() is in seconds!!, or not.. it can be depending on the processor...
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

                    # slow down the AI or it could be too fast for a player if they aren't paying attention
                    self.active_sleep(0.5)

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

                        # you get another turn when you roll a six
                        if rolled_number == 6:
                            self.active_sleep(1)
                            self.refresh_ui()
                            self.player_turn_human(current_player)
                        return

                    time_previous = time_now

                    selecting = True
                    self.refresh_ui()

                    while selecting:
                        # select a pawn, difficulty can currently only be 1... -> pawn is selected randomly
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
                    # as above... makes it easier to follow the game
                    self.active_sleep(0.5)
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
                self.check_pygame_events(event)

    """
                desc: 
                    - check all possible events that need to be handled
                param:
                    - event: pygame.event -> event to check
                return:
                    - none
    """
    def check_pygame_events(self, event: pygame.event):
        if event.type == pygame.QUIT:
            exit()
        # if the rules button is clicked show the rules screen
        elif event.type == pygame.MOUSEBUTTONDOWN and self.rules_button_rect.collidepoint(pygame.mouse.get_pos()):
            self.rules.show_screen()
            self.refresh_ui()
        # if the help button is clicked show the help screen
        elif event.type == pygame.MOUSEBUTTONDOWN and self.help_button_rect.collidepoint(pygame.mouse.get_pos()):
            self.help.show_screen()
            self.refresh_ui()
        # if the sound button is clicked stop/resume sound effects and background music
        elif event.type == pygame.MOUSEBUTTONDOWN and self.game_field.ingame_sound_button_rect.collidepoint(
                pygame.mouse.get_pos()):
            if pygame.mixer.music.get_busy():
                self.sound_helper.stop_background_music()
                self.sound_helper.stop_channel()
                self.refresh_ui()
            else:
                self.sound_helper.play_background_music()
                self.sound_helper.resume_channel()
                self.refresh_ui()

    """
                desc: 
                    - selection of the pawn_number for the pawn object that should be moved
                param:
                    - none
                return:
                    - number of the pawn that should be moved
    """
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
                self.check_pygame_events(event)

    """
    desc: 
        - wait till space is pressed and then call function
    param:
        - current_player - int
    return:
        - space_pressed - bool
    """
    def wait_for_space_pressed(self, current_player: int):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return True
                self.check_pygame_events(event)
            self.game_field.show_text_info(current_player, "Press space to roll the die!")

    """
    desc:
        - allows the user to interact with the help/rules and sound button while "animations" are going on
            or while the AI waits to make its turn
    params:
        - time_to_wait: float -> time the program will wait in seconds
    return:
        - none
    """
    def active_sleep(self, time_to_wait: float):
        start_time = time.time()
        current_time = time.time()
        while (current_time - start_time) < time_to_wait:
            for event in pygame.event.get():
                self.check_pygame_events(event)
            current_time = time.time()

