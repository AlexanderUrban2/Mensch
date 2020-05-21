import pygame
import Screen
import Engine
import json


class Victory:

    screen_width: float
    screen_height: float

    screen_size_multiplier: float

    screen_class: Screen
    engine: Engine
    screen: pygame.display
    font: pygame.font

    background_image: pygame.image
    victory_image: pygame.image
    continue_button_image: pygame.image

    continue_button_image_rect: pygame.rect

    def __init__(self, screen: Screen, engine: Engine, font: pygame.font):
        self.screen_class = screen
        self.screen = self.screen_class.screen
        self.engine = engine

        self.init_images()

        self.font = font

        self.init_screen()

        self.victory_image = pygame.transform.smoothscale(self.victory_image, (int(self.screen_width/2), int(self.screen_height/2)))
        self.continue_button_image = pygame.transform.scale(self.continue_button_image, (int(self.screen_size_multiplier*2), int(self.screen_size_multiplier)))
        self.continue_button_image_rect = self.continue_button_image.get_rect(topleft = (self.screen_width/2 - self.continue_button_image.get_rect().size[0]/2, self.screen_width/2 + self.victory_image.get_rect().size[1]/2 + self.screen_size_multiplier))

        self.engine.refresh_ui()

    def init_images(self):
        with open('image_pack.txt') as json_file:
            data = json.load(json_file)
        self.background_image = pygame.image.load(data["background_image_game"])
        self.continue_button_image = pygame.image.load(data["continue_button_victory"])
        self.victory_image = pygame.image.load(data["victory_image"])

    def init_screen(self):

        self.screen_width = self.screen_class.screen_width
        self.screen_height = self.screen_class.screen_height

        self.screen_size_multiplier = self.screen_height / 11

    def victory(self, player):
        self.player_win_animation(player)
        victory_sound = pygame.mixer.Sound('music/victory_sound.wav')
        pygame.mixer.Sound.play(victory_sound)
        self.show_victory_screen(player)
        self.get_back_to_start()

    def player_win_animation(self, player):

        delay = 500

        current_time = pygame.time.get_ticks()
        change_time = current_time + delay
        show = True
        animation = True
        counter = 0

        while animation:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            # --- updates ---

            current_time = pygame.time.get_ticks()

            # is time to change ?
            if current_time >= change_time:
                # time of next change 
                change_time = current_time + delay
                if counter == 5:
                    animation = False
                elif (counter % 2) == 0:
                    self.overwrite_rect(player)
                    
                show = not show
                counter += 1

            if show:
                self.draw_rect(player)

    def show_victory_screen(self, player):
        
        self.screen.blit(self.victory_image, (self.screen_width/2 - self.victory_image.get_rect().size[0]/2, self.screen_size_multiplier/2))
        self.screen.blit(self.continue_button_image, (self.screen_width/2 - self.continue_button_image.get_rect().size[0]/2, self.screen_width/2 + self.victory_image.get_rect().size[1]/2 + self.screen_size_multiplier))
        
        pygame.draw.rect(self.screen, (255, 255, 255), (self.screen_size_multiplier*3.75, self.screen_size_multiplier*6.5, self.screen_size_multiplier*3.5, self.screen_size_multiplier))

        winning_text = "Player " + str(player+1) + " WinS"
        winning_text_font = self.font.render(winning_text, True, (0, 0, 0))
        self.screen.blit(winning_text_font, (self.screen_width/2 - winning_text_font.get_rect().size[0]/2,self.screen_size_multiplier*7 - winning_text_font.get_rect().size[1]/2))

        pygame.display.update()

        run = True

        while run:           
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and self.continue_button_image_rect.collidepoint(pygame.mouse.get_pos()):
                    run = False

    def get_back_to_start(self):
        pass

    def overwrite_rect(self, player):
        self.engine.game_field.show_screen()
        self.engine.draw_pawns()
        self.engine.dice.draw_dice_on_game_field()

        if player == 0:
            pygame.display.update((self.screen_size_multiplier, self.screen_size_multiplier*5, self.screen_size_multiplier*4, self.screen_size_multiplier))
        elif player == 1:
            pygame.display.update((self.screen_size_multiplier*5, self.screen_size_multiplier, self.screen_size_multiplier, self.screen_size_multiplier*4))
        elif player == 2:
            pygame.display.update((self.screen_size_multiplier*6, self.screen_size_multiplier*5, self.screen_size_multiplier*4, self.screen_size_multiplier))
        else:
            pygame.display.update((self.screen_size_multiplier*5, self.screen_size_multiplier*6, self.screen_size_multiplier, self.screen_size_multiplier*4))

    def draw_rect(self, player):
                # pygame.display.update((X_coord,Y_coord, Breite,Höhe))
                # 1 = -------
                # 2 = |  3= |
                # 4 = -------
        if player == 0:
            pygame.draw.rect(self.screen, (255, 0, 0), (self.screen_size_multiplier, self.screen_size_multiplier*5, self.screen_size_multiplier*4, self.screen_size_multiplier*0.1))
            pygame.draw.rect(self.screen, (255, 0, 0), (self.screen_size_multiplier, self.screen_size_multiplier*6 - self.screen_size_multiplier*0.1, self.screen_size_multiplier*4, self.screen_size_multiplier*0.1))
            pygame.draw.rect(self.screen, (255, 0, 0), (self.screen_size_multiplier, self.screen_size_multiplier*5, self.screen_size_multiplier*0.1, self.screen_size_multiplier))
            pygame.draw.rect(self.screen, (255, 0, 0), (self.screen_size_multiplier*5 - self.screen_size_multiplier*0.1, self.screen_size_multiplier*5, self.screen_size_multiplier*0.1, self.screen_size_multiplier))
            pygame.display.update((self.screen_size_multiplier, self.screen_size_multiplier*5, self.screen_size_multiplier*4, self.screen_size_multiplier))

        elif player == 1:
            pygame.draw.rect(self.screen, (255, 0, 0), (self.screen_size_multiplier*5, self.screen_size_multiplier, self.screen_size_multiplier, self.screen_size_multiplier*0.1))
            pygame.draw.rect(self.screen, (255, 0, 0), (self.screen_size_multiplier*5, self.screen_size_multiplier, self.screen_size_multiplier*0.1, self.screen_size_multiplier*4))
            pygame.draw.rect(self.screen, (255, 0, 0), (self.screen_size_multiplier*6 -self.screen_size_multiplier*0.1 , self.screen_size_multiplier, self.screen_size_multiplier*0.1, self.screen_size_multiplier*4))
            pygame.draw.rect(self.screen, (255, 0, 0), (self.screen_size_multiplier*5, self.screen_size_multiplier*5 - self.screen_size_multiplier*0.1, self.screen_size_multiplier, self.screen_size_multiplier*0.1))
            pygame.display.update((self.screen_size_multiplier*5, self.screen_size_multiplier, self.screen_size_multiplier, self.screen_size_multiplier*4))

        elif player == 2:
            pygame.draw.rect(self.screen, (255, 0, 0), (self.screen_size_multiplier*6, self.screen_size_multiplier*5, self.screen_size_multiplier*4, self.screen_size_multiplier*0.1))
            pygame.draw.rect(self.screen, (255, 0, 0), (self.screen_size_multiplier*6, self.screen_size_multiplier*5, self.screen_size_multiplier*0.1, self.screen_size_multiplier))
            pygame.draw.rect(self.screen, (255, 0, 0), (self.screen_size_multiplier*10 - self.screen_size_multiplier*0.1, self.screen_size_multiplier*5, self.screen_size_multiplier*0.1, self.screen_size_multiplier))
            pygame.draw.rect(self.screen, (255, 0, 0), (self.screen_size_multiplier*6, self.screen_size_multiplier*6 - self.screen_size_multiplier*0.1, self.screen_size_multiplier*4, self.screen_size_multiplier*0.1))
            pygame.display.update((self.screen_size_multiplier*6, self.screen_size_multiplier*5, self.screen_size_multiplier*4, self.screen_size_multiplier))

        else:
            pygame.draw.rect(self.screen, (255, 0, 0), (self.screen_size_multiplier*5, self.screen_size_multiplier*6, self.screen_size_multiplier, self.screen_size_multiplier*0.1))
            pygame.draw.rect(self.screen, (255, 0, 0), (self.screen_size_multiplier*5, self.screen_size_multiplier*6, self.screen_size_multiplier*0.1, self.screen_size_multiplier*4))
            pygame.draw.rect(self.screen, (255, 0, 0), (self.screen_size_multiplier*6 -self.screen_size_multiplier*0.1, self.screen_size_multiplier*6, self.screen_size_multiplier*0.1, self.screen_size_multiplier*4))
            pygame.draw.rect(self.screen, (255, 0, 0), (self.screen_size_multiplier*5, self.screen_size_multiplier*10 - self.screen_size_multiplier*0.1, self.screen_size_multiplier, self.screen_size_multiplier*0.1))
            pygame.display.update((self.screen_size_multiplier*5, self.screen_size_multiplier*6, self.screen_size_multiplier, self.screen_size_multiplier*4))


