''' Belgrade 1456
    This game is a little bit larger than many of the other games and an ongoing project as of 07-02. The game is of the
    historic battle of Belgrade or Nandorfehervar in 1456. 
'''

import pygame
import math
import unittest

# bullet (CLASS)
# A class for bullets fired by the player. The class contains methods for drawing as well as for looking for collisions
# with data inputted.

class bullet:
    def __init__(self, x, y):
        self.x = x
        self.initX = x
        self.y = y
        self.initY = y
        self.image = pygame.image.load('bullet.png')
        self.image = pygame.transform.scale(self.image, (20,20))

    # getX()
    # Simply returns the X coordinate
    def getX(self):
        return self.x

    # checkCollision()
    # Checks the Euclidean distance with a tolerance 'tol' so that if the distance is smaller than the tolerance we score as hit:
    def checkCollision(self, pX,pY):
        d = math.sqrt(math.pow((pX-self.x),2) + math.pow((pY-self.y),2))
        tol = 10
        if (d <= tol):
            return True
        return False

    # drawBullet()
    # Draws the bullet on the field and increments it x-value for the next call so that the bullet is moving.
    def drawBullet(self, multiplier):
        if(self.x <= 1200 and self.x > 0):
            screen.blit(self.image, (self.x, self.y))
            self.x += 40*multiplier

        return self.x

    # reset()
    # A function that is called once the bullet reaches a certain threshold. The reset function simply resets the bullet to be in
    # its initial position in regards to X and Y, so that a shot can be fired again.
    def reset(self):
        self.x = self.initX
        self.y = self.initY

# enemy (CLASS)
# A class that draws and logically instructs how an enemy should behave. This is regarding things such as movement,
# attacks, etc. The class takes in x and y-coordinates as well as a type t, the type t describes what kind of enemy it is.
# 1. = Swordsman, 2. = Gunman.

class enemy:
    def __init__(self, x, y, t, id, c):
        self.x = x
        self.y = y
        self.type = t
        self.id = id
        self.attackCounter = c

        if t == 1:
            self.attackAnimation = swordAttackAnimation
        else:
            self.attackAnimation = gunAttackAnimation
            self.bullet = bullet(self.x-stepsize, self.y+stepsize)
            self.shot = False

    # getID()
    # A function that returns the ID of an enemy object.

    def getID(self):
        return self.id

    # setID()
    # A setter function that sets the ID to be a specified integer, <id>.

    def setID(self, id):
        self.id = id

    def getX(self):
        return self.x

    # drawEnemy()
    # A function that simply blits an enemy that is just standing, that is not attacking.

    def drawEnemy(self):
        screen.blit(self.attackAnimation[0], (self.x, self.y))

    # attack()
    # A general function that animates attacks made by an enemy object and also handles the logic of it
    # with the help of the function attackCollision, that checks if the player was hit.

    def attack(self, px, py):
        self.attackCounter += 1
        if (self.attackCounter == len(self.attackAnimation)):
            self.attackCounter = 0

        screen.blit(self.attackAnimation[self.attackCounter], (self.x, self.y))

        if(self.type == 1):

            ret = False
            if(self.attackCounter == len(self.attackAnimation)):
                ret = True

            if(ret):
                return self.attackCollision(px, py)
            return False

        elif self.type == 2:

            if(self.shot):
                self.bullet.drawBullet(-1)

            elif self.attackCounter == 0:
                self.shot = True




    # moveLeft(), moveRight()
    # Two functions that moves an enemy object to the left or to the right respectively, a distance based on whatever the
    # global stepsize is.

    def moveLeft(self):
        self.x -= stepsize

    def moveRight(self):
        self.x += stepsize

    # attackCollision
    # A helper function used by the attack function to check for player collision when attacking.
    # If such a collision occurs the object returns true, so that the game can account for the player
    # getting hit.

    def attackCollision(self, px, py):
        if(self.y == py):
            D = abs((self.x-100) - px)
            if(D < 25):
                return True

    # checkCollision()
    # A function used by the enemy class to see if a collision is made. This collision pertains specifically to a
    # collision made by the player on the enemy object, if a player shoots or stabs an enemy object etc. If so, the
    # enemy object return a True statement as well as a list containing the x and y coordinates and whatever type the
    # enemy object is of. This list then becomes a sublist stored in the deadList, and is plotted on the field.

    def checkCollision(self, x, y):
        D = math.sqrt(math.pow((self.x - x),2) + math.pow((self.y - y),2))

        if(D < tol):
            return True, [self.x, self.y, self.type]
        else:
            return False, []

