import pygame
import Screen
import Rules
import json
import ThemePack


class StartScreen:
    screen_width: float
    screen_height: float

    player_counter: int
    theme_counter: int

    start_game_message_rect: pygame.rect
    rule_message_rect: pygame.rect
    start_game_button_rect: pygame.rect
    hidden_rect: pygame.rect
    player_arrow_up_rect: pygame.rect
    player_arrow_down_rect: pygame.rect
    theme_arrow_right_rect: pygame.rect
    theme_arrow_left_rect: pygame.rect
    player_counter_rect: pygame.rect
    theme_counter_rect: pygame.rect

    screen: pygame.display
    font: pygame.font
    run: bool

    screen_size_multiplier: int

    background_image: pygame.image
    start_button: pygame.image
    maedn_logo: pygame.image
    player_arrow_up: pygame.image
    player_arrow_down: pygame.image
    theme_arrow_left: pygame.image
    theme_arrow_right: pygame.image
    current_gamefield: pygame.image
    old_gamefield: pygame.image

    screen_class: Screen
    rules: Rules
    theme_pack: ThemePack

    data: json

    text_color: (int, int, int)

    theme_list: ()

    """
    desc: 
        - initialize the rules window
    param:
        - screen_class - object reference from class Screen
        - font: default pygame font
        - theme_list: string
    return:
        - none
    """
    def __init__(self, screen_class: Screen, font: pygame.font, theme_list: ()):
        # theme_list includes all available themes as strings
        self.theme_list = theme_list
        self.theme_pack = ThemePack.ThemePack(self.theme_list[0])
        self.init_images()

        self.font = font
        self.run = True

        with open('text_color_pack.txt') as json_file:
            data = json.load(json_file)
        self.text_color = data["start_screen_color"]

        self.screen_class = screen_class
        self.screen = self.screen_class.screen
        self.screen_width = self.screen_class.screen_width
        self.screen_height = self.screen_class.screen_height
        self.screen_size_multiplier = self.screen_height//11

        self.player_counter = 1
        self.theme_counter = 1

        self.build_game_screen()

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
            self.data = json.load(json_file)
        self.background_image = pygame.image.load(self.data["background_image_start_screen"])
        self.maedn_logo = pygame.image.load(self.data["maedn_logo"])
        self.player_arrow_down = pygame.image.load(self.data["player_arrow_down"])
        self.player_arrow_up = pygame.image.load(self.data["player_arrow_up"])
        self.start_button = pygame.image.load(self.data["start_button"])
        self.theme_arrow_right = pygame.image.load(self.data["theme_arrow_right"])
        self.theme_arrow_left = pygame.image.load(self.data["theme_arrow_left"])
        self.current_gamefield = pygame.image.load(self.data["theme_image"])
        
    """
    desc: 
        - scale all images, describe screen, describe text, blit images, blit text
    param:
        - none
    return:
        - none
    """
    def build_game_screen(self):
        self.background_image = pygame.transform.smoothscale(self.background_image, (self.screen_width, self.screen_height))
        self.maedn_logo = pygame.transform.smoothscale(self.maedn_logo, (int(self.screen_width * 0.03), int(self.screen_height*0.03)))
        self.player_arrow_up = pygame.transform.smoothscale(self.player_arrow_up, (int(self.screen_width*0.05), int(self.screen_height*0.05)))
        self.player_arrow_down = pygame.transform.smoothscale(self.player_arrow_down, (int(self.screen_width*0.05), int(self.screen_height*0.05)))
        self.theme_arrow_right = pygame.transform.smoothscale(self.theme_arrow_right, (int(self.screen_width * 0.05), int(self.screen_height * 0.05)))
        self.theme_arrow_left = pygame.transform.smoothscale(self.theme_arrow_left, (int(self.screen_width * 0.05), int(self.screen_height * 0.05)))
        self.current_gamefield = pygame.transform.smoothscale(self.current_gamefield, (self.screen_size_multiplier*3, self.screen_size_multiplier*3))

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Mensch Ärgere dich nicht")
        self.screen.blit(self.background_image, (0, 0))
        hello_message_str = "Hi and welcome to \"Mensch ärgere dich nicht\""
        start_game_message_str = "Play"
        rule_message_str = "RuleS"
        player_text_str = "Number of PlayerS:"
        theme_text_str = "Theme"
        hello_message = self.font.render(hello_message_str, True, self.text_color)
        start_game_message = self.font.render(start_game_message_str, True, self.text_color)
        rule_message = self.font.render(rule_message_str, True, self.text_color)
        player_text = self.font.render(player_text_str, True, self.text_color)
        theme_text = self.font.render(theme_text_str, True, self.text_color)
        player_counter = self.font.render(str(self.player_counter), True, self.text_color)
        theme_counter = self.font.render(str(self.theme_counter), True, self.text_color)
        player_counter_max = self.font.render("4", True, self.text_color)
        theme_counter_max = self.font.render("4", True, self.text_color)

        # Hi message
        self.screen.blit(hello_message, (self.screen_width/2 - self.font.size(hello_message_str)[0]/2,  0))

        # arrow left
        self.theme_arrow_left_rect = self.theme_arrow_left.get_rect(topleft=(self.screen_size_multiplier * 3 - self.theme_arrow_left.get_rect().size[0], self.screen_size_multiplier * 3 - self.player_arrow_up.get_rect().size[1]))
        self.screen.blit(self.theme_arrow_left, (self.screen_size_multiplier * 3 - self.theme_arrow_left.get_rect().size[0], self.screen_size_multiplier * 3 - self.theme_arrow_left.get_rect().size[1]))

        # arrow right
        self.theme_arrow_right_rect = self.theme_arrow_right.get_rect(topleft=(self.screen_size_multiplier * 8, self.screen_size_multiplier * 3 - self.theme_arrow_right.get_rect().size[1]))
        self.screen.blit(self.theme_arrow_right, (self.screen_size_multiplier * 8, self.screen_size_multiplier * 3 - self.theme_arrow_right.get_rect().size[1]))

        # gamefield
        gamefield_image = pygame.transform.smoothscale(self.current_gamefield, (self.screen_size_multiplier*3, self.screen_size_multiplier*3))
        self.screen.blit(gamefield_image, (self.screen_width/2 - gamefield_image.get_rect().size[0]/2, self.screen_size_multiplier*3 - gamefield_image.get_rect().size[1]/2))

        # Theme Text
        self.theme_counter_rect = theme_counter_max.get_rect(topleft=(self.screen_width/2 + self.font.size(theme_text_str + " ")[0]/2, self.screen_size_multiplier - 0.5*self.font.size(theme_text_str)[1]))
        self.screen.blit(theme_text, (self.screen_width/2 - self.font.size(theme_text_str + " ")[0]/2, self.screen_size_multiplier - 0.5*self.font.size(theme_text_str)[1]))
        self.screen.blit(theme_counter, (self.screen_width/2 + self.font.size(theme_text_str + " ")[0]/2, self.screen_size_multiplier - 0.5*self.font.size(theme_text_str)[1]))

        # Play button
        self.start_game_button_rect = self.start_button.get_rect(topleft=(self.screen_width/2 - self.start_button.get_rect().size[0]/2, self.screen_height/2 - self.start_button.get_rect().size[1]/2))
        self.screen.blit(self.start_button, (self.screen_width/2 - self.start_button.get_rect().size[0]/2, self.screen_height/2 - self.start_button.get_rect().size[1]/2))

        # Start message
        self.start_game_message_rect = start_game_message.get_rect(topleft=(self.screen_width/2 - self.font.size(start_game_message_str)[0]/2, self.screen_height/2 + self.start_button.get_rect().size[1]/2))
        self.screen.blit(start_game_message, (self.screen_width/2 - self.font.size(start_game_message_str)[0]/2, self.screen_height/2 + self.start_button.get_rect().size[1]/2))
        
        # Number of Players text
        self.player_counter_rect = player_counter_max.get_rect(topleft=(self.screen_width*0.55, self.screen_size_multiplier*8 - 0.5*self.font.size(player_text_str)[1]))
        self.screen.blit(player_text, (self.screen_width/2 - self.font.size(player_text_str)[0], self.screen_size_multiplier*8 - 0.5*self.font.size(player_text_str)[1]))
        self.screen.blit(player_counter, (self.screen_width*0.55, self.screen_size_multiplier*8 - 0.5*self.font.size(player_text_str)[1]))

        # arrow up
        self.player_arrow_up_rect = self.player_arrow_up.get_rect(topleft=(self.screen_width * 0.65, self.screen_size_multiplier*8 - self.player_arrow_up.get_rect().size[1] - 0.005 *self.screen_height))
        self.screen.blit(self.player_arrow_up, (self.screen_width * 0.65, self.screen_size_multiplier*8 - self.player_arrow_up.get_rect().size[1] - 0.005 * self.screen_height))
       
        # arrow down
        self.player_arrow_down_rect = self.player_arrow_down.get_rect(topleft=(self.screen_width * 0.65, self.screen_size_multiplier*8 + 0.005 * self.screen_height))
        self.screen.blit(self.player_arrow_down, (self.screen_width * 0.65, self.screen_size_multiplier*8 + 0.005 *self.screen_height))
       
        # rule message
        self.rule_message_rect = rule_message.get_rect(topleft=(self.screen_width/2 - self.font.size(rule_message_str)[0]/2, self.screen_size_multiplier*9))
        self.screen.blit(rule_message, (self.screen_width/2 - self.font.size(rule_message_str)[0]/2,  self.screen_size_multiplier*9))

        
        # hidden quest
        self.hidden_rect = self.maedn_logo.get_rect(topleft=(0, self.screen_height - self.maedn_logo.get_rect().size[0]))
        self.screen.blit(self.maedn_logo, (0, self.screen_height - self.maedn_logo.get_rect().size[0]))

        pygame.display.update()

    """
    desc: 
        - blit current player counter on change
    param:
        - none
    return:
        - none
    """
    def update_player_counter_on_screen(self):
        self.screen.blit(self.background_image, (0, 0))
        self.screen.blit(self.font.render(str(self.player_counter), True, self.text_color), (self.screen_width*0.55, self.screen_size_multiplier*8 - 0.5*self.font.size("Number of PlayerS:")[1]))
        pygame.display.update(self.player_counter_rect)

    """
    desc: 
        - update gamefield theme image
    param:
        - option - int
    return:
        - none
    """
    def update_theme(self, option):
        self.screen.blit(self.background_image, (0, 0))
        self.screen.blit(self.font.render(str(self.theme_counter), True, self.text_color), (self.screen_width/2 + self.font.size("Theme ")[0]/2, self.screen_size_multiplier - 0.5*self.font.size("Theme ")[1]))
        pygame.display.update(self.theme_counter_rect)

        self.gamefield_animation(option)

    """
    desc: 
        - make gamefield theme animation
    param:
        - option - int
    return:
        - none
    """
    def gamefield_animation(self, option):

        delay = 75

        current_time = pygame.time.get_ticks()
        change_time = current_time + delay
        animation = True

        self.old_gamefield = pygame.image.load(self.data["theme_image"])

        # update ThemePack
        self.theme_pack = ThemePack.ThemePack(self.theme_list[self.theme_counter-1])
        # update the rules screen

        with open('image_pack.txt') as json_file:
            self.data = json.load(json_file)

        # neues gamefield rein (slided rein)
        self.current_gamefield = pygame.transform.smoothscale(pygame.image.load(self.data["theme_image"]), (self.screen_size_multiplier*3, self.screen_size_multiplier*3))

        new_gamefield_width = self.current_gamefield.get_rect().size[0]

        new_gamefield_x_coord_end = self.screen_width/2 - self.current_gamefield.get_rect().size[0]/2

        if option == 0:
            new_gamefield_x_coord = -new_gamefield_width
        else:
            new_gamefield_x_coord = self.screen_width + new_gamefield_width
        new_gamefield_y_coord = self.screen_size_multiplier*3 - self.current_gamefield.get_rect().size[1]/2
        new_gamefield_rect = self.current_gamefield.get_rect(topleft=(new_gamefield_x_coord, new_gamefield_y_coord))
        new_gamefield_rect.w = 100 + new_gamefield_width

        #altes gamefield raus (slided raus)
        old_gamefield_image = pygame.transform.smoothscale(self.old_gamefield, (self.screen_size_multiplier*3, self.screen_size_multiplier*3))

        old_gamefield_width = old_gamefield_image.get_rect().size[0]

        old_gamefield_x_coord = self.screen_width/2 - old_gamefield_image.get_rect().size[0]/2
        old_gamefield_y_coord = self.screen_size_multiplier*3 - old_gamefield_image.get_rect().size[1]/2
        old_gamefield_rect = old_gamefield_image.get_rect(topleft=(old_gamefield_x_coord, old_gamefield_y_coord))
        old_gamefield_rect.w = 100 + old_gamefield_width

        while animation:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            current_time = pygame.time.get_ticks()
            if current_time >= change_time:
                change_time = current_time + delay
                if new_gamefield_x_coord + 100 >= new_gamefield_x_coord_end and option == 0:
                    self.screen.blit(self.theme_arrow_right, (self.screen_size_multiplier * 8, self.screen_size_multiplier * 3 - self.theme_arrow_right.get_rect().size[1]))
                    self.screen.blit(self.theme_arrow_left, (self.screen_size_multiplier * 3 - self.theme_arrow_left.get_rect().size[0], self.screen_size_multiplier * 3 - self.theme_arrow_left.get_rect().size[1]))
                    self.screen.blit(self.current_gamefield, (new_gamefield_x_coord_end, new_gamefield_y_coord))
                    self.screen.blit(old_gamefield_image, (self.screen_width, old_gamefield_y_coord))
                    pygame.display.update(new_gamefield_rect)
                    pygame.display.update(old_gamefield_rect)
                    animation = False
                elif new_gamefield_x_coord - 100 <= new_gamefield_x_coord_end and option == 1:
                    new_gamefield_rect = self.current_gamefield.get_rect(topleft=(new_gamefield_x_coord-100, new_gamefield_y_coord))
                    new_gamefield_rect.w = 100 + new_gamefield_width
                    old_gamefield_rect = old_gamefield_image.get_rect(topleft=(old_gamefield_x_coord-100, old_gamefield_y_coord))
                    old_gamefield_rect.w = 100 + old_gamefield_width
                    self.screen.blit(self.theme_arrow_right, (self.screen_size_multiplier * 8, self.screen_size_multiplier * 3 - self.theme_arrow_right.get_rect().size[1]))
                    self.screen.blit(self.theme_arrow_left, (self.screen_size_multiplier * 3 - self.theme_arrow_left.get_rect().size[0], self.screen_size_multiplier * 3 - self.theme_arrow_left.get_rect().size[1]))
                    self.screen.blit(self.current_gamefield, (new_gamefield_x_coord_end, new_gamefield_y_coord))
                    self.screen.blit(old_gamefield_image, (-old_gamefield_width, old_gamefield_y_coord))
                    pygame.display.update(new_gamefield_rect)
                    pygame.display.update(old_gamefield_rect)
                    animation = False
                else:
                    if option == 0:
                        new_gamefield_x_coord += 100
                        old_gamefield_x_coord += 100
                        self.screen.blit(self.theme_arrow_right, (self.screen_size_multiplier * 8, self.screen_size_multiplier * 3 - self.theme_arrow_right.get_rect().size[1]))
                        self.screen.blit(self.theme_arrow_left, (self.screen_size_multiplier * 3 - self.theme_arrow_left.get_rect().size[0], self.screen_size_multiplier * 3 - self.theme_arrow_left.get_rect().size[1]))
                        self.screen.blit(self.current_gamefield, (new_gamefield_x_coord, new_gamefield_y_coord))
                        self.screen.blit(old_gamefield_image, (old_gamefield_x_coord, old_gamefield_y_coord))

                        pygame.display.update(new_gamefield_rect)
                        pygame.display.update(old_gamefield_rect)

                        self.screen.blit(self.background_image, (0, 0))

                        new_gamefield_rect = self.current_gamefield.get_rect(topleft=(new_gamefield_x_coord, new_gamefield_y_coord))
                        new_gamefield_rect.w = 100 + new_gamefield_width
                        old_gamefield_rect = old_gamefield_image.get_rect(topleft=(old_gamefield_x_coord, old_gamefield_y_coord))
                        old_gamefield_rect.w = 100 + old_gamefield_width
                    else:
                        new_gamefield_x_coord -= 100
                        old_gamefield_x_coord -= 100

                        new_gamefield_rect = self.current_gamefield.get_rect(topleft=(new_gamefield_x_coord, new_gamefield_y_coord))
                        new_gamefield_rect.w = 100 + new_gamefield_width
                        old_gamefield_rect = old_gamefield_image.get_rect(topleft=(old_gamefield_x_coord, old_gamefield_y_coord))
                        old_gamefield_rect.w = 100 + old_gamefield_width

                        self.screen.blit(self.theme_arrow_right, (self.screen_size_multiplier * 8, self.screen_size_multiplier * 3 - self.theme_arrow_right.get_rect().size[1]))
                        self.screen.blit(self.theme_arrow_left, (self.screen_size_multiplier * 3 - self.theme_arrow_left.get_rect().size[0], self.screen_size_multiplier * 3 - self.theme_arrow_left.get_rect().size[1]))
                        self.screen.blit(self.current_gamefield, (new_gamefield_x_coord, new_gamefield_y_coord))
                        self.screen.blit(old_gamefield_image, (old_gamefield_x_coord, old_gamefield_y_coord))

                        pygame.display.update(new_gamefield_rect)
                        pygame.display.update(old_gamefield_rect)

                        self.screen.blit(self.background_image, (0, 0))

    """
    desc: 
        - start game and call functions on click
    param:
        - none
    return:
        - self.player_counter - int
    """
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
                    if self.player_counter + 1 > 4:
                        self.player_counter = 1
                    else:
                        self.player_counter += 1
                    self.update_player_counter_on_screen()
                elif event.type == pygame.MOUSEBUTTONDOWN and self.player_arrow_down_rect.collidepoint(pygame.mouse.get_pos()):
                    if self.player_counter - 1 < 1:
                        self.player_counter = 4
                    else:
                        self.player_counter -= 1
                    self.update_player_counter_on_screen()
                elif event.type == pygame.MOUSEBUTTONDOWN and self.theme_arrow_left_rect.collidepoint(pygame.mouse.get_pos()):
                    if self.theme_counter - 1 < 1:
                        self.theme_counter = len(self.theme_list)
                    else:
                        self.theme_counter -= 1
                    self.update_theme(0)
                elif event.type == pygame.MOUSEBUTTONDOWN and self.theme_arrow_right_rect.collidepoint(pygame.mouse.get_pos()):
                    if self.theme_counter + 1 > len(self.theme_list):
                        self.theme_counter = 1
                    else:
                        self.theme_counter += 1
                    self.update_theme(1)
                elif event.type == pygame.MOUSEBUTTONDOWN and self.hidden_rect.collidepoint(pygame.mouse.get_pos()):
                    self.run = False
                    #Hidden Kecks Quest einbauen
                elif event.type == pygame.MOUSEBUTTONDOWN and self.rule_message_rect.collidepoint(pygame.mouse.get_pos()):
                    # initialize rules here, in order to guarantee the use of the correct images
                    self.rules = Rules.Rules(self.screen_class, self.font, "Rule.txt")
                    self.rules.show_screen()
                    self.build_game_screen()

                #Check only left klick!!!!!!
