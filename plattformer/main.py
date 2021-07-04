# Credits to: Lucas Wikström, for photoshopping images and material into its proper shape.

import pygame
import random
import math
import schedule
import time


# obstacle
# The obstacle is a class, an abstraction, representing the obstacles that our lovely Nacka Flappy Bird most surely avoid
# in his journey to Slussen.

class obstacle:
    def __init__(self,T,H):
        self.TYPE = T
        self.HEIGHT = H
        self.X = 1000
        self.DANGERZONE = []
        self.DANGERZONE2 = []
        self.OBST = pygame.image.load('OBST.png')

        if self.TYPE == "HIGH":
            self.DANGERZONE = [0,H*100]
            self.OBST = pygame.transform.scale(self.OBST, (10,H*100))

        elif self.TYPE == "LOW":
            self.DANGERZONE2 = [800-H*100,800]
            self.OBST = pygame.transform.scale(self.OBST, (10, H * 100))

        else:
            self.DANGERZONE = [0, H * 50]
            self.DANGERZONE2 = [800-H*50, 800]
            self.OBST = pygame.transform.scale(self.OBST, (10, H * 50))

    def collides(self, x, y):
        tol = 100
        D = self.X - x
        if(D <= tol):
            return self.checkDanger(y)
        return False

    # Collision detection with respect to the Y-coordinate
    def checkDanger(self, y):
        tol = 100
        print("IN DANGERZONE OK")
        if len(self.DANGERZONE) > 0:
            d1 = 0
            d2 = self.DANGERZONE[1]

            if(y <= d2):
                return True

        if len(self.DANGERZONE2) > 0:
            d1 = self.DANGERZONE2[1]
            d2 = 800

            if(y >= d1):
                return True

    def paintObst(self):
        # TODO FIXA Y
        if self.TYPE == "HIGH":
            screen.blit(self.OBST, (self.X, 0))
        elif self.TYPE == "LOW":
            screen.blit(self.OBST, (self.X, 800-self.HEIGHT*100))
        else:
            screen.blit(self.OBST, (self.X,800-self.HEIGHT*50)) #Lower end
            screen.blit(self.OBST, (self.X,0)) # Upper end



    def decrementX(self, speed):
        self.X -= speed

    def getX(self):
        return self.X

pygame.init()

# Create the screen:
screen = pygame.display.set_mode((1200,800))

# Obstacle List:
listOfObst = []

# Captions, logo and title
icon = pygame.image.load('bird.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("Flappy Nacka Bird")

# Player images
playerIMG = pygame.image.load('bird.png')
playerIMG = pygame.transform.scale(playerIMG,(100,100))
playerIMG2 = pygame.transform.scale(playerIMG,(40,40))

# Game over image
GOImage = pygame.image.load('bird2.png')
GOImage = pygame.transform.scale(GOImage, (400,400))

# Win image:
winImage = pygame.image.load('winImage.png')
winImage = pygame.transform.scale(winImage, (1200,800))

# Speech
pratImage  = pygame.image.load('prat1.png')
pratImage2 = pygame.image.load('prat2.png')
pratImage3 = pygame.image.load('prat3.png')
pratImage4 = pygame.image.load('prat4.png')
pratImage5 = pygame.image.load('prat5.png')

# Sun Image
sunImage = pygame.image.load('sun.png')
sunImage = pygame.transform.scale(sunImage, (100,100))

# Player data:
playerX = 50
playerY = 500
upwardSpeed = 0
gravitationalPull = 0

# Obstacle object
ob = None

# Score text:
score = 0
font = pygame.font.SysFont(None,24)
textImg = font.render('Score: ' + score.__str__(), True, (255,255,255))

def player(x, y):
    screen.blit(playerIMG, (x,y))

def upwardInclination(upwardSpeed):
    flapFactor = 0.1

    if upwardSpeed > 0:
        upwardSpeed += flapFactor
    elif upwardSpeed == 0:
        upwardSpeed += flapFactor
    else:
        upwardSpeed += flapFactor

    return upwardSpeed

def gravitationalPull():
    None

# A function that generates a random height on an obstacle that is in it of itself assumed to be randomized between
# three types: High, Split and Low where the two later are objects rising from the ceiling or the bottom respectively.
# Split means that the obstacle will be of both types, and that the flappy bird will have to fly inbetween.

def generateObstacle():
    obstType = ""
    r = random.randint(1,3)
    h = random.randint(1,5)

    if r == 1:
        obstType = "HIGH"
    elif r == 2:
        obstType = "SPLIT"
    else:
        obstType = "LOW"

    global ob
    ob = obstacle(obstType,h)


def increaseScore():
    global score
    global incrementation
    score += 100
    incrementation = False

def downwardInclination():
    global upwardSpeed
    print("YO")
    upwardSpeed -= 0.15

def moveObject():
    global speed
    speed = 5
    # Ha speed ökande TODO

    ob.decrementX(speed)

speed = 0
schedule.every(1).second.do(downwardInclination)
schedule.every(0.5).seconds.do(increaseScore)
schedule.every(0.05).seconds.do(moveObject)

running = True
gameOver = False
win = False

while running:
    if ob == None or ob.getX() < 0:
        generateObstacle()

    # Starting Canvas:
    if gameOver:
        if win:
            screen.blit(winImage,(0,0))
        else:
            screen.fill((0, 75, 0))
            screen.blit(GOImage,(200,200))
            font = pygame.font.SysFont(None, 62)
            textImg2 = font.render('Final Score: ' + score.__str__(), True, (255, 255, 255))
            screen.blit(textImg2, (600,300))
    else:
        screen.fill((0,0,75))
        screen.blit(sunImage, (1050, 25))

        # Bird speech:
        if score >= 500 and score <= 1000:
            screen.blit(pratImage, (playerX + 75, playerY - 250))
        elif score >= 2500 and score <= 3000:
            screen.blit(pratImage2, (playerX + 75, playerY - 250))
        elif score >= 5000 and score <= 5500:
            screen.blit(pratImage3, (playerX + 75, playerY - 250))
        elif score >= 7500 and score <= 8000:
            screen.blit(pratImage4, (playerX + 75, playerY - 250))
        elif score >= 10500 and score <= 11000:
            screen.blit(pratImage5, (playerX + 75, playerY - 250))

        # Set Win condition
        if(score >= 12000):
            win = True
            gameOver = True


        # Drawing the Score
        textImg = font.render('Score: ' + score.__str__(), True, (255, 255, 255))
        screen.blit(playerIMG2,(30,25))
        screen.blit(textImg, (75,40))

        # Drawing the player:
        player(playerX, playerY)

        # Key event:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    upwardSpeed = upwardInclination(upwardSpeed)

        # Timer:
        schedule.run_pending()

        if (not(ob == None)):
            # Draw Obstacle
            ob.paintObst()

            # Collision detection:
            if ob.collides(playerX,playerY):
                gameOver = True

        # Boundaries
        if playerY <= 0:
            playerY = 0
            gameOver = True
        elif playerY >= 800:
            playerY = 800
            gameOver = True

        else:
            playerY += -upwardSpeed

    pygame.display.update()