# drawBlock
# drawBlock is a helper function that simply takes in a list of images and then draws them out, incrementing the step with a modulo, max, that is
# recommended to be of the size of the list l. This construct allows fo the animation of pictures in a while loop, e.g the while loop that constitutes
# the actual game.

def drawBlock(current, l, max, x, y):
    screen.blit(l[current], (x,y))

    if(current == max - 1):
        return 0
    else:
        return current + 1

# generateEnemy
# generateEnemy takes a global list and inserts into it an enemy object with specifications given as parameter. x and y both give the x and the y
# coordinates respectively, t gives what type the enemy is of 1 = swordsman, 2 = gunman, and id gives a specific id pertaining to the place also in
# which the enemy is within the list.

def generateEnemy(x, y, t, id, c):
    print("Generating enemies")
    global enemyList
    e = enemy(x,y,t, id, c)
    enemyList.append(e)

# drawBodies
# drawBodies takes in a list consisting of dead enemies and it plots out these on the battlefield. After an enemy has been killed, by sword or by
# bullet, the enemy is transfered from the enemyList to the deadList. The deadList is then passed onto this function that draws the bodies of all
# the enemies that have died.

def drawBodies(l):
    for i in l:
        x = i[0]
        y = i[1]
        t = i[2]
        if t == 1:
            screen.blit(deadTurkishSoldierImage, (x,y))
        # TODO lägg till gunman

# animateHealthAndAmmo
# This function takes in the amount of hp and ammo that the player still has and plots that onto the canvas.
# If the parameter 'testing' is True the game will display the enemyList as the 'Testing Mode' is enabled and
# that is something we can enable and disable.

def animateHealthAndAmmo(hp, ammo):
    testing = False
    font = pygame.font.SysFont('Comic Sans MS', 30)
    if(testing):
        global  enemyList
        str = ""
        for e in enemyList:
            str += e.getID().__str__()
        ammoText = font.render("Enemy List:  " + str, False, (0, 0, 0))
        hpText = font.render("Testing Mode", False, (0,0,0))
    else:
        hpText = font.render("Health: " + hp.__str__(), False, (0,0,0))
        ammoText = font.render("Ammo:  " + ammo.__str__(), False, (0,0,0))


    screen.blit(hpText, (100,700))
    screen.blit(hunFlag, (70, 710))
    screen.blit(ammoText, (100, 740))
    screen.blit(barrel, (70, 750))

# setState
# setState is a function that takes in a 'level' as parameter which is a y-level and the function then loads the images of correct
# size. E.G: If a character moves upward, the setState function will set the image of the player in accordance with the y-level.

def setState(level):
    global playerImage
    playerImage = pygame.transform.scale(playerImage, (20*level, 20*level))

# updateList()
# A function that updates the enemyList and the removeList. Specifically, if an enemy is killed, for instance an enemy
# with id = 2, when there are 4 enemies with these ids: [1,2,3,4]. What should happen then is that id 3 and id 4 resp
# should be decremented so that the list [1,2,3,4] -> [1,2,3], after enemy with id 2 is removed. This function takes care
# of that update. This is done in two steps:
# 1. First the ids are updated in 'enemyList'
# 2. Second, the enemies in the list 'removeList' are popped from 'enemyList'. As per the example above, if an enemy with
# id = 2 is killed, removeList = [2], enemyList becomes updated as [1,2,2,3], and then removeList is iterated removing one of
# the instances of '2' so that we get [1,2,3] after killing an enemy (independantly of what ID the enemy holds).

