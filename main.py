import pygame
import random
import os
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT, MOUSEBUTTONDOWN


pygame.init()

FPS = pygame.time.Clock()

# Разрешение экрана
HEIGHT = 800
WIDTH = 1200
main_display = pygame.display.set_mode((WIDTH, HEIGHT))

# Фон
bg = pygame.transform.scale(pygame.image.load('background.png'), (WIDTH, HEIGHT))
bg_X1 = 0 
bg_X2 = bg.get_width()
bg_move = 3

IMG_PATH = "Goose-animation"
PLAYER_IMAGES = os.listdir(IMG_PATH)

# Счёт
FONT = pygame.font.SysFont('Verdana', 20)
score = 0

# Цвета
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_GREEN = (0, 255, 0)

# Игрок
player = pygame.image.load('player.png').convert_alpha()
player_rect = player.get_rect(center=(WIDTH // 2, HEIGHT // 2))
player_move_down = [0, 4]
player_move_right = [4, 0]
player_move_top = [0, -4]
player_move_left = [-4, 0]
# Анимация игрока
image_index = 0
CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 200)

# Враги
def create_enemy():
    enemy = pygame.image.load('enemy.png').convert_alpha()
    enemy_rect = pygame.Rect(WIDTH, random.randint(HEIGHT // 4, 3 * HEIGHT // 4), enemy.get_width(), enemy.get_height())
    enemy_move = [random.randint(-6, -1), 0]
    return [enemy, enemy_rect, enemy_move]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

# Бонусы
def create_bonus():
    bonus = pygame.image.load('bonus.png').convert_alpha()
    bonus_rect = pygame.Rect(random.randint(WIDTH // 4, 3 * WIDTH // 4), 0, bonus.get_width(), bonus.get_height())
    bonus_move = [0, random.randint(4, 8)]
    return [bonus, bonus_rect, bonus_move]

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 3000)

# Звуки
hit_sound = pygame.mixer.Sound('Bang-sound.mp3')
bonus_sound = pygame.mixer.Sound('Bonus-sound.mp3')

# Изображение для экрана перезапуска
game_over_image = pygame.image.load('game_over.png').convert_alpha()
game_over_rect = game_over_image.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))

restart_arrow = pygame.image.load('restart_arrow.png').convert_alpha()
restart_arrow_rect = restart_arrow.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

def reset_game():
    global player_rect, enemies, bonuses, score, playing
    player_rect = player.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    enemies = []
    bonuses = []
    score = 0
    playing = True

enemies = []
bonuses = []

# Настройка ФПС
playing = True
game_over = False

while True:
    FPS.tick(120)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CHANGE_IMAGE:
            player = pygame.image.load(os.path.join(IMG_PATH, PLAYER_IMAGES[image_index])).convert_alpha()
            image_index += 1
            if image_index >= len(PLAYER_IMAGES):
                image_index = 0
        if event.type == MOUSEBUTTONDOWN and game_over:
            if restart_arrow_rect.collidepoint(event.pos):
                game_over = False
                reset_game()

    if playing:
        bg_X1 -= bg_move
        bg_X2 -= bg_move
        
        if bg_X1 < -bg.get_width():
            bg_X1 = bg.get_width()
        if bg_X2 < -bg.get_width():
            bg_X2 = bg.get_width()

        main_display.blit(bg, (bg_X1, 0))
        main_display.blit(bg, (bg_X2, 0))

        keys = pygame.key.get_pressed()

        if keys[K_DOWN] and player_rect.bottom < HEIGHT:
            player_rect = player_rect.move(player_move_down)
        if keys[K_RIGHT] and player_rect.right < WIDTH:
            player_rect = player_rect.move(player_move_right)
        if keys[K_UP] and player_rect.top > 0:
            player_rect = player_rect.move(player_move_top)
        if keys[K_LEFT] and player_rect.left > 0:
            player_rect = player_rect.move(player_move_left)

        for enemy in enemies:
            enemy[1] = enemy[1].move(enemy[2])
            main_display.blit(enemy[0], enemy[1])
            if enemy[1].left < 0:
                enemies.remove(enemy)
            if player_rect.colliderect(enemy[1]):
                hit_sound.play()
                playing = False
                game_over = True

        for bonus in bonuses:
            bonus[1] = bonus[1].move(bonus[2])
            main_display.blit(bonus[0], bonus[1])
            if bonus[1].top > HEIGHT:
                bonuses.remove(bonus)
            if player_rect.colliderect(bonus[1]):
                bonus_sound.play()
                score += 1
                bonuses.remove(bonus)

        main_display.blit(FONT.render(str(score), True, COLOR_WHITE), (WIDTH - 50, 20))
        main_display.blit(player, player_rect)
    else:
        main_display.blit(game_over_image, game_over_rect)
        main_display.blit(restart_arrow, restart_arrow_rect)

    pygame.display.flip()
