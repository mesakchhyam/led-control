import pygame
import time

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Runner")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Set up fonts
font = pygame.font.SysFont("Arial", 20)

# Maze layout (1 = wall, 0 = path, 2 = player, 3 = exit, 4 = entry)
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 1, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Player initial position
player_x, player_y = 1, 1

# Entry and Exit positions
entry_x, entry_y = 1, 1  # Mark the entry point (top-left)
exit_x, exit_y = 8, 8     # Mark the exit point (bottom-right)

# Player movement
def draw_maze():
    block_size = 50
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            rect = pygame.Rect(col * block_size, row * block_size, block_size, block_size)
            if maze[row][col] == 1:  # wall
                pygame.draw.rect(screen, BLACK, rect)
            elif maze[row][col] == 0:  # path
                pygame.draw.rect(screen, WHITE, rect)
            elif maze[row][col] == 2:  # player
                pygame.draw.rect(screen, GREEN, rect)
            elif maze[row][col] == 3:  # exit
                pygame.draw.rect(screen, RED, rect)
            elif maze[row][col] == 4:  # entry
                pygame.draw.rect(screen, YELLOW, rect)  # Entry point is marked with yellow

def move_player(dx, dy):
    global player_x, player_y
    if maze[player_y + dy][player_x + dx] != 1:
        player_x += dx
        player_y += dy

def countdown():
    font_big = pygame.font.SysFont("Arial", 60)
    for i in range(3, 0, -1):
        screen.fill(WHITE)
        text = font_big.render(str(i), True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.update()
        time.sleep(1)

def main():
    global player_x, player_y

    # Show countdown before the game starts
    countdown()

    # Main game loop
    running = True
    while running:
        screen.fill(WHITE)
        draw_maze()

        # Draw the player at the current position
        maze[player_y][player_x] = 2
        maze[exit_y][exit_x] = 3
        maze[entry_y][entry_x] = 4  # Keep the entry point yellow

        # Check if player reached the exit
        if player_x == exit_x and player_y == exit_y:
            text = font.render("You Win!", True, GREEN)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
            pygame.display.update()
            pygame.time.wait(2000)
            running = False

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_player(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    move_player(1, 0)
                elif event.key == pygame.K_UP:
                    move_player(0, -1)
                elif event.key == pygame.K_DOWN:
                    move_player(0, 1)

        pygame.display.update()

    # Game Over message after player wins or exits
    screen.fill(WHITE)
    text = font.render("Game Over! Press Q to Quit", True, BLACK)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()

    # Wait for the user to press 'Q' to quit the game
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                waiting = False

    pygame.quit()

if __name__ == "__main__":
    main()
