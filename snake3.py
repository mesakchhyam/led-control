import pygame
import random
import time

# Initialize pygame
pygame.init()

# Screen dimensions
screen_width = 600
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Snake attributes
snake_size = 10
speed = 8  # Reduced speed for a slower snake

# Font for score and game over text
font = pygame.font.Font(None, 30)
large_font = pygame.font.Font(None, 50)

# Function to start a new game
def new_game():
    # Snake initial position and attributes
    snake = [(100, 50)]
    snake_dir = "RIGHT"
    change_to = snake_dir
    score = 0

    # Food attributes
    food_x = random.randrange(0, screen_width - snake_size, 10)
    food_y = random.randrange(0, screen_height - snake_size, 10)
    food = (food_x, food_y)

    return snake, snake_dir, change_to, score, food

# Countdown before game starts
for i in range(3, 0, -1):
    screen.fill(BLACK)
    countdown_text = large_font.render(f"Starting in {i}", True, WHITE)
    screen.blit(countdown_text, (screen_width // 2 - 80, screen_height // 2 - 20))
    pygame.display.flip()
    time.sleep(1)

# Main loop
running = True
clock = pygame.time.Clock()

# Initial game state
snake, snake_dir, change_to, score, food = new_game()

while running:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_dir != "DOWN":
                change_to = "UP"
            elif event.key == pygame.K_DOWN and snake_dir != "UP":
                change_to = "DOWN"
            elif event.key == pygame.K_LEFT and snake_dir != "RIGHT":
                change_to = "LEFT"
            elif event.key == pygame.K_RIGHT and snake_dir != "LEFT":
                change_to = "RIGHT"

    # Update direction
    snake_dir = change_to

    # Move the snake
    if snake_dir == "UP":
        new_head = (snake[0][0], snake[0][1] - snake_size)
    elif snake_dir == "DOWN":
        new_head = (snake[0][0], snake[0][1] + snake_size)
    elif snake_dir == "LEFT":
        new_head = (snake[0][0] - snake_size, snake[0][1])
    elif snake_dir == "RIGHT":
        new_head = (snake[0][0] + snake_size, snake[0][1])

    # Check for collisions
    if (
        new_head[0] < 0 or new_head[0] >= screen_width or
        new_head[1] < 0 or new_head[1] >= screen_height or
        new_head in snake
    ):
        # Game over: show option for new game
        screen.fill(BLACK)
        game_over_text = large_font.render("GAME OVER", True, RED)
        score_text = font.render(f"Final Score: {score}", True, WHITE)
        new_game_text = font.render("Press 'N' for New Game", True, WHITE)
        screen.blit(game_over_text, (screen_width // 2 - 100, screen_height // 2 - 40))
        screen.blit(score_text, (screen_width // 2 - 70, screen_height // 2 + 10))
        screen.blit(new_game_text, (screen_width // 2 - 120, screen_height // 2 + 50))
        pygame.display.flip()

        # Wait for 'N' key press to restart or quit
        waiting_for_restart = True
        while waiting_for_restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting_for_restart = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        # Start new game
                        snake, snake_dir, change_to, score, food = new_game()
                        waiting_for_restart = False
                    elif event.key == pygame.K_q:
                        # Quit game
                        running = False
                        waiting_for_restart = False

        continue

    # Add new head and remove tail unless food is eaten
    snake.insert(0, new_head)
    if new_head == food:
        score += 1
        food_x = random.randrange(0, screen_width - snake_size, 10)
        food_y = random.randrange(0, screen_height - snake_size, 10)
        food = (food_x, food_y)
    else:
        snake.pop()

    # Draw food
    pygame.draw.rect(screen, RED, (food[0], food[1], snake_size, snake_size))

    # Draw snake
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], snake_size, snake_size))

    # Display score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Refresh screen
    pygame.display.flip()
    clock.tick(speed)  # Reduced speed to slow down the snake

# Quit pygame
pygame.quit()
