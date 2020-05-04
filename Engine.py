import GameField
import Player
import Dice
import pygame
import time


class Engine:
    player_list: []
    game_field: GameField
    dice: Dice
    all_sprites: pygame.sprite.RenderPlain()

    def __init__(self, players: [Player, Player, Player, Player], gamefield: GameField):
        self.player_list = players
        self.game_field = gamefield
        self.dice = Dice.Dice(self.game_field)
        self.all_sprites = pygame.sprite.RenderPlain()

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
        #for player in self.player_list:
            #for pawn in player.pawn_list:
            #    x = MapGamefieldToPosition.get_coordinates(pawn.current_position)[0]
            #    y = MapGamefieldToPosition.get_coordinates(pawn.current_position)[1]
            #    self.game_field.show_text(pawn.image, pawn.color, x, y)
         #   player.pawn_list.update()
         #   player.pawn_list.draw(self.game_field.screen)
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
                for i in range(steps):
                    pawn.move_pawn_one_step()
                    self.refresh_ui()
                    time.sleep(0.1)
                return

    def player_turn(self, current_player: int):
        if self.player_list[current_player].user_controlled:
            self.player_turn_human(current_player)
        else:
            self.player_turn_ai(current_player)

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
                        rolled_number = self.roll_dice()
                        self.move_pawn(current_player, self.player_list[current_player].get_pawn_number_on_start_field(), rolled_number)
                        if rolled_number != 6:
                            turn = False
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
                        break

                    else:
                        tries += 1
                        if tries >= 3:
                            turn = False
                        break
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