def updateList(id):
    global enemyList
    global removeList

    if (id >= 0):
        i = 0
        length = len(enemyList)
        while (i < length):
            if (i >= id):
                enemyList[i].setID(i)

            i += 1

    # Removing dead enemies:
    while (not removeList == []):
        d1 = removeList.pop(0)
        enemyList.pop(d1 - 1)

pygame.init()
screen = pygame.display.set_mode((1200,800))

# Create main menu background, Icon and Caption:
Nandorfehervar = pygame.image.load('nandorfehervar.png')
Nandorfehervar = pygame.transform.scale(Nandorfehervar, (1200,800))
iconPic = pygame.image.load('hun.png')
pygame.display.set_caption("Belgrade 1456")
icon = pygame.display.set_icon(iconPic)


# Player Data:
# This is all data that is necessary for logic and rendering regarding the player.

playerX = 100
Ylevel = 10
playerY = 500
playerStatus = "ready"
yMaxLevel = 10
yMinLevel = 5
endOfLevel = 1200

stepsize = 50
playerCurrent = 0
bulletOffsetX = 10
bulletOffsetY = 115
playerBullet = bullet(playerX+bulletOffsetX,playerY+bulletOffsetY)
ammunition = 20
health = 10

# List of Enemies.
enemyList = []
deadList = []
global tol
tol = 25

# ANIMATIONS
# Down below comes animations for the game:

# Turkish Soldier Animation:
turkishSoldierImage = pygame.image.load('turkishSoldier.png')
turkishSoldierImage = pygame.transform.scale(turkishSoldierImage, (150,150))
turkishSoldierAttack = pygame.image.load('turkishSoldierAttack.png')
turkishSoldierAttack = pygame.transform.scale(turkishSoldierAttack, (150,150))

# Turkish Rifleman Animation:
turkishRiflemanImage = pygame.image.load('rifleman.png')
turkishRiflemanImage = pygame.transform.scale(turkishRiflemanImage, (150,150))
turkishRiflemanAttack = pygame.image.load('riflemanFire.png')
turkishRiflemanAttack = pygame.transform.scale(turkishRiflemanAttack, (150,150))


swordAttackAnimation = [turkishSoldierAttack, turkishSoldierImage, turkishSoldierImage, turkishSoldierImage]
gunAttackAnimation = [turkishRiflemanAttack, turkishRiflemanImage, turkishRiflemanImage, turkishRiflemanImage]

# Killed Enemies:
deadTurkishSoldierImage = pygame.image.load('deadTurkishSoldier.png')
deadTurkishSoldierImage = pygame.transform.scale(deadTurkishSoldierImage, (185,185))

# Backgrounds:
background = pygame.image.load('bg.png')
background = pygame.transform.scale(background, (1200,800))
background2 = pygame.image.load('bg2.png')
background2 = pygame.transform.scale(background2, (1200,800))
background3 = pygame.image.load('bg3.png')
background3 = pygame.transform.scale(background3, (1200,800))
background4 = pygame.image.load('bg4.png')
background4 = pygame.transform.scale(background4, (1200,800))
background5 = pygame.image.load('bg5.png')
background5 = pygame.transform.scale(background5, (1200,800))
background6 = pygame.image.load('bg6.png')
background6 = pygame.transform.scale(background6, (1200,800))
background7 = pygame.image.load('bg7.png')
background7 = pygame.transform.scale(background7, (1200,800))
# Cannon Sprites:
#

