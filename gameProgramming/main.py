import pygame
import random
import math

# A Youtube Tutorial I followed for making a basic version of space invaders.
# All the work in this code segment is from that tutorial, we only make a small
# change which is to implement the game horisontally instead of vertically.
# Youtube Tutorial: https://www.youtube.com/watch?v=FfWpgLFMI7w&t=167s


pygame.init()

# Creates a screen:
screen = pygame.display.set_mode((1200,800))

# Captions, logo and title:
pygame.display.set_caption("Norrtälje Under Attack!")
icon = pygame.image.load('defender.png')
pygame.display.set_icon(icon)

# Score Icon
ScoreIMG = pygame.image.load('defender.png')
ScoreIMG = pygame.transform.scale(ScoreIMG,(100,75))

# Player
playerImg = pygame.image.load('defender.png')
playerImg = pygame.transform.scale(playerImg,(200,200))
playerX = 20
playerY = 300

# prat IMG 1
pratIMG = pygame.image.load('prat.png')
pratIMG = pygame.transform.scale(pratIMG,(200,200))

# Enemy
enemyImg = pygame.image.load('enemy.png')
enemyImg = pygame.transform.scale(enemyImg,(100,100))
enemyX = 1000
enemyY = random.randint(0, 600)
enemyX_change = 100
speedUp = False
enemyY_Change = 0.3 + speedUp

# Bullet - State of fire or state of ready:
bulletImg = pygame.image.load('laser1.png')
bulletImg = pygame.transform.scale(bulletImg, (50,50))
bulletX = 0
bulletY = 0
bulletX_change = 4
bulletY_change = 0
bullet_state = "ready"

# Text:
kills = 0
font = pygame.font.SysFont(None,24)
textImg = font.render('Slain Cossacks: ' + kills.__str__(), True, (255,255,255))

def isCollision(x1,x2,y1,y2):
    tol = 45
    dist = math.sqrt(math.pow((x1-x2),2) + math.pow((y1-y2),2))
    if dist < tol:
        return True
    return False

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x+50,y+50))

def player(x, y):
    screen.blit(playerImg, (x, y)) # Draws the player

def enemy(x, y):
    screen.blit(enemyImg, (x, y))

def game_over():
    font = pygame.font.SysFont(None, 48)
    gameOverText = font.render('GAME OVER, COSSACKS SLAIN: ' + kills.__str__(), True, (255, 255, 255))
    screen.blit(gameOverText, (400,400))

# Game Loop:
running = True
over = False
while running:
    if(over):
        game_over()
        continue


    screen.fill((0, 75, 0))
    screen.blit(ScoreIMG, (10, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # So that we may close it down.
            running = False

        # KEY Strokes:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and playerY > 0:
                playerY -= 20

            if event.key == pygame.K_DOWN and playerY < 600:
                playerY += 20

            # Bullets:
            if event.key == pygame.K_SPACE:
                fire_bullet(playerX,playerY)
                bulletY = playerY

    enemyY += (enemyY_Change)

    if(enemyY >= 700 or enemyY <= 0):
        enemyX -= enemyX_change
        enemyY_Change = -enemyY_Change

    # Bullet Movement
    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletX += bulletX_change
        screen.blit(pratIMG, (playerX + 150, playerY - 150))

        if speedUp == False:
            if enemyY_Change > 0:
               enemyY_Change += 0.1
            else:
                enemyY_Change -= 0.1

        speedUp = True

        if bulletX > 1000:
            speedUp = False
            bulletX = 0
            bullet_state = "ready"

    # Collision:
    collision = isCollision(enemyX,bulletX,enemyY,bulletY)
    if collision:
        kills += 1
        bulletX = 0
        bullet_state = "ready"
        enemyX = 1000
        textImg = font.render('Cossacks Slain: ' + kills.__str__(), True, (255, 255, 255))

    # Game Over
    if enemyX == 0:
        over = True
        game_over()



    # RGB Values:
    screen.blit(textImg,(120,20))
    player(playerX,playerY)
    enemy(enemyX, enemyY)
    pygame.display.update()