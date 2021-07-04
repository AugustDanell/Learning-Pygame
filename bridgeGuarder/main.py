import pygame
import math
import random

pygame.init()
screen = pygame.display.set_mode((1200,800))

# Create Icon and Caption:
icon = pygame.image.load("boat.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Bridge Guarder")

openImage = pygame.image.load("bridgeOpen.png")
openImage = pygame.transform.scale(openImage, (1200,800))
closedImage = pygame.image.load("bridgeClosed.png")
closedImage = pygame.transform.scale(closedImage, (1200, 800))
currentImage = openImage

# Cow- and boat list
boats = []
cows = []

open = True
running = True
killedCows = 0
killedBoats = 0

def generate(open):
    R = random.randint(1,2)
    global cows
    global boats

    if(R == 1):
        cows.append(0)
    else:
        boats.append(-2)

def incrementAll():
    global killedCows
    global killedBoats

    a = len(boats)
    i = 0
    while i < a:
        if(not open and boats[i] in [3,4,5]):
           boats.pop(i)
           a -= 1
           killedBoats += 1
        else:
           boats[i] += 1
           i += 1

    a = len(cows)
    i = 0

    while i < a:
        if(open and cows[i] in [3,4,5]):
            cows.pop(i)
            a -= 1
            killedCows += 1
        else:
            cows[i] += 1
            i += 1


boat = pygame.image.load('boat.png')
boat = pygame.transform.scale(boat, (100,100))

cow = pygame.image.load('cow1.png')
cow = pygame.transform.scale(cow, (100,100))

font = pygame.font.SysFont(None,48)


while running:
    screen.blit(currentImage, (0, 0))
    cowText = font.render('Killed Cows ' + killedCows.__str__(), True, (255, 255, 255))
    boatText = font.render('Killed Boats ' + killedBoats.__str__(), True, (255, 255, 255))

    screen.blit(cowText,(800,20))
    screen.blit(boatText,(800,60))

    generate(open)
    incrementAll()

    #screen.fill((0,0,0))

    pygame.time.delay(1000)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if(open):
                    currentImage = closedImage
                    open = False
                else:
                    currentImage = openImage
                    open = True

    for i in boats:
        screen.blit(boat,(550,700-i*100))

    for i in cows:
        if not open or i not in [4,5]:
            screen.blit(cow, (100+100*i, 250))

    pygame.display.update()