import ctypes
import pygame


class Rules:
    screen_width: float
    screen_height: float

    back_rect: pygame.rect

    background_image: pygame.image
    back_arrow_image: pygame.image
    back_arrow_rect: pygame.rect

    screen: pygame.display
    text_surface: pygame.Surface
    font: pygame.font
    filename: str
    run: bool
    file_content: str

    def __init__(self, background_image: pygame.image, back_arrow_image: pygame.image, font: pygame.font, filename: str):
        self.background_image = background_image
        self.back_arrow_image = back_arrow_image
        self.font = font
        self.filename = filename
        self.run = True

        self.init_screen()
        self.get_file_content()
        self.build_game_screen()

    def init_screen(self):
        user32 = ctypes.windll.user32

        self.screen_width = int(user32.GetSystemMetrics(1) * 0.9)
        self.screen_height = int(user32.GetSystemMetrics(1) * 0.9)


    def get_file_content(self):
        file = open(self.filename,'r') 
        self.file_content = file.read()
        file.close()
        

    def build_game_screen(self):
        self.background_image = pygame.transform.smoothscale(self.background_image, (self.screen_width, self.screen_height))
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.back_arrow_image = pygame.transform.smoothscale(self.back_arrow_image, (int(self.screen_width * 0.08), int(self.screen_height* 0.08)))

        self.text_surface = pygame.Surface((self.screen_width*0.9, self.screen_height*0.9))  


       
    #Methode um den text auf das surface zu packen. Dabei werden die wörter so geblittet das keine wörter über 2 Zeilen gehen
    def blit_text(self,surface, text, pos, font, color=pygame.Color('black')):
        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
        space = font.size(' ')[0]  # The width of a space.
        max_width, max_height = surface.get_size()
        x, y = pos
        for line in words:
            for word in line:
                word_surface = font.render(word, 0, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]  # Reset the x.
                    y += word_height  # Start on new row.
                surface.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  # Reset the x.
            y += word_height  # Start on new row.
            pygame.display.update()

    def update_screen(self):
        self.run = True
        self.screen.blit(self.background_image, (0,0))
        self.screen.blit(self.back_arrow_image, (0 + self.screen_width* 0.01 ,0 + self.screen_height * 0.005))
        self.back_arrow_rect = self.back_arrow_image.get_rect(topleft=(0 + self.screen_width* 0.01 ,0 + self.screen_height * 0.005))
        self.update_surface(0)


    def update_surface(self, y_coordinate):
        self.text_surface.blit(self.background_image, (-self.screen_width*0.05, -self.screen_height*0.1))
        self.blit_text(self.text_surface,self.file_content, (0,y_coordinate), self.font)
        self.screen.blit(self.text_surface, (0+self.screen_width*0.05, 0+ self.screen_height*0.1))
        pygame.display.update()



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
                        if(y_coordinate != 0):
                            y_coordinate += 100
                    elif event.button == 5:
                        self.update_surface(y_coordinate)
                        # -2400 ist ein hardgecodeter wert.... Noch rausfinden wann Ende ist, bei neuer Textdatei.S
                        if(y_coordinate != -2400):
                            y_coordinate -= 100
                    elif event.button == 1 and self.back_arrow_rect.collidepoint(pygame.mouse.get_pos()):
                        self.run = False
                        
                            
                        
                
            clock.tick(30)
                


