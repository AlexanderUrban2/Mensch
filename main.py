import pygame
import random
import time
# pylint: disable=no-member
pygame.init()
pygame.font.init() 



#methodes
def init_dice(dice):
    for i in range(0,6):
        dice.append(pygame.image.load('Dice' + str(i+1) + '.png'))
        dice[i] = pygame.transform.scale(dice[i], (100, 100))
    return dice


def roll_dice(dice):
    for i in range (0,10):
        number = random.randint(0,5)
        pygame.display.update()
        screen.blit(background, (0,0))
        screen.blit(dice[number], (590,450))
        time.sleep(0.005)
    return number
        


def start_game(keys):
    run = True
    screen.blit(myfont.render('Press Space to roll the Dice', False, (0, 0, 0)), (500,900))
    pygame.display.update()
    while run:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    number = roll_dice(dice)
                    screen.blit(myfont.render('U can Move ' + str(number +1) + 'Steps now', False, (0, 0, 0)), (500,900))
                    pygame.display.update()

        






#main
screen_Width = 1280
screen_Height = 1000

background = pygame.image.load('GameField.jpg')
background = pygame.transform.scale(background, (1280, 1000))
screen = pygame.display.set_mode((screen_Width,screen_Height))
pygame.display.set_caption("Mensch ärgere dich nicht")
screen.fill((0,0,0))


myfont = pygame.font.SysFont('Comic Sans MS', 30)
screen.blit(myfont.render('Press X to start the Game', False, (255, 0, 0)), (500,450))

dice = []
dice = init_dice(dice)



run= True
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






