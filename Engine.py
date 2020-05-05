import GameField
import Player
import Dice
import MapGamefieldToPosition
import pygame
import time
import Rules
import Help


class Engine:
    player_list: []
    game_field: GameField
    dice: Dice
    all_sprites: pygame.sprite.RenderPlain()
    rules: Rules
    help: Help

    rules_button_rect: pygame.rect
    help_button_rect: pygame.rect


    def __init__(self, players: [Player, Player, Player, Player], gamefield: GameField, rules: Rules, help: Help):
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
            if pawn.current_position > 40:
                pawn.move_pawn_out_of_house()
                self.refresh_ui()
                return

    def move_pawn(self, current_player: int, pawn_number: int, steps: int):
        for pawn in self.player_list[current_player].pawn_list:
            if pawn.pawn_number == pawn_number:
                if self.is_move_possible(current_player, pawn_number, steps) == True:
                    for i in range(steps):
                        pawn.move_pawn_one_step()
                        self.refresh_ui()
                        time.sleep(0.1)
                    self.check_hit(current_player, pawn_number)  
                    self.refresh_ui()  
                else:
                    self.refresh_ui()
                    self.game_field.show_text_info(current_player, "U can´t move this pawn. Move an other one!")
                    pawn_number = self.select_pawn()
                    self.move_pawn(current_player, pawn_number, steps) 
                    # einbauen von checken ob überhaupt ein move geht also außer von start aus

    def player_turn(self, current_player: int):
        if self.player_list[current_player].user_controlled:
            self.player_turn_human(current_player)
        else:
            self.player_turn_ai(current_player)


    def is_move_possible(self, current_player: int, pawn_number: int, steps: int) -> bool:
        is_move_possible = True
        final_position = 0
        for pawn in self.player_list[current_player].pawn_list:
            if pawn.pawn_number == pawn_number:
                if pawn.current_position + steps > 40:
                    final_position = pawn.current_position + steps -40
                else:
                    final_position = pawn.current_position + steps
        for pawn in self.player_list[current_player].pawn_list: 
            if pawn.pawn_number != pawn_number:
                if pawn.current_position == final_position:
                    return False
        return is_move_possible
        # einbauen von checken ob man ins häusle kann
        # einbauen von checken ob überhaupt ein move geht also außer von start aus         


    def check_hit(self,current_player: int, pawn_number: int):
        current_position = 0
        for pawn in self.player_list[current_player].pawn_list:
            if pawn.pawn_number == pawn_number:
                current_position = pawn.current_position
        for player_counter in range(4): 
            for pawn in self.player_list[player_counter].pawn_list: 
                if player_counter != current_player:
                    if pawn.current_position == current_position:
                        pawn.move_pawn_to_house(player_counter, pawn.pawn_number)
                        break

#--------------------------------- move pawn starting square        

    def move_pawn_from_starting_square(self, current_player: int, pawn_number: int, steps: int):
        for pawn in self.player_list[current_player].pawn_list:
            if pawn.pawn_number == pawn_number:
                for i in range(steps):
                    pawn.move_pawn_one_step()
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
                        pawn.move_pawn_to_house(player_counter, pawn.pawn_number)
                        break



    # mit 1, 2, 3, 4 kann ausgewählt werde, welcher pawn auf dem Spielfeld bewegt werden soll
    def player_turn_human(self, current_player: int):
        tries = 0
        turn = True

        while turn:
            self.game_field.show_text_info(current_player, "Press Space To Roll The Dice!")
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    rolled_number = self.roll_dice()

                    if rolled_number == 6 and self.player_list[current_player].has_pawn_in_house():
                        self.move_pawn_out_of_house(current_player)
                        self.check_hit(current_player, self.player_list[current_player].get_pawn_number_on_start_field())
                        self.refresh_ui()
                        self.game_field.show_text_info(current_player, "Press Space To Roll The Dice!")
                        self.wait_for_K_pressed()
                        rolled_number = self.roll_dice()
                        self.move_pawn_from_starting_square(current_player, self.player_list[current_player].get_pawn_number_on_start_field(), rolled_number)
                        self.game_field.show_text_info(current_player, "Moved pawn from Starting yard!")
                        if rolled_number != 6:
                            turn = False
                        else:
                            self.refresh_ui()
                        break

                    elif self.player_list[current_player].has_pawn_on_game_field():
                        select = True
                        while select:
                            pawn_number = self.select_pawn()
                            for pawn in self.player_list[current_player].pawn_list:
                                if pawn.current_position < 40:
                                    select = False
                                    break
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
        pass

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

    def wait_for_K_pressed(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return True
                if event.type == pygame.QUIT:
                    exit()