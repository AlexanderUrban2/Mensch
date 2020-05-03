import ctypes
import pygame
import Screen
import Rules


class StartScreen:
    screen_width: float
    screen_height: float

    start_game_message_rect: pygame.rect
    rule_message_rect: pygame.rect
    start_game_button_rect: pygame.rect
    hidden_rect: pygame.rect

    screen: pygame.display
    font: pygame.font
    run: bool

    background_image: pygame.image
    start_button: pygame.image
    maedn_logo: pygame.image

    screen_class: Screen
    rules: Rules

    def __init__(self, screen_class: Screen, rules: Rules, background_image: pygame.image,start_button: pygame.image, maedn_logo: pygame.image, font: pygame.font):
        self.background_image = background_image
        self.start_button = start_button
        self.maedn_logo = maedn_logo
        self.font = font
        self.run = True

        self.rules = rules

        self.screen_class = screen_class
        self.screen = self.screen_class.screen
        self.screen_width = self.screen_class.screen_width
        self.screen_height = self.screen_class.screen_height

      
        self.build_game_screen()
        

    def build_game_screen(self):
        self.background_image = pygame.transform.smoothscale(self.background_image, (self.screen_width, self.screen_height))
        self.maedn_logo = pygame.transform.smoothscale(self.maedn_logo, (int(self.screen_width *0.03), int(self.screen_height*0.03)))
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Mensch Ärgere dich nicht")
        self.screen.blit(self.background_image, (0, 0))
        hello_message = "Hi and welcome to \"Mensch ärgere dich nicht\""
        start_game_message = "Play"
        # Man kann nicht mit nem fcking s aufhören sonst is es nimmer in der mitte 
        rule_message = "RuleS"
        hello_message_font = self.font.render(hello_message, True, (0,0,0))
        start_game_message_font = self.font.render(start_game_message, True, (0,0,0))
        rule_message_font = self.font.render(rule_message, True, (0,0,0))
        self.start_game_message_rect = start_game_message_font.get_rect(topleft=(self.screen_width/2 - self.font.size(start_game_message)[0]/2, self.screen_height/2 + self.start_button.get_rect().size[1]/2))
        self.rule_message_rect = rule_message_font.get_rect(topleft=(self.screen_width/2 - self.font.size(rule_message)[0]/2, self.screen_height/3*2))
        self.start_game_button_rect = self.start_button.get_rect(topleft=(self.screen_width/2 - self.start_button.get_rect().size[0]/2, self.screen_height/2 - self.start_button.get_rect().size[1]/2))


        self.screen.blit(hello_message_font, (self.screen_width/2 - self.font.size(hello_message)[0]/2,  self.font.size(hello_message)[1]))
        self.screen.blit(self.start_button, (self.screen_width/2 - self.start_button.get_rect().size[0]/2, self.screen_height/2 - self.start_button.get_rect().size[1]/2))
        self.screen.blit(start_game_message_font, (self.screen_width/2 - self.font.size(start_game_message)[0]/2, self.screen_height/2 + self.start_button.get_rect().size[1]/2))
        self.screen.blit(rule_message_font, (self.screen_width/2 - self.font.size(rule_message)[0]/2, self.screen_height/3*2))
        

        self.hidden_rect = self.start_button.get_rect(topleft=(0, self.screen_height - self.maedn_logo.get_rect().size[0]))
        self.screen.blit(self.maedn_logo, (0, self.screen_height - self.maedn_logo.get_rect().size[0]))

        pygame.display.update()
        

    def start_game(self):
        while self.run:           
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    #Mousevent wenn spiel starten -> player anzahl auswählbar
                    pass
                elif event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and self.start_game_message_rect.collidepoint(pygame.mouse.get_pos()):
                    self.run = False
                elif event.type == pygame.MOUSEBUTTONDOWN and self.start_game_button_rect.collidepoint(pygame.mouse.get_pos()):
                    self.run = False
                elif event.type == pygame.MOUSEBUTTONDOWN and self.hidden_rect.collidepoint(pygame.mouse.get_pos()):
                    self.run = False
                    #Hidden Kecks Quest einbauen
                elif event.type == pygame.MOUSEBUTTONDOWN and self.rule_message_rect.collidepoint(pygame.mouse.get_pos()):
                    self.rules.show_screen()
                    self.build_game_screen()
  

        

            