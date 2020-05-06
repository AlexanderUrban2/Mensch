import ctypes
import pygame
import Screen
import Rules
import ImagePack


class StartScreen:
    screen_width: float
    screen_height: float

    player_counter: int

    start_game_message_rect: pygame.rect
    rule_message_rect: pygame.rect
    start_game_button_rect: pygame.rect
    hidden_rect: pygame.rect
    player_arrow_up_rect: pygame.rect
    player_arrow_down_rect: pygame.rect
    player_counter_rect: pygame.rect

    screen: pygame.display
    font: pygame.font
    run: bool

    background_image: pygame.image
    start_button: pygame.image
    maedn_logo: pygame.image
    player_arrow_up: pygame.image
    player_arrow_down: pygame.image


    screen_class: Screen
    rules: Rules
    image_pack: ImagePack

    def __init__(self, screen_class: Screen, rules: Rules, font: pygame.font):
        self.image_pack = ImagePack.ImagePack()

        self.background_image = self.image_pack.background_image_start_screen
        self.start_button = self.image_pack.start_button
        self.maedn_logo = self.image_pack.maedn_logo
        self.player_arrow_up = self.image_pack.player_arrow_up
        self.player_arrow_down = self.image_pack.player_arrow_down

        self.font = font
        self.run = True

        self.rules = rules

        self.screen_class = screen_class
        self.screen = self.screen_class.screen
        self.screen_width = self.screen_class.screen_width
        self.screen_height = self.screen_class.screen_height

        self.player_counter = 1

        self.build_game_screen()
        

    def build_game_screen(self):
        self.background_image = pygame.transform.smoothscale(self.background_image, (self.screen_width, self.screen_height))
        self.maedn_logo = pygame.transform.smoothscale(self.maedn_logo, (int(self.screen_width *0.03), int(self.screen_height*0.03)))
        self.player_arrow_up = pygame.transform.smoothscale(self.player_arrow_up, (int(self.screen_width*0.05), int(self.screen_height*0.05)))
        self.player_arrow_down = pygame.transform.smoothscale(self.player_arrow_down, (int(self.screen_width*0.05), int(self.screen_height*0.05)))


        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Mensch Ärgere dich nicht")
        self.screen.blit(self.background_image, (0, 0))
        hello_message = "Hi and welcome to \"Mensch ärgere dich nicht\""
        start_game_message = "Play"
        rule_message = "RuleS"
        player_text = "Number of PlayerS:"
        hello_message_font = self.font.render(hello_message, True, (0,0,0))
        start_game_message_font = self.font.render(start_game_message, True, (0,0,0))
        rule_message_font = self.font.render(rule_message, True, (0,0,0))
        player_text_font = self.font.render(player_text, True, (0,0,0))
        player_counter_font = self.font.render(str(self.player_counter), True, (0,0,0))
        player_counter_max_font = self.font.render("4", True, (0,0,0))

        self.start_game_message_rect = start_game_message_font.get_rect(topleft=(self.screen_width/2 - self.font.size(start_game_message)[0]/2, self.screen_height/3 + self.start_button.get_rect().size[1]/2))
        self.rule_message_rect = rule_message_font.get_rect(topleft=(self.screen_width/2 - self.font.size(rule_message)[0]/2, self.screen_height/3*2))
        self.start_game_button_rect = self.start_button.get_rect(topleft=(self.screen_width/2 - self.start_button.get_rect().size[0]/2, self.screen_height/3 - self.start_button.get_rect().size[1]/2))
        self.player_arrow_up_rect = self.player_arrow_up.get_rect(topleft=(self.screen_width* 0.65, self.screen_height/2 - self.player_arrow_up.get_rect().size[1] - 0.005 *self.screen_height))
        self.player_arrow_down_rect = self.player_arrow_down.get_rect(topleft=(self.screen_width* 0.65, self.screen_height/2 + 0.005 *self.screen_height))
        self.player_counter_rect = player_counter_max_font.get_rect(topleft=(self.screen_width*0.55, self.screen_height/2 - 0.5*self.font.size(player_text)[1]))

        self.screen.blit(hello_message_font, (self.screen_width/2 - self.font.size(hello_message)[0]/2,  self.font.size(hello_message)[1]))
        self.screen.blit(start_game_message_font, (self.screen_width/2 - self.font.size(start_game_message)[0]/2, self.screen_height/3 + self.start_button.get_rect().size[1]/2))
        self.screen.blit(rule_message_font, (self.screen_width/2 - self.font.size(rule_message)[0]/2, self.screen_height/1.5))
        self.screen.blit(player_text_font, (self.screen_width/2 - self.font.size(player_text)[0], self.screen_height/2 - 0.5*self.font.size(player_text)[1]))
        self.screen.blit(player_counter_font, (self.screen_width*0.55, self.screen_height/2 - 0.5*self.font.size(player_text)[1]))

        self.screen.blit(self.start_button, (self.screen_width/2 - self.start_button.get_rect().size[0]/2, self.screen_height/3 - self.start_button.get_rect().size[1]/2))
        self.screen.blit(self.player_arrow_up, (self.screen_width* 0.65, self.screen_height/2 - self.player_arrow_up.get_rect().size[1] - 0.005 *self.screen_height))
        self.screen.blit(self.player_arrow_down, (self.screen_width* 0.65, self.screen_height/2 + 0.005 *self.screen_height))


        self.hidden_rect = self.maedn_logo.get_rect(topleft=(0, self.screen_height - self.maedn_logo.get_rect().size[0]))
        self.screen.blit(self.maedn_logo, (0, self.screen_height - self.maedn_logo.get_rect().size[0]))

        pygame.display.update()
        

    def update_player_counter_on_screen(self):
        self.screen.blit(self.background_image, (0, 0))
        self.screen.blit(self.font.render(str(self.player_counter), True, (0,0,0)), (self.screen_width*0.55, self.screen_height/2 - 0.5*self.font.size("Number of PlayerS:")[1]))
        pygame.display.update(self.player_counter_rect)


    def start_game(self) -> int:
        while self.run:           
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and self.start_game_message_rect.collidepoint(pygame.mouse.get_pos()):
                    return self.player_counter
                elif event.type == pygame.MOUSEBUTTONDOWN and self.start_game_button_rect.collidepoint(pygame.mouse.get_pos()):
                    return self.player_counter
                elif event.type == pygame.MOUSEBUTTONDOWN and self.player_arrow_up_rect.collidepoint(pygame.mouse.get_pos()):
                    if self.player_counter +1 > 4:
                        self.player_counter = 1
                    else:
                        self.player_counter += 1
                    self.update_player_counter_on_screen()
                elif event.type == pygame.MOUSEBUTTONDOWN and self.player_arrow_down_rect.collidepoint(pygame.mouse.get_pos()):
                    if self.player_counter -1 < 1:
                        self.player_counter = 4
                    else:
                        self.player_counter -= 1
                    self.update_player_counter_on_screen()
                elif event.type == pygame.MOUSEBUTTONDOWN and self.hidden_rect.collidepoint(pygame.mouse.get_pos()):
                    self.run = False
                    #Hidden Kecks Quest einbauen
                elif event.type == pygame.MOUSEBUTTONDOWN and self.rule_message_rect.collidepoint(pygame.mouse.get_pos()):
                    self.rules.show_screen()
                    self.build_game_screen()
  

        

            