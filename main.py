import os

import pygame
from modules.button import Button
from modules.menu import Menu
from modules.const import PATH, SCREEN_SIZE, WIDTH, HEIGHT


class Game:
    def __init__(self):
        pygame.init()
        self.is_running = True
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption('Metal Mayhem: Tanktopia64 2D')
        self.pygame_icon = pygame.image.load(os.path.join(PATH, 'assets/images/favicon.png')).convert_alpha()
        self.pygame_icon_transformed = pygame.transform.scale(self.pygame_icon, (200, 200))
        self.pygame_icon_transformed_rect = self.pygame_icon_transformed.get_rect(midright=(WIDTH-100, HEIGHT//2))
        pygame.display.set_icon(self.pygame_icon)
        self.clock = pygame.time.Clock()

    def exit_game(self):
        self.is_running = False

    def play(self):
        menu = Menu(size=(WIDTH, HEIGHT))
        menu.add_action('1 Player')
        menu.add_action('2 Player')
        menu.add_action('Settings')
        menu.add_action('Creators')
        menu.add_action('Exit', on_action=self.exit_game)

        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

            menu.update()
            menu.background.blit(self.pygame_icon_transformed, self.pygame_icon_transformed_rect)
            self.screen.blit(menu, (0, 0))

            pygame.display.update()
            self.clock.tick(60)


def main():
    game = Game()
    game.play()


if __name__ == "__main__":
    main()
