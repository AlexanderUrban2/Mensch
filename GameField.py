import ctypes
import pygame


class GameField:
    screen_width: float
    screen_height: float

    screen_size_multiplier: float

    screen: pygame.display
    font: pygame.font

    background_image: pygame.image

    def __init__(self, background_image: pygame.image, font: pygame.font):
        self.background_image = background_image
        self.font = font

        self.init_game_field_variables()

        self.build_game_screen()

    def init_game_field_variables(self):
        user32 = ctypes.windll.user32

        self.screen_width = int(user32.GetSystemMetrics(1) * 0.9)
        self.screen_height = int(user32.GetSystemMetrics(1) * 0.9)

        self.screen_size_multiplier = self.screen_height / 11

    def build_game_screen(self):
        self.background_image = pygame.transform.smoothscale(self.background_image, (self.screen_width, self.screen_height))
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Mensch ärgere dich nicht")
        self.surface_dice = self.screen.subsurface((self.screen_size_multiplier * 5,self.screen_size_multiplier * 5),(self.screen_size_multiplier,self.screen_size_multiplier))
        self.surface_dice_blank = self.surface_dice.copy()

    def show_screen(self):
        self.screen.blit(self.background_image, (0, 0))
        pygame.display.update()

    # Koordinaten entsprechen den Feldern einer 11*11 Matrix
    def show_image(self, image: pygame.image, x_coordinate: int, y_coordinate: int, picture_type: str):
        if x_coordinate != 0:
            x_coordinate = self.screen_size_multiplier * x_coordinate
        if y_coordinate != 0:
            y_coordinate = self.screen_size_multiplier * y_coordinate

        if picture_type == "dice":
            self.surface_dice.blit(self.background_image, (-x_coordinate, -y_coordinate))
            self.surface_dice.blit(image, (0,0))
            #surface zurücksetzen
            pygame.display.update()
        elif picture_type == "pawn":
            pass
            #pawn surface befehl

    def show_text(self, text: str, color, x_coordinate: int, y_coordinate: int):
        if x_coordinate != 0:
            x_coordinate = self.screen_size_multiplier * x_coordinate
        if y_coordinate != 0:
            y_coordinate = self.screen_size_multiplier * y_coordinate

        self.screen.blit(self.font.render(text, False, color), (x_coordinate + 20, y_coordinate))
        pygame.display.update()

    def show_text_info(self, player_number: int, text: str):

        text_part_one , text_part_two = self.split_text(text)

        if(player_number == 0):
            self.show_text(text_part_one, (0,0,0), 0, 2)
            self.show_text(text_part_two, (0,0,0), 0, 3)
        elif(player_number == 1):
            self.show_text(text_part_one, (0,0,0), 7, 2)
            self.show_text(text_part_two, (0,0,0), 7, 3)
        elif(player_number == 2):
            self.show_text(text_part_one, (0,0,0), 7, 7)
            self.show_text(text_part_two, (0,0,0), 7, 8)
        elif(player_number == 3):
            self.show_text(text_part_one, (0,0,0), 0, 7)
            self.show_text(text_part_two, (0,0,0), 0, 8)
        else:
            pass
        

    def split_text(self, text: str):
        
        text_part_one = [] 
        text_part_two = []

        text_width, text_height = self.font.size(text)
        limit =  3 * self.screen_size_multiplier
        #check if word is full in this row else move word one line down
        if text_width > limit:
            for c in text:
                text_width, text_height = self.font.size(''.join(text_part_one))
                if text_width <= limit:
                    text_part_one.append(c)
                else:
                    text_part_two.append(c) 
            return ''.join(text_part_one), ''.join(text_part_two)                  
        else:
            return text, ""


            