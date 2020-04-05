import GameField
import Player
import Dice
import MapGamefieldToPosition
import pygame
import time


class Engine:
    player_list: []
    game_field: GameField
    dice: Dice

    def __init__(self, players: [Player, Player, Player, Player], gamefield: GameField):
        self.player_list = players
        self.game_field = gamefield
        self.dice = Dice.Dice(self.game_field)

        self.refresh_ui()

    def refresh_ui(self):
        self.game_field.show_screen()

        self.draw_pawns()

    def draw_pawns(self):
        for player in self.player_list:
            for pawn in player.pawn_list:
                x = MapGamefieldToPosition.get_coordinates(pawn.current_position)[0]
                y = MapGamefieldToPosition.get_coordinates(pawn.current_position)[1]
                self.game_field.show_text(pawn.image, pawn.color, x, y)

    def roll_dice(self):
        for i in range(10):
            number = self.dice.roll_dice()
            self.draw_pawns()
            pygame.display.update()
            time.sleep(0.01)
        return number

    def move_pawn_out_of_house(self, current_player: int):
        for pawn in self.player_list[current_player].pawn_list:
            if pawn.current_position > 40:
                pawn.move_pawn_out_of_house()
                self.refresh_ui()
                return

    # bewegt momentan immer den ersten pawn den es findet, geht aber ziemlich einfach indem man ne pawn_number benutzt
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

    def player_turn_human(self, current_player: int):
        turn = True
        while turn:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    rolled_number = self.roll_dice()

                    if rolled_number == 6 and self.player_list[current_player].has_pawn_in_house():
                        self.move_pawn_out_of_house(current_player)
                        rolled_number = self.roll_dice()
                        for pawn in self.player_list[current_player].pawn_list:
                            if pawn.current_position == (pawn.player_number - 1) * 10:
                                self.move_pawn(current_player, pawn.pawn_number, rolled_number)
                                break
                        if rolled_number != 6:
                            turn = False
                        break

                    elif self.player_list[current_player].has_pawn_on_field():
                        pawn_number = self.select_pawn()
                        while self.player_list[current_player].pawn_list[pawn_number - 1].current_position > 40:
                            pawn_number = self.select_pawn()
                        self.move_pawn(current_player, pawn_number, rolled_number)
                        if rolled_number != 6:
                            turn = False
                        break
                    else:
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