cannonX = 75
cannonY = 20
cannon1 = pygame.image.load('leftCannon1.png')
cannon1 = pygame.transform.scale(cannon1, (cannonX, cannonY))
cannon2 = pygame.image.load('leftCannon2.png')
cannon2 = pygame.transform.scale(cannon2, (cannonX, cannonY))
cannon3 = pygame.image.load('leftCannon3.png')
cannon3 = pygame.transform.scale(cannon3, (cannonX, cannonY))
cannonList = [cannon1, cannon1, cannon1, cannon2, cannon3, cannon3, cannon3]
cannonMax = len(cannonList)

currentCannon1 = 0
currentCannon2 = 0
currentCannon3 = 0
currentCannon4 = 0

# Player animation
# This is the regular player animation, we make an image object called playerImage simply.
playerImage = pygame.image.load('player1.png')
playerImage = pygame.transform.scale(playerImage, (200,200))

# Stabbing animation
# As for stabbing with the word we make a list called 'attackAnimation' where we put the regular player
# sprite as well as an attacking motion, and in alternating between the two we can draw an attack by the player.
# This is a trick that we are using for multiple animations, cannons, attacking animations, fire animations etc, we put
# the sprites into a list and we have a counter for which one to paint so as to present an illusion of animation.

attackImage = pygame.image.load('playerAttack.png')
attackImage = pygame.transform.scale(attackImage, (200,200))
attackImage2 = pygame.image.load('playerAttack2.png')
attackImage2 = pygame.transform.scale(attackImage2, (200,200))
attackAnimation = [attackImage, attackImage2]

# Player Fire Animation:
# As with the stabbing motions we use a list and a counter to animate firing the gun. We also define a variable called
# gunStatus that tells us if the gun is ready for firing.

gunStatus = "ready"
fireImage = pygame.image.load('playerShoot1.png')
fireImage = pygame.transform.scale(fireImage, (200,200))
fireImage2 = pygame.image.load('playerShoot2.png')
fireImage2 = pygame.transform.scale(fireImage2, (200,200))
fireAnimation = [fireImage, fireImage]
fireAnimation2 = [fireImage, fireImage2]

# Gunman Animation:
# Rendering gunmen handling the cannons on level 1 etc.

gunmanImage = pygame.image.load('gunman.png')
gunmanImage4 = pygame.transform.scale(gunmanImage, (90,90))
gunmanImage3 = pygame.transform.scale(gunmanImage,(75, 75))
gunmanImage2 = pygame.transform.scale(gunmanImage, (60, 60))
gunmanImage = pygame.transform.scale(gunmanImage, (40,40))

# Soldier animation
# Animating the soldier hurrying to the walls in level 2 etc. Every soldier has a different
# x-coordinate that is decremented whereas their y-coordinates remain the same so it looks as
# if they are runing in a line, when the player enters level 2 that is (see level 2 below for more info).

hungarianSoldierImage = pygame.image.load('hungarianSoldier.png')
hungarianSoldierImage = pygame.transform.scale(hungarianSoldierImage, (75,75))
hungarianSoldierFlagImage = pygame.image.load('hunSoldierFlag.png')
hungarianSoldierFlagImage = pygame.transform.scale(hungarianSoldierFlagImage, (75,75))
deadHungarianSoldier = pygame.image.load('deadHungarianSoldier.png')
deadHungarianSoldier = pygame.transform.scale(deadHungarianSoldier, (75,75))

soldier1 = 200
soldier2 = 300
soldier3 = 400
soldier4 = 500

# Flag pic and Small Barrell.
# Just rendering barrels and flags that are meant to be ammo and health packs:

hunFlag = pygame.image.load('hun.png')
hunFlag = pygame.transform.scale(hunFlag, (25,25))
barrel = pygame.image.load('barrel.png')
barrel = pygame.transform.scale(barrel, (25, 25))

# Message animation
# Animating a "flashing animation" for the introduction message in level 2.

