import pygame
import random
import math
from pygame import mixer

# Initialising pygame
pygame.init()

# Creating screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('images/background.jpg')

# Background Sound
mixer.music.load('musics/background.wav')
mixer.music.play(-1)

# Title and icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('images/alien.png')
pygame.display.set_icon(icon)

# Player Position and Image
playerImg = pygame.image.load('images/space-invaders.png')
playerX = 370
playerY = 480
playerX_change = 0


def player(x, y):
    screen.blit(playerImg, (x, y))


# Enemy Position and Image
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 6

for i in range(no_of_enemies):
    enemyImg.append(pygame.image.load('images/monster.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(0, 50))
    enemyX_change.append(3.5)
    enemyY_change.append(40)


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# Bullet Position and Image
bulletImg = pygame.image.load('images/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 5
bullet_state = 'ready'
bullet_initial = 0


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fired'
    screen.blit(bulletImg, (x+16, y+10))


# Collision
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) +
                         math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


# Score
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game Ove text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    display_score = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(display_score, (x, y))


def game_over_text():
    over_text = over_font.render(f'GAME OVER', True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


# Game Loop
running = True
while running:

    # Background Color
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # If keystroke is pressed check right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound = mixer.Sound('musics/laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    enemyX += enemyX_change

    # Player boundary
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movment
    for i in range(no_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(no_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 3.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -3.5
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('musics/explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = 'ready'
            score += 10
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(0, 50)

        enemy(int(enemyX[i]), int(enemyY[i]), i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'

    if bullet_state == 'fired':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(int(playerX), int(playerY))
    show_score(textX, textY)
    pygame.display.update()
