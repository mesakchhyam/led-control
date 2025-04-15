import pygame
import cv2
import mediapipe as mp
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gesture Table Tennis")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)  # Blue color for the ball

# Game elements
paddle_width, paddle_height = 10, 100
ball_size = 10
table_width, table_height = WIDTH, HEIGHT // 2
net_width = 10

# Paddles
player_paddle = pygame.Rect(50, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)
computer_paddle = pygame.Rect(WIDTH - 50 - paddle_width, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)

# Ball
ball = pygame.Rect(WIDTH // 2 - ball_size // 2, HEIGHT // 2 - ball_size // 2, ball_size, ball_size)
ball_speed = [5, 5]  # Initial ball speed (horizontal and vertical)

# Table and net
table = pygame.Rect(0, HEIGHT // 2 - table_height // 2, table_width, table_height)
net = pygame.Rect(WIDTH // 2 - net_width // 2, HEIGHT // 2 - table_height // 2, net_width, table_height)

# Computer AI
computer_speed = 3

# Scoreboard variables
player_score = 0
computer_score = 0

# Mediapipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Camera setup
cap = cv2.VideoCapture(0)

# Font for score display
font = pygame.font.SysFont("Arial", 30)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Capture hand gestures
    ret, frame = cap.read()
    if not ret:
        continue

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get the y-coordinate of the index finger tip
            y_coord = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * HEIGHT)
            player_paddle.centery = y_coord
            player_paddle.centery = max(paddle_height // 2, min(player_paddle.centery, HEIGHT // 2 + table_height // 2 - paddle_height // 2))

            # Draw hand landmarks on the frame
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Computer AI
    if computer_paddle.centery < ball.centery:
        computer_paddle.centery += computer_speed
    elif computer_paddle.centery > ball.centery:
        computer_paddle.centery -= computer_speed
    computer_paddle.centery = max(HEIGHT // 2 - table_height // 2 + paddle_height // 2, min(computer_paddle.centery, HEIGHT - paddle_height // 2))

    # Ball movement
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    # Ball collisions with top and bottom walls
    if ball.top <= HEIGHT // 2 - table_height // 2 or ball.bottom >= HEIGHT // 2 + table_height // 2:
        ball_speed[1] *= -1  # Reverse vertical direction

    # Ball collisions with paddles
    if ball.colliderect(player_paddle) or ball.colliderect(computer_paddle):
        ball_speed[0] *= -1  # Reverse horizontal direction
        ball_speed[1] += random.uniform(-1, 1)  # Slight variation in vertical speed

    # Ball out of bounds (Player's side)
    if ball.left <= 0:
        # Reset ball to center and give it a direction towards the computer side
        ball.center = (WIDTH // 2, HEIGHT // 2)
        ball_speed[0] = random.choice([5, -5])  # Random horizontal direction
        ball_speed[1] = random.choice([5, -5])  # Random vertical direction
        computer_score += 1  # Computer scores

    # Ball out of bounds (Computer's side)
    if ball.right >= WIDTH:
        # Reset ball to center and give it a direction towards the player side
        ball.center = (WIDTH // 2, HEIGHT // 2)
        ball_speed[0] = random.choice([5, -5])  # Random horizontal direction
        ball_speed[1] = random.choice([5, -5])  # Random vertical direction
        player_score += 1  # Player scores

    # Ball collision with the net
    if ball.colliderect(net):
        if ball_speed[0] > 0 and ball.right <= net.left:  # Ball is coming from left
            ball.right = net.left  # Ensure ball moves left if coming from right
            ball_speed[0] *= -1  # Reverse horizontal direction
        elif ball_speed[0] < 0 and ball.left >= net.right:  # Ball is coming from right
            ball.left = net.right  # Ensure ball moves right if coming from left
            ball_speed[0] *= -1  # Reverse horizontal direction

    # Drawing
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, table)
    pygame.draw.rect(screen, RED, net)
    pygame.draw.rect(screen, GREEN, player_paddle)
    pygame.draw.rect(screen, GREEN, computer_paddle)
    pygame.draw.ellipse(screen, BLUE, ball)  # Ball color updated to blue

    # Display scores
    player_score_text = font.render(f"Player: {player_score}", True, WHITE)
    computer_score_text = font.render(f"Computer: {computer_score}", True, WHITE)
    screen.blit(player_score_text, (WIDTH // 4 - player_score_text.get_width() // 2, 20))
    screen.blit(computer_score_text, (3 * WIDTH // 4 - computer_score_text.get_width() // 2, 20))

    pygame.display.flip()

    cv2.imshow("Hand Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
pygame.quit()
