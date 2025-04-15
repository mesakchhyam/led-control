import pygame
import random
import time
# Initialize the pygame
pygame.init()
# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
# Gun attributes
gun_width = 50
gun_height = 20
gun_x = screen_width // 2
gun_speed = 20
gun_smooth_speed = 0
# Falling object attributes
object_width = 40
object_height = 40
falling_objects = []
fall_speed = 1.5
# Laser attributes (boxes)
laser_width = 15
laser_height = 15
lasers = []
laser_speed = 12
# Game loop flag
running = True
game_over = False
score = 0
last_shot_time = 0
shot_delay = 0.06  # 0.06 seconds
# Font
font = pygame.font.Font(None, 36)
# Countdown
countdown_time = 3
countdown_start_time = time.time()
# Create falling objects
def create_falling_object():
    x = random.randint(0, screen_width - object_width)
    y = -object_height
    falling_objects.append(pygame.Rect(x, y, object_width, object_height))
# Draw gun
def draw_gun():
    pygame.draw.rect(screen, WHITE, pygame.Rect(gun_x, screen_height - gun_height, gun_width, gun_height))
# Draw lasers (boxes)
def draw_lasers():
    for laser in lasers:
        pygame.draw.rect(screen, RED, laser)
# Draw falling objects
def draw_falling_objects():
    for obj in falling_objects:
        pygame.draw.rect(screen, WHITE, obj)
# Handle collisions
def check_collisions():
    global falling_objects, lasers, score
    for laser in lasers[:]:
        for obj in falling_objects[:]:
            if laser.colliderect(obj):
                falling_objects.remove(obj)
                lasers.remove(laser)
                score += 1
                break

# Game loop
while running:
    screen.fill(BLACK)

    if time.time() - countdown_start_time < countdown_time:
        countdown = countdown_time - int(time.time() - countdown_start_time)
        text = font.render(f"Starting in {countdown}", True, WHITE)
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.Clock().tick(60)
        continue

    if game_over:
        text = font.render("Game Over!", True, RED)
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.Clock().tick(60)
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        gun_smooth_speed = -gun_speed
    elif keys[pygame.K_RIGHT]:
        gun_smooth_speed = gun_speed
    else:
        gun_smooth_speed = 0

    gun_x += gun_smooth_speed
    gun_x = max(0, min(gun_x, screen_width - gun_width))

    current_time = time.time()
    if current_time - last_shot_time >= shot_delay:
        laser = pygame.Rect(gun_x + gun_width // 2 - laser_width // 2, screen_height - gun_height - laser_height, laser_width, laser_height)
        lasers.append(laser)
        last_shot_time = current_time

    for laser in lasers[:]:
        laser.y -= laser_speed
        if laser.y < 0:
            lasers.remove(laser)

    for obj in falling_objects[:]:
        obj.y += fall_speed
        if obj.y > screen_height:
            falling_objects.remove(obj)
            game_over = True
            break

    if random.randint(1, 100) <= 2:
        create_falling_object()

    check_collisions()

    draw_falling_objects()
    draw_gun()
    draw_lasers()

    # Score display
    score_text = font.render(f"Kills: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()