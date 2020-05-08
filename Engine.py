import GameField
import Player
import Dice
import MapGamefieldToPosition
import pygame
import time
import Rules
import Help
import random


class Engine:
    player_list: []
    game_field: GameField
    dice: Dice
    all_sprites: pygame.sprite.RenderPlain()
    rules: Rules
    help: Help

    rules_button_rect: pygame.rect
    help_button_rect: pygame.rect

    move_possible: bool

    def __init__(self, players: [Player, Player, Player, Player], gamefield: GameField, rules: Rules, help: Help):
        self.player_list = players
        self.game_field = gamefield
        self.dice = Dice.Dice(self.game_field)
        self.all_sprites = pygame.sprite.RenderPlain()
        self.rules = rules
        self.help = help

        self.rules_button_rect = gamefield.ingame_rules_button_rect
        self.help_button_rect = gamefield.ingame_help_button_rect

        self.move_possible = True

        self.get_all_sprites()
        self.refresh_ui()

        tmp = 0
        for counter in range(4):
            if counter == 0:
                tmp = 39
            else: 
                tmp = 9
                tmp +=  10 * (counter-1)
            for pawn in self.player_list[counter].pawn_list: 
                if pawn.pawn_number == 1:
                    pawn.current_position = tmp

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
            if pawn.current_position > 40 and pawn.current_position < 1000:
                pawn.move_pawn_out_of_house()
                self.refresh_ui()
                return

    def move_pawn(self, current_player: int, pawn_number: int, steps: int):
        for pawn in self.player_list[current_player].pawn_list:
            if pawn.pawn_number == pawn_number:
                # if self.is_move_possible(current_player, pawn_number, steps):
                    for i in range(steps):
                        pawn.move_pawn_one_step(current_player)
                        self.refresh_ui()
                        time.sleep(0.1)
                    self.check_hit(current_player, pawn_number)  
                    self.refresh_ui()
                    return
                #else:
                #    self.refresh_ui()
                #    self.game_field.show_text_info(current_player, "You can´t move this token!")
                #    pawn_number = self.select_pawn()
                #    self.move_pawn(current_player, pawn_number, steps)
                    # einbauen von checken ob überhaupt ein move geht also außer von start aus

    def player_turn(self, current_player: int):
        if self.player_list[current_player].__class__.__name__ == "AI":
            self.player_turn_ai(current_player)
        elif self.player_list[current_player].__class__.__name__ == "Player":
            self.player_turn_human(current_player)

#-------------------------------- check move possible

    def is_move_possible(self, current_player: int, pawn_number: int, steps: int) -> bool:
        is_move_possible = True
        final_position = 0
        for pawn in self.player_list[current_player].pawn_list:
            if pawn.pawn_number == pawn_number:
                if self.is_move_possible_into_house(current_player, pawn_number, steps, pawn) == False:
                    is_move_possible =  False
                elif pawn.current_position + steps > 39:
                    final_position = pawn.current_position + steps - 40
                else:
                    final_position = pawn.current_position + steps
        for pawn in self.player_list[current_player].pawn_list: 
            if pawn.pawn_number != pawn_number:
                if pawn.current_position == final_position:
                    is_move_possible = False

        return is_move_possible

    def is_move_possible_into_house (self, current_player: int, pawn_number: int, steps: int, pawn):
        final_position = 0
        field_before_house = 0
        if current_player == 0:
            field_before_house = 39
        else:
            field_before_house = 39 - (4-current_player) *10
        tmp = 0
        first_pawn_in_house = 0

        if pawn.current_position > 1000:
            final_position = pawn.current_position + steps*10
        else:
            for counter in range(steps):
                if counter + pawn.current_position == field_before_house:
                    tmp = counter
                    break
                else:
                    return True
            steps -= counter
            final_position = (current_player+1) * 1000 + steps * 10
        if final_position > (current_player+1) * 1000 + 40:
            return False
        else:
            for pawn in self.player_list[current_player].pawn_list: 
                if pawn.pawn_number != pawn_number:
                    if pawn.current_position > first_pawn_in_house and pawn.current_position > 1000:
                        first_pawn_in_house = pawn.current_position
            if first_pawn_in_house >= final_position:
                return False
            else:
                return True

    def check_if_any_move_is_possible(self, current_player: int, steps: int) -> bool:
        is_move_possible = True
        pawn_number = 0
        final_position = 0
        for pawn in self.player_list[current_player].pawn_list:
            pawn_number = pawn.pawn_number
            if self.is_move_possible_into_house(current_player, pawn_number, steps, pawn) == False:
                is_move_possible =  False
            elif pawn.current_position > 100 and pawn.current_position < 1000:
                is_move_possible = False
            elif pawn.current_position + steps > 39:
                final_position = pawn.current_position + steps - 40
                for pawn in self.player_list[current_player].pawn_list: 
                    if pawn.pawn_number != pawn_number:
                        if pawn.current_position == final_position:
                            is_move_possible = False
                        else:
                            return True
            else:
                final_position = pawn.current_position + steps
                for pawn in self.player_list[current_player].pawn_list: 
                    if pawn.pawn_number != pawn_number:
                        if pawn.current_position == final_position:
                            is_move_possible = False
                        else:
                            return True
            

        return is_move_possible
            

    def check_hit(self,current_player: int, pawn_number: int):
        current_position = 0
        for pawn in self.player_list[current_player].pawn_list:
            if pawn.pawn_number == pawn_number:
                current_position = pawn.current_position
        for player_counter in range(4): 
            for pawn in self.player_list[player_counter].pawn_list: 
                if player_counter != current_player:
                    if pawn.current_position == current_position:
                        pawn.move_pawn_to_house()
                        return

