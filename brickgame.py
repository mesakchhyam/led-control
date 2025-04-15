import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 500, 600
BLOCK_SIZE = 30
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Irregular Brick Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]

# Define clock
clock = pygame.time.Clock()
FPS = 30  # Increase FPS for smooth movement

# Define irregular block shapes
SHAPES = [
    [(0, 0), (1, 0), (1, 1), (2, 1)],  # L-shape
    [(0, 0), (0, 1), (1, 1), (1, 2)],  # Z-shape
    [(0, 0), (1, 0), (1, 1), (1, 2)],  # T-shape
    [(0, 0), (1, 0), (0, 1), (1, 1)],  # Square
]

# Game settings
fall_delay = 15  # Delay before falling (higher = slower fall)
move_speed = 5   # Left-right movement speed

def generate_block():
    shape = random.choice(SHAPES)
    color = random.choice(COLORS)
    return {'shape': shape, 'x': WIDTH // (2 * BLOCK_SIZE), 'y': 0, 'color': color}

def collision_check(block, placed_blocks):
    """Check if the block collides with placed blocks or the bottom."""
    for x_offset, y_offset in block['shape']:
        new_x = block['x'] + x_offset
        new_y = block['y'] + y_offset

        # Check bottom boundary
        if new_y * BLOCK_SIZE >= HEIGHT:
            return True
        
        # Check collision with placed blocks
        for placed_block in placed_blocks:
            for px_offset, py_offset in placed_block['shape']:
                if new_x == placed_block['x'] + px_offset and new_y == placed_block['y'] + py_offset:
                    return True
    return False

# Game variables
falling_block = generate_block()
placed_blocks = []
fall_counter = 0  # Control fall speed

# Main game loop
running = True
while running:
    screen.fill(BLACK)
    keys = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Faster left-right movement
    if keys[pygame.K_LEFT] and falling_block['x'] > 0:
        falling_block['x'] -= 1
        pygame.time.delay(move_speed)
    if keys[pygame.K_RIGHT] and falling_block['x'] < (WIDTH // BLOCK_SIZE) - 2:
        falling_block['x'] += 1
        pygame.time.delay(move_speed)
    if keys[pygame.K_DOWN]:
        falling_block['y'] += 1  # Faster downward movement
    if keys[pygame.K_SPACE]:
        if not collision_check(falling_block, placed_blocks):
            placed_blocks.append(falling_block)
            falling_block = generate_block()

    # Control falling speed
    fall_counter += 1
    if fall_counter >= fall_delay:
        fall_counter = 0
        falling_block['y'] += 1
        if collision_check(falling_block, placed_blocks):
            falling_block['y'] -= 1
            placed_blocks.append(falling_block)
            falling_block = generate_block()

    # Draw falling block
    for x_offset, y_offset in falling_block['shape']:
        pygame.draw.rect(screen, falling_block['color'], ((falling_block['x'] + x_offset) * BLOCK_SIZE, (falling_block['y'] + y_offset) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    
    # Draw placed blocks
    for block in placed_blocks:
        for x_offset, y_offset in block['shape']:
            pygame.draw.rect(screen, block['color'], ((block['x'] + x_offset) * BLOCK_SIZE, (block['y'] + y_offset) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

