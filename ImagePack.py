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
        self.background_image = pygame.image.load('GameField.jpg')
        self.background_image_start_screen = pygame.image.load('StartScreen.jpg')
        self.back_arrow_image = pygame.image.load('BackArrow.png')
        self.start_button = pygame.image.load('StartButton.png')
        self.maedn_logo = pygame.image.load('MaednLogo.png')
        self.ingame_rules_button = pygame.image.load('RulesButtonIngame.png')
        self.ingame_help_button = pygame.image.load('HelpButtonIngame.png')
        #https://www.pexels.com/photo/white-apple-keyboard-near-white-cup-917463/
        self.help_image_1 = pygame.image.load('HelpImage1.png')
        self.rules_image_1 = pygame.image.load('RulesImage1.png')