# --------------------------------- move pawn starting square

    def move_pawn_from_starting_square(self, current_player: int, pawn_number: int, steps: int):
        for pawn in self.player_list[current_player].pawn_list:
            if pawn.pawn_number == pawn_number:
                for i in range(steps):
                    pawn.move_pawn_one_step(current_player)
                    self.refresh_ui()
                    time.sleep(0.1)
                self.check_hit_from_starting_square(current_player, pawn_number)  
                self.refresh_ui()

    def check_hit_from_starting_square(self,current_player: int, pawn_number: int):
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

                    if rolled_number == 6 and self.player_list[current_player].has_pawn_in_house():
                        self.move_pawn_out_of_house(current_player)
                        self.check_hit(current_player, self.player_list[current_player].get_pawn_number_on_start_field())
                        self.refresh_ui()
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
                        self.move_possible = self.check_if_any_move_is_possible(current_player, rolled_number)
                        if self.move_possible == False:
                            self.refresh_ui()
                            self.game_field.show_text_info(current_player, "Unfortunate!")
                            select = False
                            turn = False
                            self.move_possible = True
                            break

                        select = True
                        self.refresh_ui()

                        self.game_field.show_text_info(current_player, "Press the number key of the token you want to move!")
                        while select:
                            pawn_number = self.select_pawn()
                            for pawn in self.player_list[current_player].pawn_list:
                                if pawn.pawn_number == pawn_number:
                                    if pawn.current_position < 40 and self.is_move_possible(current_player, pawn_number, rolled_number):
                                        select = False
                                        break
                                    elif pawn.current_position > 1000 and self.is_move_possible_into_house(current_player, pawn_number, rolled_number, pawn):
                                        select = False
                                        break
                                    else:
                                        self.refresh_ui()
                                        self.game_field.show_text_info(current_player, "You can't move this token!")                            
                        self.move_pawn(current_player, pawn_number, rolled_number)
                        if rolled_number != 6:
                            turn = False
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

            if time_now - time_previous >= self.player_list[current_player].turn_time_delay:
                rolled_number = self.roll_dice()

                if rolled_number == 6 and self.player_list[current_player].has_pawn_in_house():
                    self.move_pawn_out_of_house(current_player)
                    self.check_hit(current_player, self.player_list[current_player].get_pawn_number_on_start_field())
                    self.refresh_ui()

                    # I don't like this, but another loop would be worse
                    # and otherwise the AI could be too fast for a player if they aren't paying attention
                    time.sleep(0.5)

                    time_previous = time.time()

                    rolled_number = self.roll_dice()
                    self.move_pawn_from_starting_square(current_player, self.player_list[
                        current_player].get_pawn_number_on_start_field(), rolled_number)
                    self.game_field.show_text_info(current_player, "Moved token from starting square!")

                    if rolled_number != 6:
                        turn = False
                    else:
                        self.refresh_ui()

                elif self.player_list[current_player].has_pawn_on_game_field():
                    self.move_possible = self.check_if_any_move_is_possible(current_player, rolled_number)
                    if self.move_possible == False:
                            self.refresh_ui()
                            self.game_field.show_text_info(current_player, "Unfortunate!")
                            turn = False
                            self.move_possible = True
                            break

                    time_previous = time_now

                    selecting = True
                    self.refresh_ui()

                    while selecting:
                        if self.player_list[current_player].difficulty == 1:
                            pawn_number = random.randint(1, 4)
                            for pawn in self.player_list[current_player].pawn_list:
                                if pawn.pawn_number == pawn_number:
                                    if pawn.current_position < 40 and self.is_move_possible(current_player, pawn_number,
                                                                                            rolled_number):
                                        selecting = False
                                        break
                                    elif pawn.current_position > 1000 and self.is_move_possible_into_house(current_player, pawn_number, rolled_number, pawn):
                                        selecting = False
                                        break
                        else:
                            # implement other difficulties
                            pass
                    # as above... makes the game easier to follow
                    time.sleep(0.5)
                    self.move_pawn(current_player, pawn_number, rolled_number)
                    if rolled_number != 6:
                        turn = False
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