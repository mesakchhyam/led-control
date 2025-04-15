import pygame
import random
import time
# Initialize pygame
pygame.init()
# Set up the game window
width, height = 400, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Car Avoidance Game")
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
# Set up the car
car_width = 50
car_height = 60
car_x = width // 2 - car_width // 2
car_y = height - car_height - 10
car_velocity = 5
# Set up the obstacles
obstacle_width = 50
obstacle_height = 50
obstacle_velocity = 5
obstacle_frequency = 30  # Higher means fewer obstacles
obstacles = []
# Game loop flag
running = True
clock = pygame.time.Clock()
# Font for messages
font = pygame.font.Font(None, 50)
def show_message(text, duration=2):
    """Displays a message at the center of the screen for a given duration."""
    screen.fill(BLACK)
    message = font.render(text, True, WHITE)
    text_rect = message.get_rect(center=(width // 2, height // 2))
    screen.blit(message, text_rect)
    pygame.display.update()
    time.sleep(duration)
# Countdown before the game starts
for i in range(3, 0, -1):
    show_message(str(i), 1)
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get keys pressed for car movement
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP] and car_y > 0:
        car_y -= car_velocity
    if keys[pygame.K_DOWN] and car_y < height - car_height:
        car_y += car_velocity
    if keys[pygame.K_LEFT] and car_x > 0:
        car_x -= car_velocity
    if keys[pygame.K_RIGHT] and car_x < width - car_width:
        car_x += car_velocity

    # Create obstacles
    if random.randint(1, obstacle_frequency) == 1:
        obstacle_x = random.randint(0, width - obstacle_width)
        obstacles.append([obstacle_x, -obstacle_height])

    # Move obstacles
    for obstacle in obstacles[:]:
        obstacle[1] += obstacle_velocity
        if obstacle[1] > height:
            obstacles.remove(obstacle)

    # Check for collisions
    car_rect = pygame.Rect(car_x, car_y, car_width, car_height)
    for obstacle in obstacles:
        obstacle_rect = pygame.Rect(obstacle[0], obstacle[1], obstacle_width, obstacle_height)
        if car_rect.colliderect(obstacle_rect):
            show_message("Game Over", 2)  # Show Game Over message
            running = False  # Exit game loop

    # Draw the car
    pygame.draw.rect(screen, GREEN, (car_x, car_y, car_width, car_height))

    # Draw obstacles
    for obstacle in obstacles:
        pygame.draw.rect(screen, RED, (obstacle[0], obstacle[1], obstacle_width, obstacle_height))

    pygame.display.update()

    # Set frames per second
    clock.tick(60)
pygame.quit()
