import pygame
import json
import Screen

class HiddenQuest:
    screen_width: float
    screen_height: float

    back_rect: pygame.rect

    background_image: pygame.image
    back_arrow_image: pygame.image
    cookie_monster: pygame.image

    back_arrow_rect: pygame.rect
    back_message_rect: pygame.rect

    screen: pygame.display 
    font: pygame.font
    run: bool

    screen_class = Screen

    text_color: (int, int, int)

    """
    desc: 
        - initialize the rules window
    param:
        - screen_class - object reference from class Screen
        - font: default pygame font
        - filename: string
    return:
        - none
    """
    def __init__(self, screen_class: Screen,  font: pygame.font):
        self.init_images()

        self.font = font
        self.run = True

        with open('text_color_pack.txt') as json_file:
            data = json.load(json_file)
        self.text_color = data["rules_help_color"]

        self.screen_class = screen_class

        self.screen = self.screen_class.screen
        self.screen_width = self.screen_class.screen_width
        self.screen_height = self.screen_class.screen_height

        self.scale_images()
        self.build_screen()

    """
    desc: 
        - initialize all images for rules screen
    param:
        - none
    return:
        - none
    """
    def init_images(self):
        with open('image_pack.txt') as json_file:
            data = json.load(json_file)
        self.background_image = pygame.image.load(data["rules_help_background"])
        self.back_arrow_image = pygame.image.load(data["back_arrow_image"])
        self.cookie_monster = pygame.image.load(data["cookie_monster"])

    """
    desc: 
        - scale all images
    param:
        - none
    return:
        - none
    """
    def scale_images(self):
        self.background_image = pygame.transform.smoothscale(self.background_image, (self.screen_width, self.screen_height))
        self.back_arrow_image = pygame.transform.smoothscale(self.back_arrow_image, (int(self.screen_width * 0.08), int(self.screen_height * 0.08)))
        self.cookie_monster = pygame.transform.smoothscale(self.cookie_monster, (int(self.screen_width * 0.8), int(self.screen_height * 0.8)))

    """
    desc: 
        - build screen and blit images on it, adjust back rectangle
    param:
        - none
    return:
        - none
    """
    def build_screen(self):
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        
        back_message = "Back"
        back_message_font = self.font.render(back_message, True, self.text_color)

        self.screen.blit(self.background_image, (0, 0))
        self.screen.blit(self.back_arrow_image, (self.screen_width * 0.01, 0 + self.screen_height * 0.005))
        self.screen.blit(back_message_font,  (self.screen_width * 0.1, 0 + self.screen_height * 0.02))
        self.screen.blit(self.cookie_monster, (self.screen_width/2 - self.cookie_monster.get_rect().size[0]/2, self.screen_height/2 - self.cookie_monster.get_rect().size[1]/2))
        self.back_arrow_rect = self.back_arrow_image.get_rect(topleft=(self.screen_width * 0.01, self.screen_height * 0.005))
        self.back_message_rect = back_message_font.get_rect(topleft=(self.screen_width * 0.1, self.screen_height * 0.02))

        # adjust rectangle, so that its over the text and the space between text and arrow
        x_before_moving = self.back_message_rect.x 
        self.back_message_rect.x = self.back_arrow_rect.x + self.back_arrow_rect.w
        x_after_moving = self.back_message_rect.x
        self.back_message_rect.w += x_before_moving - x_after_moving 
        pygame.display.update()

    def show_screen(self):

        while self.run:           
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and (self.back_arrow_rect.collidepoint(pygame.mouse.get_pos()) or self.back_message_rect.collidepoint(pygame.mouse.get_pos())):
                        self.run = False

  
