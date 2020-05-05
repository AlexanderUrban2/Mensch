import pygame

class ImagePack:
    
    background_image: pygame.image
    background_image_start_screen: pygame.image
    back_arrow_image: pygame.image
    start_button: pygame.image
    maedn_logo: pygame.image
    ingame_rules_button: pygame.image
    ingame_help_button: pygame.image
    help_image_1: pygame.image
    rules_image_1: pygame.image

    def __init__(self):
        self.background_image = pygame.image.load('images/GameField.jpg')
        self.background_image_start_screen = pygame.image.load('images/StartScreen.jpg')
        self.back_arrow_image = pygame.image.load('images/BackArrow.png')
        self.start_button = pygame.image.load('images/StartButton.png')
        self.maedn_logo = pygame.image.load('images/MaednLogo.png')
        self.ingame_rules_button = pygame.image.load('images/RulesButtonIngame.png')
        self.ingame_help_button = pygame.image.load('images/HelpButtonIngame.png')
        #https://www.pexels.com/photo/white-apple-keyboard-near-white-cup-917463/
        self.help_image_1 = pygame.image.load('images/HelpImage1.png')
        self.rules_image_1 = pygame.image.load('images/RulesImage1.png')
