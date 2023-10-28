import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rectangle Collision")

# Player rectangle
player_width, player_height = 50, 50
player_x, player_y = 10, 10
player_speed = 5
player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

# Obstacle rectangle
obstacle_width, obstacle_height = 100, 100
obstacle_x, obstacle_y = 400, 300
obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height)

clock = pygame.time.Clock()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle player input

    old_x = player_rect.x
    old_y = player_rect.y

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_rect.y -= player_speed
    if keys[pygame.K_s]:
        player_rect.y += player_speed
    if keys[pygame.K_a]:
        player_rect.x -= player_speed
    if keys[pygame.K_d]:
        player_rect.x += player_speed

    # Collision detection
    if player_rect.colliderect(obstacle_rect):
        player_rect.y = old_y
        player_rect.x = old_x
        print("collide")

    # Clear the screen
    screen.fill(WHITE)

    # Draw the player and obstacle rectangles
    pygame.draw.rect(screen, RED, player_rect)
    pygame.draw.rect(screen, RED, obstacle_rect)

    # Update the display
    pygame.display.update()
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
