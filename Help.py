import pygame
import Screen
import json


class Help:
    screen_width: float
    screen_height: float

    back_rect: pygame.rect

    background_image: pygame.image
    back_arrow_image: pygame.image
    help_image_1: pygame.image
    back_arrow_rect: pygame.rect
    back_message_rect: pygame.rect

    screen: pygame.display
    text_surface: pygame.Surface
    font: pygame.font
    filename: str
    run: bool
    file_content: str

    screen_class = Screen

    text_color: (int, int, int)

    """
    desc:
        - initialize the help window
    param:
        - screen_class - object reference from class Screen
        - font - default pygame font
        - filename - string 
    return:
        - none
    """
    def __init__(self, screen_class: Screen,  font: pygame.font, filename: str):
        self.init_images()

        self.font = font
        self.filename = filename
        self.run = True

        self.screen_class = screen_class

        self.screen = self.screen_class.screen
        self.screen_width = self.screen_class.screen_width
        self.screen_height = self.screen_class.screen_height

        self.get_file_content()
        self.build_game_screen()

        with open('text_color_pack.txt') as json_file:
            data = json.load(json_file)
        self.text_color = data["rules_help_color"]

        self.counter = 0
        self.surface_height = 0

    """
    desc: 
        - initalize all images for help screen
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
        self.help_image_1 = pygame.image.load(data["help_image_1"])

    """
    desc: 
        - get help text from Help.txt file
    param:
        - none
    return:
        - none
    """
    def get_file_content(self):
        file = open(self.filename, 'r')
        self.file_content = file.read().upper()
        file.close()

    """
    desc: 
        - scale all images, describe screen, create text surface
    param:
        - none
    return:
        - none
    """
    def build_game_screen(self):
        self.background_image = pygame.transform.smoothscale(self.background_image, (self.screen_width, self.screen_height))
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.back_arrow_image = pygame.transform.smoothscale(self.back_arrow_image, (int(self.screen_width * 0.08), int(self.screen_height*0.08)))
        self.help_image_1 = pygame.transform.smoothscale(self.help_image_1, (int(self.screen_width * 0.45), int(self.screen_height*0.45)))

        self.text_surface = pygame.Surface((self.screen_width*0.5, self.screen_height))  

    """
    desc: 
        - blit text on surface, newline if text doesnt fit in current line
        - from https://stackoverflow.com/questions/42014195/rendering-text-with-multiple-lines-in-pygame/42015712
    param:
        - surface - default pygame surface
        - text - string 
        - pos - tupel
        - font - default pygame font
    return:
        - none
    """
    def blit_text(self, surface, text, pos, font):
        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
        space = font.size(' ')[0]  # The width of a space.
        max_width, max_height = surface.get_size()
        x, y = pos
        for line in words:
            for word in line:
                word_surface = font.render(word, 0, self.text_color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]  # Reset the x.
                    y += word_height  # Start on new row.
                surface.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  # Reset the x.
            y += word_height  # Start on new row.
            pygame.display.update()
        if self.counter == 0:
            self.surface_height = y
            self.counter = 1    

    """
    desc: 
        - update the whole screen
    param:
        - none
    return:
        - none
    """
    def update_screen(self):
        self.run = True
        back_message = "Back"
        back_message_font = self.font.render(back_message, True, self.text_color)

        self.screen.blit(self.background_image, (0, 0))
        self.screen.blit(self.back_arrow_image, (self.screen_width * 0.01, self.screen_height * 0.005))
        self.screen.blit(self.help_image_1, (self.screen_width * 0.01, self.screen_height * 0.1))
        self.screen.blit(back_message_font,  (self.screen_width * 0.1, self.screen_height * 0.02))
        self.back_arrow_rect = self.back_arrow_image.get_rect(topleft=(self.screen_width * 0.01, self.screen_height * 0.005))
        self.back_message_rect = back_message_font.get_rect(topleft=(self.screen_width * 0.1, self.screen_height * 0.02))

        # adjust rectangle, so that its over the text and the space between text and arrow
        x_before_moving = self.back_message_rect.x 
        self.back_message_rect.x = self.back_arrow_rect.x + self.back_arrow_rect.w
        x_after_moving = self.back_message_rect.x
        self.back_message_rect.w += x_before_moving - x_after_moving 
        self.update_surface(0)

    """
    desc: 
        - update text surface
    param:
        - y_coordinate: int
    return:
        - none
    """
    def update_surface(self, y_coordinate):
        self.text_surface.blit(self.background_image, (-self.screen_width*0.5, 0))
        self.blit_text(self.text_surface, self.file_content, (0, y_coordinate), self.font)
        self.screen.blit(self.text_surface, (self.screen_width*0.5, 0))
        pygame.display.update()

    """
    desc: 
        - get click events and call functions
    param:
        - none
    return:
        - none
    """
    def show_screen(self):
        self.update_screen()

        y_coordinate = 0
        clock = pygame.time.Clock()
        while self.run:           
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        self.update_surface(y_coordinate)
                        if y_coordinate != 0:
                            y_coordinate += 100
                    elif event.button == 5:
                        self.update_surface(y_coordinate)
                        if y_coordinate >= -self.surface_height + self.text_surface.get_size()[1]:
                            y_coordinate -= 100
                    elif event.button == 1 and (self.back_arrow_rect.collidepoint(pygame.mouse.get_pos()) or self.back_message_rect.collidepoint(pygame.mouse.get_pos())):
                        self.run = False

            clock.tick(10)
