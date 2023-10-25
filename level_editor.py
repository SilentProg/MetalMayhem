import pygame
from modules.const import STEP, PATH, WIDTH, HEIGHT, ROWS, COLS
from modules.button import Button
from modules.menu import Menu

pygame.init()
screen = pygame.display.set_mode((WIDTH + 200, HEIGHT))
pygame.display.set_caption("Metal Mayhem | Lever Editor")
is_running = True


def draw_grid():
    for c in range(COLS + 1):
        pygame.draw.line(screen, 'white', (c * STEP, 0), (c * STEP, HEIGHT))
    for c in range(ROWS + 1):
        pygame.draw.line(screen, 'white', (0, c * STEP), (WIDTH, c * STEP))


menu = Menu("Level Editor", (200, 500), title_size=30)
menu.add_action("Save", on_action=lambda: print('no action'))

while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
            pygame.quit()
            quit(0)

        draw_grid()
        menu.update()
        screen.blit(menu, (0, 0))
        pygame.display.flip()