message1 = pygame.image.load('message1.png')
message1 = pygame.transform.scale(message1, (100,100))
message2 = pygame.image.load('message2.png')
message2 = pygame.transform.scale(message2, (100, 100))
messageCurrent = 0
messageList = [message1, message2]
messageMax = len(messageList)

# Next Level Animation:
# Animating the arrow that is displayed when a level is cleared of enemies.

nlAnimation1 = pygame.image.load('NextLevel1.png')
nlAnimation1 = pygame.transform.scale(nlAnimation1, (100,100))
nlAnimation2 = pygame.image.load('NextLevel2.png')
nlAnimation2 = pygame.transform.scale(nlAnimation2, (100,100))
nlList = [nlAnimation1, nlAnimation2]
nlMax = len(nlList)
nextLevelCurrent = 0
nextLevelX = 1000
nextLevelY = 250

# Cannon Ball Animations
# For level 5 specifically we animate ottoman cannon balls pounding the Hungarian wall.
# As always we adopt the same trick of animation, that is putting the rendered images into a list.

cannonBall1 = pygame.image.load('Cannonball1.png')
cannonBall1 = pygame.transform.scale(cannonBall1, (100,100))
cannonBall2 = pygame.image.load('Cannonball2.png')
cannonBall2 = pygame.transform.scale(cannonBall2, (100,100))
cannonBallList = [cannonBall1, cannonBall2]
cannonBallMax = len(cannonBallList)
cannonBallCounter = 0

mainMenu = pygame.image.load('menu.png')
mainMenu = pygame.transform.scale(mainMenu,(400,400))
settings = pygame.image.load('settings.png')
settings = pygame.transform.scale(settings, (400,400))
loadGame = pygame.image.load('load_games.png')
loadGame = pygame.transform.scale(loadGame, (400,400))

choose = pygame.image.load('choose.png')

# Adjusting game settings
running = True
level = 0
clear = False
drawnLevel = level-1
menuLevel = [1,1]

