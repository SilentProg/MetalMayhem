import pygame
import os
from modules.button import Button
from modules.const import PATH

class Menu(pygame.Surface):
    def __init__(self, title="Menu", size=(500, 500)) -> None:
        super().__init__(size)
        self.title = title
        self.actions = pygame.sprite.Group()
        self.size = size
        self.font = pygame.font.Font(os.path.join(PATH, 'assets/fonts/PixelifySans-SemiBold.ttf'), 50)

        self.background = pygame.image.load(os.path.join(PATH, 'assets/images/Background.png')).convert_alpha()
        self.background = pygame.transform.scale(self.background, self.size)

        self.menu_bg = pygame.image.load(os.path.join(PATH, 'assets/images/BG.png')).convert_alpha()
        self.menu_bg = pygame.transform.scale(self.menu_bg, (220, 350))
        self.menu_bg_rect = self.menu_bg.get_rect()
        self.menu_bg_rect.center = (self.get_rect().centerx, self.get_rect().centery)

        self.title_surf = self.font.render(self.title, True, '#caa84f')
        self.title_rect = self.title_surf.get_rect()
        self.title_rect.center = (self.menu_bg.get_width()//2, 38)

        self.start_y = 80
        self.start_x = 10

    def add_action(self, name='Action', on_action=lambda: print('No action')):
        action = Button(text=name, pos=(self.start_x, self.start_y), parent_pos=self.menu_bg_rect.topleft, auto_size=False, size=(200, 50), command=on_action)
        self.start_y += action.rect.h+10
        self.actions.add(action)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        relative_pos = (mouse_pos[0] - self.menu_bg_rect.x, mouse_pos[1] - self.menu_bg_rect.y)
        for action in self.actions:
            if action.rect.collidepoint(relative_pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                break
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        self.blit(self.background, (0, 0))

        self.menu_bg.blit(self.title_surf, self.title_rect)

        self.blit(self.menu_bg, self.menu_bg_rect)

        self.actions.draw(self.menu_bg)
        self.actions.update()


