''' Race_Cars
    Race_Cars is a simple game where the player simply controlls a car going in a singular direction by pressing space.
    The player is racing against three other cars and if the player can reach the finish line before the other cars the
    player will win. If any of the other cars reach the finish line before the player, the player loses. The game is made
    by having an action listener listening for space, moving the player in the x-direction. The other car moves based on
    a time ticking.
'''

import pygame
import random

pygame.init()
screen = pygame.display.set_mode((1200,800))

running = True
xCoordinates = [0,0,0,0]
yCoordinates = [400,500,600,700]

p1 = pygame.image.load('p1.png')
p1 = pygame.transform.scale(p1, (75,75))
p2 = pygame.image.load('p2.png')
p2 = pygame.transform.scale(p2, (75,75))
p3 = pygame.image.load('p3.png')
p3 = pygame.transform.scale(p3, (75,75))
p4 = pygame.image.load('p4.png')
p4 = pygame.transform.scale(p4, (75,75))

loseim = pygame.image.load('lose.png')
loseim = pygame.transform.scale(loseim, (1200, 800))
winIm = pygame.image.load('win.png')
winIm = pygame.transform.scale(winIm, (1200, 800))

cars = [p1,p2,p3,p4]
win = False
lose = False
while running:
    screen.fill((0,0,200))
    pygame.draw.rect(screen,(0,200,0), pygame.Rect(0, 300, 1200, 1200))

    if(xCoordinates[0] >= 1200):
        win = True

        for i in range(3):
            if xCoordinates[i+1] >= 1200:
                lose = True

    for i in range(len(cars)):
        screen.blit(cars[i], (xCoordinates[i],yCoordinates[i]))

    if(pygame.time.get_ticks() % 260 > 250):

        r1 = random.randint(1,8)
        r2 = random.randint(1,8)
        r3 = random.randint(1,8)

        xCoordinates[1] += r1*0.7
        xCoordinates[2] += r2*0.7
        xCoordinates[3] += r3*0.7

    for event in pygame.event.get():
        if(event.type == pygame.KEYDOWN):
            if event.key == pygame.K_SPACE:
                if(win or lose):
                    exit()
                else:
                    xCoordinates[0] += 10

    if win:
        screen.blit(winIm,(0,0))
    elif lose and not win:
        screen.blit(loseim, (0,0))

    pygame.display.update()

