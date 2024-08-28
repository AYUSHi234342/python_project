import pygame
import random
import math

# Initialize pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Invader Game")

# Load images and sounds
icon_path = r"C:\Users\Ayushi\Downloads\spaceship.png"
background_music_path = r"C:\Users\Ayushi\Downloads\background.wav"
bullet_sound_path = r"C:\Users\Ayushi\Downloads\explosion.wav"
background_image_path = r"C:\Users\Ayushi\Downloads\background1.png"
playerImg_path = r"C:\Users\Ayushi\Downloads\player.png"
enemyImg_paths = [r"C:\Users\Ayushi\Downloads\play.png"] * 6
bulletImg_path = r"C:\Users\Ayushi\Downloads\bullet.png"

# Load assets
try:
    icon = pygame.image.load(icon_path)
    pygame.display.set_icon(icon)
except pygame.error as e:
    print("Error loading spaceship icon:", e)

try:
    pygame.mixer.music.load(background_music_path)
    pygame.mixer.music.play(-1)
    bullet_sound = pygame.mixer.Sound(bullet_sound_path)
except pygame.error as e:
    print("Error loading sounds:", e)

try:
    backg = pygame.image.load(background_image_path)
    playerImg = pygame.image.load(playerImg_path)
    bulletImg = pygame.image.load(bulletImg_path)
    enemyImg = [pygame.image.load(path) for path in enemyImg_paths]
except pygame.error as e:
    print("Error loading images:", e)

# Player attributes
playerX = 370
playerY = 480
player_speed = 5

# Enemy attributes
no_of_enemy = 6
enemyX = [random.randint(0, 763) for _ in range(no_of_enemy)]
enemyY = [random.randint(50, 150) for _ in range(no_of_enemy)]
enemyX_change = [4] * no_of_enemy
enemyY_change = [48] * no_of_enemy

# Bullet attributes
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score and font
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Difficulty settings
base_speed = 4
speed_increase_per_score = 1

def player(x, y):
    gameWindow.blit(playerImg, (x, y))

def enemy(x, y, i):
    gameWindow.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    gameWindow.blit(bulletImg, (x + 16, y + 12))
    bullet_sound.play()

def testCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    return distance < 27

def show_score(x, y):
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    gameWindow.blit(score_text, (x, y))

def game_over():
    text = font.render("Game Over", True, (255, 255, 255))
    gameWindow.blit(text, (200, 250))

def start_menu():
    menu = True
    while menu:
        gameWindow.fill((0, 0, 0))
        title_font = pygame.font.Font('freesansbold.ttf', 64)
        title = title_font.render("Space Invader", True, (255, 255, 255))
        gameWindow.blit(title, (150, 150))
        
        subtitle_font = pygame.font.Font('freesansbold.ttf', 32)
        subtitle = subtitle_font.render("Press ENTER to Start", True, (255, 255, 255))
        gameWindow.blit(subtitle, (230, 250))
        
        instructions_font = pygame.font.Font('freesansbold.ttf', 24)
        instructions = instructions_font.render("Press Q to Quit", True, (255, 255, 255))
        gameWindow.blit(instructions, (320, 300))
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    menu = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()

start_menu()

playerX_change = 0
closewindow = False
white = (255, 255, 255)

while not closewindow:
    gameWindow.fill(white)
    gameWindow.blit(backg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            closewindow = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -player_speed
            if event.key == pygame.K_RIGHT:
                playerX_change = player_speed
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    playerX = max(0, min(playerX, 736))

    # Enemy movement and collision
    game_over_flag = False
    for i in range(no_of_enemy):
        current_speed = base_speed + (score // 10) * speed_increase_per_score
        enemyX[i] += current_speed if enemyX_change[i] > 0 else -current_speed
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        if enemyY[i] > 440:
            game_over_flag = True
            break

        collision = testCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

    if game_over_flag:
        for j in range(no_of_enemy):
            enemyY[j] = 20000
        game_over()
        pygame.display.update()
        pygame.time.delay(500)
        pygame.quit()
        exit()

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)

    for i in range(no_of_enemy):
        enemy(enemyX[i], enemyY[i], i)

    show_score(textX, textY)
    pygame.display.update()
