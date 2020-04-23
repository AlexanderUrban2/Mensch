import ctypes
import pygame
import Rules

class StartScreen:
    screen_width: float
    screen_height: float

    start_game_message_rect: pygame.rect
    rule_message_rect: pygame.rect

    screen: pygame.display
    font: pygame.font
    run: bool

    rules: Rules

    def __init__(self, background_image: pygame.image, font: pygame.font, rules: Rules):
        self.background_image = background_image
        self.font = font
        self.run = True

        self.init_screen()
        self.build_game_screen()
        self.rules = rules
        self.screen = self.rules.screen


    def init_screen(self):
        user32 = ctypes.windll.user32

        self.screen_width = int(user32.GetSystemMetrics(1) * 0.9)
        self.screen_height = int(user32.GetSystemMetrics(1) * 0.9)


    def build_game_screen(self):
        self.background_image = pygame.transform.smoothscale(self.background_image, (self.screen_width, self.screen_height))
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Mensch Ärgere dich nicht")
        self.screen.blit(self.background_image, (0, 0))
        hello_message = "Hi and welcome to \"Mensch ärgere dich nicht\""
        start_game_message = "Press here to start the game"
        rule_message = "Press here to see the general rules"
        hello_message_font = self.font.render(hello_message, True, (255,0,0))
        start_game_message_font = self.font.render(start_game_message, True, (0,0,0))
        rule_message_font = self.font.render(rule_message, True, (255,255,0))
        self.start_game_message_rect = start_game_message_font.get_rect(topleft=(self.screen_width/2 - self.font.size(start_game_message)[0]/2, self.screen_height/2 - self.font.size(start_game_message)[1]/2))
        self.rule_message_rect = rule_message_font.get_rect(topleft=(self.screen_width/2 - self.font.size(rule_message)[0]/2, self.screen_height/3*2))

        self.screen.blit(hello_message_font, (self.screen_width/2 - self.font.size(hello_message)[0]/2,  self.font.size(hello_message)[1]))
        self.screen.blit(start_game_message_font, (self.screen_width/2 - self.font.size(start_game_message)[0]/2, self.screen_height/2 - self.font.size(start_game_message)[1]/2))
        self.screen.blit(rule_message_font, (self.screen_width/2 - self.font.size(rule_message)[0]/2, self.screen_height/3*2))

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
                elif event.type == pygame.MOUSEBUTTONDOWN and self.rule_message_rect.collidepoint(pygame.mouse.get_pos()):
                    self.rules.show_screen()
                    self.build_game_screen()
                    # add ne py File for rules
                    #scrolling  -> get rules from text file -> load into variable -> make surface from 0,0 -> if mousewheel is rolled -> move surface up/down

        

            