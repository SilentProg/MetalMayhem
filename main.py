import os

import pygame
from modules.button import Button
from modules.menu import Menu
from modules.const import PATH
screen = pygame.display.set_mode((800, 600))
buttons = pygame.sprite.Group()





if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption('Example of button')
    screen = pygame.display.set_mode((1000, 800))
    clock = pygame.time.Clock()


    # b1 = Button("CLICK ME", pos=(100, 100), command=lambda: print("clicked right now 1"), auto_size=True)
    # b2 = Button("CLICK ME 2", pos=(100, 150), command=lambda: print("clicked right now 2"), auto_size=True)
    # b3 = Button("CLICK ME 3", pos=(100, 200), command=lambda: print("clicked right now 3"), auto_size=True)
    # buttons.add(b1)
    # buttons.add(b2)
    # buttons.add(b3)
    menu = Menu(size=(1000, 800))
    menu.add_action('1 Player')
    menu.add_action('2 Player')
    menu.add_action('Settings')
    menu.add_action('Exit')

    is_running = True
    while is_running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False


        # to show buttons created

        screen.blit(menu, (0, 0))
        menu.update()
        buttons.draw(screen)
        buttons.update()

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

# def main():
#     print("main")
#
#
# if __name__ == '__main__':
#     main()
