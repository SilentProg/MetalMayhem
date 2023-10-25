import pygame
import sys

pygame.init()

# Создание окна
screen_width = 400
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Проверка коллизии между Rect")

# Создание Rect на экране
rect1 = pygame.Rect(0, 0, 50, 50)

# Создание поверхности Surface и Rect на ней
surface = pygame.Surface((100, 100))
surface_rect = surface.get_rect()
rect2 = pygame.Rect(40, 40, 50, 50)

# Цвета
white = (255, 255, 255)
red = (255, 0, 0)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Очистка экрана
    screen.fill(white)

    # Рисование Rect на поверхности
    surface.fill('Black')
    pygame.draw.rect(surface, 'Yellow', rect2)

    # Проверка на коллизию
    if rect1.colliderect(rect2):
        print("Коллизия обнаружена!")

    # Отображение поверхности на экране
    screen.blit(surface, (60, 60))

    # Рисование Rect на экране
    pygame.draw.rect(screen, red, rect1)

    pygame.display.flip()

pygame.quit()
sys.exit()
