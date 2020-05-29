# Author: Christoph Böhringer, Alexander Urban
# Date: 05/28/2020
# Version: 3.4

import pygame
import MapGamefieldToPosition
import json


class Pawn(pygame.sprite.Sprite):
    image: pygame.image
    rect: pygame.rect
    current_position: int
    pawn_number: int
    player_number: int
    pawn_image: pygame.image

    """
    desc: 
        - init
    param:
        - pawn_number: int -> used to differentiate between pawns
        - plyaer_number: int -> number of the player object that the pawns belong to
    return:
        - none
    """
    def __init__(self, pawn_number: int, player_number: int):
        pygame.sprite.Sprite.__init__(self)
        self.pawn_number = pawn_number
        self.player_number = player_number
        self.current_position = player_number * 100 + pawn_number * 10

        self.init_images()
        self.create_picture()

        self.rect = self.image.get_rect()

    def init_images(self):
        with open('image_pack.txt') as json_file:
            data = json.load(json_file)
        self.pawn_image = pygame.image.load(data["pawn_player_" + str(self.player_number)])

    """
    desc: 
        - resize the image of the pawn and draw its pawn_number on it
    param:
        - none
    return:
        - none
    """
    def create_picture(self):
        #  get the size of a field of the 11*11 matrix
        height = pygame.display.get_surface().get_size()[0] // 11
        width = pygame.display.get_surface().get_size()[1] // 11

        # make the surface transparent
        self.image = pygame.Surface([height, width], pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))

        radius = height // 3
        self.pawn_image = pygame.transform.smoothscale(self.pawn_image, (radius * 2, radius * 2))
        self.image.blit(self.pawn_image, (height // 2 - self.pawn_image.get_width() // 2, width // 2 - self.pawn_image.get_height() // 2))
        font = pygame.font.Font(None, radius)
        text = font.render(str(self.pawn_number), True, (0, 0, 0))
        self.image.blit(text, (height // 2 - text.get_width() // 2, width // 2 - text.get_height() // 2))

    def move_pawn_out_of_house(self):
        # this is the starting position of the player
        self.current_position = (self.player_number - 1) * 10

    def move_pawn_to_house(self):
        self.current_position = self.player_number * 100 + self.pawn_number * 10

    def is_in_finishing_squares(self):
        # 1000 is the number at which the finishing squares start in MapGamefieldToPosition.py
        return self.current_position > 1000

    def move_pawn_one_step(self):
        if self.can_move_into_finishing_squares():
            # move the pawn into the finishing squares
            self.current_position = self.player_number * 1000 + 10
        elif self.is_in_finishing_squares():
            # move the pawn in the finishing squares
            self.current_position += 10
        else:
            self.current_position += 1
            # if the pawn is at the 'end' of the 'circle' set it back to the start
            if self.current_position > 39:
                self.current_position = 0
    
    def can_move_into_finishing_squares(self) -> bool:
        if self.player_number == 1:
            field_before_finishing_squares = 39
        else:
            field_before_finishing_squares = self.player_number * 10 - 11

        if self.current_position == field_before_finishing_squares:
            return True
        return False

    def is_in_players_yard(self) -> bool:
        # numbers used in MapGamefieldToPosition.py for the yard fields of a player range from 100 to 440
        return 40 < self.current_position < 1000

    """
    desc: 
        - update method for the sprites
    param:
        - none
    return:
        - none
    """
    def update(self):
        x = MapGamefieldToPosition.get_coordinates(self.current_position)[0]
        y = MapGamefieldToPosition.get_coordinates(self.current_position)[1]
        display_size_x = pygame.display.get_surface().get_size()[0]
        display_size_y = pygame.display.get_surface().get_size()[1]
        # the background is not a perfect 11*11 matrix and as such the pawn images need to be moved a tiny bit
        self.rect.x = x * (display_size_x // 11) + display_size_x/216
        self.rect.y = y * (display_size_y // 11) + display_size_y/216
        return