while running:
    screen.fill((0,0,180))
    menu = False

    if(enemyList == []):
        clear = True
    else:
        clear = False

    if(clear and playerX >= endOfLevel):
        level += 1
        clear = False
        playerX = 200
        playerY = 300
        deadList = []

    if(level == 0):
        screen.blit(Nandorfehervar, (0,0))
        menu = True

        if(menuLevel[0] == 1):
            screen.blit(mainMenu, (350,150))
        elif menuLevel[0] == 2:
            screen.blit(loadGame, (350,150))
        elif menuLevel[0] == 3:
            screen.blit(settings, (350,150))

        screen.blit(choose, (400, menuLevel[1] * 65 + 220))
    else:
        pygame.time.delay(200)


    # level 1
    # Level 1 is an introductory level, the player is introduced to the ongoing siege of the city, cannon men are animated
    # using the function drawBlock that animates a list of rendered images. The levels has no enemies, as can be seen, the
    # function generateEnemy() is never called.

    if(level == 1):
        # Draw Level One
        screen.blit(background,(0,0,))

        # Draw Canons on the rampart:
        currentCannon1 = drawBlock(currentCannon1, cannonList, cannonMax, 190, 155)
        currentCannon2 = drawBlock(currentCannon2, cannonList, cannonMax, 100, 245)
        currentCannon3 = drawBlock(currentCannon3, cannonList, cannonMax, 280, 105)
        currentCannon4 = drawBlock(currentCannon4, cannonList, cannonMax, 10, 335)

        screen.blit(gunmanImage, (360, 80))
        screen.blit(gunmanImage2,(275,135))
        screen.blit(gunmanImage3, (185, 225))
        screen.blit(gunmanImage4, (125, 285))

        if(drawnLevel == 0):
            drawnLevel = 1

    # Level 2
    # Level 2 follows the same principle as Level 1 in that there are no enemies, it is an introductary level.
    # This level gives information to the player that he or she can make use of come the next levels.

    if(level == 2):
        screen.blit(background2,(0,0))
        messageCurrent = drawBlock(messageCurrent, messageList, messageMax, 950, 120)

        if(soldier1 > 0):
            screen.blit(hungarianSoldierFlagImage, (soldier1, 150))
            soldier1 -= 10

        if(soldier2 > 0):
            screen.blit(hungarianSoldierImage, (soldier2, 150))
            soldier2 -= 10

        if(soldier3 > 0):
            screen.blit(hungarianSoldierImage, (soldier3, 150))
            soldier3 -= 10

        if(soldier4 > 0):
            screen.blit(hungarianSoldierImage, (soldier4, 150))
            soldier4 -= 10

        if(drawnLevel == 1):
            drawnLevel = 2

    # Level 3
    # Level 3 is a tutorial level in which there is an enemy but who is not attacking, he is just standing
    # and the player must end him before moving on.

    if(level == 3):
        screen.blit(background3, (0,0))
        screen.blit(deadHungarianSoldier, (100,100))
        screen.blit(deadHungarianSoldier, (300, 100))
        screen.blit(deadHungarianSoldier, (500, 150))
        screen.blit(deadHungarianSoldier, (500, 370))
        screen.blit(deadHungarianSoldier, (200, 300))

        if drawnLevel == 2:
            drawnLevel = 3
            generateEnemy(400,500,1,1, 1)

        for e in enemyList:
            e.drawEnemy()

    # Level 4
    # Level 4 is the first real level in which there are stationary enemies wielding swords. The player must
    # kill them in order to proceed.

    if(level == 4):
        screen.blit(background4, (0,0))

        if drawnLevel == 3:
            print("YO 416")
            drawnLevel = 4
            generateEnemy(200, 300, 1, 1, 0)
            generateEnemy(400, 300, 1, 2, 1)
            generateEnemy(400, 500, 1, 3, 2)
            generateEnemy(700, 500, 1, 4, 3)


        for e in enemyList:
            if e.attack(playerX, playerY):
                health -= 1
    # Level 5
    # Level 5 constricts the players movement by putting him in a restricted courtyard. Here the fighting is
    # very thick and the player must eliminate moving targets that are also attacking.
    # In the background the animation of the mythical Titus Dugovićs from the battle can be seen on the tower as
    # he is pushing down the Ottoman flag holder and they both fall down towards their deaths.
    
    if(level == 5):
       screen.blit(background5, (0, 0))
       yMinLevel = 7
       yMaxLevel = 10

       if(drawnLevel == 4):
            drawnLevel = 5
            playerY = 50*Ylevel
            endOfLevel = 400
            nextLevelX = 500
            nextLevelY = 450

            startX = 10*stepsize
            generateEnemy(startX, 50*10,1,1,0)
            generateEnemy(startX, 7*50, 1, 2, 1)
            movingRight = False

       for e in enemyList:
           if e.attack(playerX, playerY):
               health -= 1

           if e.getID() == 1 and len(enemyList) > 1:
               if e.getX() > 300 and not movingRight:
                    e.moveLeft()
               else:
                    e.moveRight()
                    movingRight = True

                    if e.getX() >= startX:
                        movingRight = False

    # Level 6
    # On this level the player is on the actual battlements and as such his movements are constricted even more so.
    # The battle is exceedingly thick here and soldiers are blocking the way, the player can only move in two y-levels,
    # ylevel = 10 and ylevel = 9, respectively. In some of these levels, or lanes if one so wishes, the way is blocked
    # by Hungarian soldiers.
    # TODO fixa level 6

    if(level == 6):
        screen.blit(background6, (0, 0))

        if(drawnLevel == 5):
            drawnLevel = 6
            yMinLevel = 3
            yMaxLevel = 5
            yLevel = 3
            playerY = yLevel*50

            # Gunmen
            generateEnemy(700, 250, 2, 1, 1)

        for e in enemyList:
            e.attack(playerX, playerY)

    # Level 7
    # Just Going up a tower, no enemies:
    if (level == 7):
        screen.blit(background7, (0,0))

        if(drawnLevel == 6):
            drawnLevel = 7
            endOfLevel = 500
            yLevel = 7

    if (level == 8):
        None

    drawBodies(deadList)
    animateHealthAndAmmo(health, ammunition)

    # Navigating menus:
    if(level == 0):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and menuLevel[1] > 1:
                    menuLevel[1] = menuLevel[1] - 1

                elif event.key == pygame.K_DOWN and menuLevel[1] < 4:
                    menuLevel[1] = menuLevel[1] + 1

                elif event.key == pygame.K_RETURN:
                    if menuLevel[0] == 1:
                        if menuLevel[1] == 1:
                            level += 1

                        elif menuLevel[1] == 2:
                            menuLevel[0] = 2
                            menuLevel[1] = 1

                        elif menuLevel[1] == 3:
                            menuLevel[0] = 3

                        elif (menuLevel[1] == 4):
                            running = False

                    elif menuLevel[0] == 2:
                        if menuLevel[1] == 1:
                            menuLevel[0] = 1
                            menuLevel[1] = 1

                    elif menuLevel[0] == 3:
                        if menuLevel[1] == 1:
                            menuLevel[0] = 1
                            menuLevel[1] = 1

    # Moving in the game:
    else:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    playerX += stepsize

                if event.key == pygame.K_LEFT:
                    playerX -= stepsize

                if event.key == pygame.K_UP and Ylevel > yMinLevel:
                    Ylevel -= 1
                    playerY = Ylevel*50

                if event.key == pygame.K_DOWN and Ylevel < yMaxLevel:
                    Ylevel += 1
                    playerY = Ylevel * 50

                if event.key == pygame.K_f:
                    if(playerStatus == "ready"):
                        playerStatus = "gun"
                    else:
                        playerStatus = "ready"

                if event.key == pygame.K_SPACE:
                    if playerStatus == "ready":
                        playerStatus = "stabbing"

                    elif playerStatus == "stabbing":
                        playerStatus = "ready"

                    elif playerStatus == "gun":
                        playerStatus = "firing"
                        playerBullet = bullet(playerX + bulletOffsetX,playerY + bulletOffsetY)
                        ammunition -= 1


    # Draw if level is cleared:
    if(clear):
        nextLevelCurrent = drawBlock(nextLevelCurrent, nlList,nlMax,      nextLevelX, nextLevelY)


    # Draw player:
    if playerStatus == "ready":
        screen.blit(playerImage, (playerX,playerY))

    # Registring Stabbings:
    elif playerStatus == "stabbing":
        playerCurrent = drawBlock(playerCurrent,attackAnimation,len(attackAnimation), playerX, playerY)
        removeList = []
        id = -1

        for e in enemyList:
            hit,coordinateList = e.checkCollision(playerX+200, playerY)
            if(hit):
                id = e.getID()
                print("HIT ENEMY: " + e.getID().__str__())
                removeList.append(e.getID())
                deadList.append(coordinateList)

        updateList(id)

    elif playerStatus == "gun":
        playerCurrent = drawBlock(playerCurrent,fireAnimation,len(fireAnimation), playerX, playerY)

    # Registring Shot Enemies:
    elif playerStatus == "firing":
        id = -1

        if playerBullet.getX() <= endOfLevel:
            bulletX = playerBullet.drawBullet(1)
            playerCurrent = drawBlock(playerCurrent,fireAnimation2,len(fireAnimation2), playerX, playerY)
            removeList = []

            for e in enemyList:
                hit, coordinateList = e.checkCollision(bulletX, playerY)
                if (hit):
                    id = e.getID()
                    print("SHOT ENEMY: " + e.getID().__str__())
                    removeList.append(e.getID())
                    deadList.append(coordinateList)


        else:
            playerStatus = "gun"
            playerBullet.reset()

        updateList(id)

    pygame.display.update()
