import pygame
import random

pygame.init()

# Create the screen:
screen = pygame.display.set_mode((1200,800))

# Create Icon and Caption:
icon = pygame.image.load("squirrel1.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Squirrels of Ektorp")

# Create Sky images
cloud1 = pygame.image.load('cloud.png')
cloud1 = pygame.transform.scale(cloud1,(200,200))
cloud2 = pygame.image.load('cloud2.png')
cloud2 = pygame.transform.scale(cloud2,(200,200))
cloud3 = pygame.image.load('cloud3.png')
cloud3 = pygame.transform.scale(cloud3,(200,200))

skyImage = pygame.image.load('sky.png')
skyImage = pygame.transform.scale(skyImage, (200,200))

# Player data
playerX = 0
playerY = 0
playerStatus = "walking"
gravity = 9.82
upwardSpeed = gravity

# Player Animation
initList = [pygame.image.load('squirrel1.png'), pygame.image.load('squirrel2.png'), pygame.image.load('squirrel3.png')]
walkList = [pygame.transform.scale(initList[0], (50,50)), pygame.transform.scale(initList[1], (50,50)), pygame.transform.scale(initList[2], (50,50))]
jumpInit = [pygame.image.load('squirrelJump1.png')]
jumpList = [pygame.transform.scale(jumpInit[0], (50,50))]
maxWalk = len(walkList)
maxJumps = len(jumpList)

# platforms
# A platform can consist of a tuple, its width and its y coordinates where each such tuple holds:
# the said width and the y of the platform:

plattformImage = pygame.image.load('plattform.png')
platformList = []

# big tree image:
bigTreeImage = pygame.image.load('bigtree.png')
pygame.transform.scale(bigTreeImage, (200, 2000))

running = True
gameOver = False

def generateSky():
    l1 = []
    l2 = []

    for i in range(6):
        bin = random.randint(1,2)
        if(bin == 1):
            rand = random.randint(1,3)
            l1.append(rand)
        else:
            l1.append(0)

    for i in range(6):
        bin = random.randint(1,2)
        if(bin == 1):
            l2 .append(1)
        else:
            l2.append(0)

    return (l1, l2)

def generatePlatforms():
    l = [(200,200)]
    length = 200
    prevY = 200
    while length <= 1200:
        rand = random.randint(1,4)
        length += rand * 100
        y = rand * 50 + prevY
        l.append((length, y))
        prevY = y

    return l

def drawPlatforms(l):
    platforms = len(l)
    for i in range (platforms-1):
        width = l[i+1][0] - l[i][0]
        x = l[i][0]
        y = l[i][1]
        p = pygame.transform.scale(plattformImage,(width, 20))
        screen.blit(p, (x,y))

def checkPlatform(l, pX, pY):
    for i in range (len(l)-1):
        xStart = l[i][0]
        xEnd = l[i+1][0]
        y = l[i][1]

        #print(xStart, xEnd, y)
        if(pX >= xStart and pX <= xEnd):
            if(y >= pY and abs(y-pY) < 10):
                #print("Returning: " + (y-50).__str__())
                return y-50, i+1

    return -1,0

def paintSky(l):
    l1 = l[0]   # First layer of sky.
    l2 = l[1]   # Second layer of sky.

    # Different type of clouds are possible for the highest layer:
    for i in range(6):
        if(l1[i] == 1):
            screen.blit(cloud1, (200*i,0))
        elif(l1[i] == 2):
            screen.blit(cloud2, (200 * i, 0))
        elif(l1[i] == 3):
            screen.blit(cloud3, (200 * i, 0))
        else:
            screen.blit(skyImage, (200*i,0))

    # Will only write type one or clear sky:
    for i in range(6):
        if(l2[i] == 1):
            screen.blit(cloud1, (200*i,200))
        else:
            screen.blit(skyImage, (200*i,200))

    # This loop simply paints cloudless parts of the sky for the bottom layers:
    for i in range(6):
        screen.blit(skyImage, (200*i, 400))
        screen.blit(skyImage, (200 * i, 500))

def canWalk(l,pX, p):
    print(l[p+1][0], pX)
    if(l[p+1][0] >= pX):
        return True
    return False

l = generateSky()
platformList = generatePlatforms()
walkCounter = 0
jumpCounter = 0
ground = 700

while running:
    pygame.time.delay(50)
    pos, platform = checkPlatform(platformList, playerX, playerY)
    checkX = False
    print(playerStatus)
    if(playerStatus == "platform"):
        checkX = canWalk(platformList, playerX, platform)

    if(not pos == -1 and not playerStatus == "climbing" and not checkX):
        playerY = pos
        playerStatus = "platform"

    elif playerStatus == "platform" and checkX:
        #TODO Här är problemet:
        playerStatus = "walking"
    #    upwardSpeed = gravity

    # Reset if end of screen:
    if(playerX >= 1125):
        playerStatus = "climbing"
        upwardSpeed = -50

    if(playerX > 1250):
        playerX = 0
        playerY = 0
        upwardSpeed = gravity
        l = generateSky()
        platformList = generatePlatforms()
        playerStatus = "walking"

    if(playerY >= ground):
        gameOver = True

    if not(gameOver):
        screen.fill((0,75,0))
        paintSky(l)                             # Sky
        screen.blit(bigTreeImage, (-150, 50))   # Start Tree
        screen.blit(bigTreeImage, (1150, 50))   # Final Tree
        drawPlatforms(platformList)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and (not playerStatus == "jumping"):
                    playerStatus = "jumping"
                    upwardSpeed = -3


        # Draw the player:
        if playerStatus == "walking":
            upwardSpeed = gravity
            screen.blit(walkList[walkCounter], (playerX,playerY))
            walkCounter += 1
            if(walkCounter == maxWalk):
                walkCounter = 0

        elif playerStatus == "platform":
            screen.blit(walkList[walkCounter], (playerX,playerY))
            walkCounter += 1
            if(walkCounter == maxWalk):
                walkCounter = 0
            upwardSpeed = 0

        else: # playerStatus = "jumping":
            screen.blit(jumpList[jumpCounter], (playerX, playerY))
            jumpCounter += 1
            if (jumpCounter == maxJumps):
                jumpCounter = 0

            if(upwardSpeed <= gravity):
                upwardSpeed += 0.1
            else:
                playerStatus = "walking"



        # Player movement:
        playerX += 5
        playerY += upwardSpeed

    else: # GAME OVER
        None

    pygame.display.update()