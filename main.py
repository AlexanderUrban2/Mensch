import pygame
import random
import time

import ctypes

# pylint: disable=no-member
pygame.init()
pygame.font.init() 



#methodes
def init_dice(dice):
    for i in range(0,6):
        dice.append(pygame.image.load('Dice' + str(i+1) + '.png'))
        dice[i] = pygame.transform.smoothscale(dice[i], (int(screen_width/11), int(screen_height/11)))
    return dice

def get_gamefield_distance_to_border():
    return (screen_width*1.04827 - screen_width)/2  

def get_gamefield_height():
    return screen_width - 2 * gamefield_distance_to_border 


def roll_dice(dice):
    for i in range (0,10):
        number = random.randint(0,5)
        image_width = dice[number].get_size()[0]
        image_heigth = dice[number].get_size()[1]
        pygame.display.update()
        screen.blit(background, (0,0))
        screen.blit(dice[number], (int((screen_width-image_width)/2),int((screen_height-image_heigth)/2)))
        time.sleep(0.005)
    return number
        

def set_figures_in_all_fields():
    width_multiplier = gamefield_width/11
    height_multiplier = gamefield_height/11
    for i in range(0,11):
        for m in range(0,11):
            text_width, text_heigth = myfont.size("x")
            screen.blit(myfont.render('x', False, (0, 0, 0)), (i*width_multiplier + gamefield_distance_to_border+text_width ,m*height_multiplier + gamefield_distance_to_border))
            print(str(i*width_multiplier) + '//' + str(m*height_multiplier))
    pygame.display.update()
    



    

def start_game(keys):

    run = True
    text_width, text_heigth = myfont.size("Press X to start the Game")
    screen.blit(myfont.render('Press Space to roll the Dice', False, (0, 0, 0)), (int((screen_width-text_width)/2),int(screen_height*0.9)))
    figure.set_figures()
    pygame.display.update()
    while run:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    number = roll_dice(dice)
                    if number+1 == 6:
                        figure.set_figure_out_of_house(0)
                        screen.blit(dice[number], (int((screen_width-dice[number].get_size()[0])/2),int((screen_height-dice[number].get_size()[1])/2)))
                        text_width, text_heigth = myfont.size("You got out of the house! Roll the Dice again!")
                        screen.blit(myfont.render('You got out of the house! Roll the Dice again!', False, (0, 0, 0)), (int((screen_width-text_width)/2),int(screen_height*0.9)))
                        pygame.display.update()
                    else:
                        figure.set_figures()
                        text_width, text_heigth = myfont.size("U can Move x Steps Now")
                        screen.blit(myfont.render('U can Move ' + str(number +1) + 'Steps now', False, (0, 0, 0)), (int((screen_width-text_width)/2),int(screen_height*0.9)))
                        pygame.display.update()
                    

        


#class

class Figure:

    def __init__(self):
        self.figure_width = []
        self.figure_width_start = []
        self.figure_height = []
        self.figure_height_start = []
        self.house_width = []
        self.house_height = []


    def init_figure(self):
        width_multiplier = gamefield_width/11
        height_multiplier = gamefield_height/11
        text_width, text_heigth = myfont.size("x")

        start_width = [0, 0, 1, 1, 9, 9, 10, 10, 0, 0, 1, 1, 9, 9, 10, 10]
        start_height = [0, 1, 0, 1, 0, 1, 0, 1, 9, 10, 9, 10, 9, 10, 9, 10]
        start_width_house = [0, 4, 6, 10]
        start_height_house = [4, 10, 0, 6]

        for i in range(0,16):
            self.figure_width.append(start_width[i]*width_multiplier + gamefield_distance_to_border+text_width)
            self.figure_width_start.append(start_width[i]*width_multiplier + gamefield_distance_to_border+text_width)
            self.figure_height.append(start_height[i]*height_multiplier + gamefield_distance_to_border)
            self.figure_height_start.append(start_height[i]*height_multiplier + gamefield_distance_to_border)

        for i in range(0,4):
            self.house_width.append(start_width_house[i]*width_multiplier + gamefield_distance_to_border+text_width)
            self.house_height.append(start_height_house[i]*height_multiplier + gamefield_distance_to_border)

    def set_figures(self):
        for i in range(0,16):
            screen.blit(myfont.render('x', False, (0, 0, 0)), (self.figure_width[i] ,self.figure_height[i]))
            pygame.display.update()

    def set_figure_out_of_house(self,player):
        for i in range(0,4):
            if self.figure_width[i + 4* player] == self.figure_width_start[i + 4* player] and self.figure_width[i + 4* player] == self.figure_width_start[i + 4* player]:
                self.figure_width[i + 4* player] = self.house_width[player]
                self.figure_height[i + 4* player] = self.house_height[player]
                screen.fill( (0,0,0) )
                screen.blit(background, (0,0))
                figure.set_figures()
                break
                



#main
user32 = ctypes.windll.user32

screen_width = int(user32.GetSystemMetrics(1)*0.9)
screen_height = int(user32.GetSystemMetrics(1)*0.9)

gamefield_distance_to_border = get_gamefield_distance_to_border()
gamefield_width = get_gamefield_height()
gamefield_height = get_gamefield_height()
print(gamefield_distance_to_border)
print(gamefield_width)
print(screen_width)

background = pygame.image.load('GameField.jpg')
background = pygame.transform.smoothscale(background, (screen_width, screen_height))
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Mensch ärgere dich nicht")
screen.fill((0,0,0))


myfont = pygame.font.SysFont('Comic Sans MS', 30)
text_width, text_heigth = myfont.size("Press X to start the Game")
screen.blit(myfont.render('Press X to start the Game', False, (255, 0, 0)), (int((screen_width-text_width)/2),int(screen_height*0.5)))

dice = []
dice = init_dice(dice)

figure = Figure()
figure.init_figure()

run = True
while run:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    

    if keys[pygame.K_x]:
        screen.blit(background, (0,0))
        pygame.display.update()
        start_game(keys)
        run = False

    pygame.display.update() 


pygame.quit






