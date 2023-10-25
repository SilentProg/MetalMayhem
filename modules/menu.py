import pygame
import os
from modules.button import Button
from modules.const import PATH


class Menu(pygame.Surface):
    def __init__(self, title="Menu", size=(500, 500), title_size: int = 50) -> None:
        super().__init__(size)
        self.title = title
        self.actions = pygame.sprite.Group()
        self.size = size
        self.font = pygame.font.Font(os.path.join(PATH, 'assets/fonts/PixelifySans-SemiBold.ttf'), title_size)

        self.background = pygame.image.load(os.path.join(PATH, 'assets/images/Background.png')).convert_alpha()
        self.background = pygame.transform.scale(self.background, self.size)

        self.__menu_surf: pygame.Surface = pygame.Surface(size=(220, 350))
        self.__menu_rect = self.__menu_surf.get_rect(center=(self.get_rect().centerx, self.get_rect().centery))

        self.__menu_image_top = pygame.image.load(os.path.join(PATH, 'assets/images/BG_TITLE.png')).convert_alpha()
        self.__menu_image_content = pygame.image.load(
            os.path.join(PATH, 'assets/images/BG_CONTENT.png')).convert_alpha()

        self.__menu_top_surf: pygame.Surface = pygame.transform.scale(self.__menu_image_top,
                                                                      (self.__menu_surf.get_width(), 60))
        self.__menu_content_surf: pygame.Surface = pygame.transform.scale(self.__menu_image_content,
                                                                          (self.__menu_surf.get_width(), 300))
        self.__menu_content_rect = self.__menu_content_surf.get_rect()

        self.menu_bg = pygame.image.load(os.path.join(PATH, 'assets/images/BG.png')).convert_alpha()
        self.menu_bg = pygame.transform.scale(self.menu_bg, (220, 350))
        self.menu_bg_rect = self.menu_bg.get_rect()
        self.menu_bg_rect.center = (self.get_rect().centerx, self.get_rect().centery)

        self.title_surf = self.font.render(self.title, True, '#caa84f')
        self.title_rect = self.title_surf.get_rect()
        self.title_rect.center = (self.__menu_top_surf.get_width() // 2, 38)

        self.start_y = 10
        self.start_x = 10

    # def add_action(self, name='Action', on_action=lambda: print('No action')):
    #     action = Button(text=name, pos=(self.start_x, self.start_y), parent_pos=self.menu_bg_rect.topleft, auto_size=False, size=(200, 50), command=on_action)
    #     self.start_y += action.rect.h+10
    #     self.actions.add(action)

    def add_action(self, name='Action', on_action=lambda: print('No action')):
        action = Button(text=name, pos=(self.start_x, self.start_y),
                        parent_pos=(self.__menu_rect.x, self.__menu_rect.y+60), auto_size=False, size=(200, 50),
                        command=on_action)
        self.start_y += action.rect.h + 10
        self.actions.add(action)

    def update(self):
        self.blit(self.background, (0, 0))

        mouse_pos = pygame.mouse.get_pos()


        self.__menu_surf: pygame.Surface = pygame.Surface(size=(220, len(self.actions.sprites())*65+60))
        self.__menu_rect = self.__menu_surf.get_rect(center=(self.get_rect().centerx, self.get_rect().centery))

        self.__menu_top_surf.blit(self.title_surf, self.title_rect)

        self.__menu_content_surf = pygame.transform.scale(self.__menu_image_content, (self.__menu_surf.get_width(), len(self.actions.sprites())*65))
        self.__menu_content_rect = self.__menu_content_surf.get_rect()

        self.actions.update()
        self.actions.draw(self.__menu_content_surf)

        self.__menu_surf.blit(self.__menu_top_surf, (0, 0))
        self.__menu_surf.blit(self.__menu_content_surf, (0, 60))

        self.blit(self.__menu_surf, self.__menu_rect)

        relative_pos = (mouse_pos[0] - self.__menu_rect.x, mouse_pos[1] - self.__menu_rect.y - 60)
        for action in self.actions:
            if action.rect.collidepoint(relative_pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                break
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        #
        # self.blit(self.background, (0, 0))
        #
        # self.menu_bg.blit(self.title_surf, self.title_rect)
        #
        # self.blit(self.menu_bg, self.menu_bg_rect)
        #
        # self.actions.draw(self.menu_bg)
        # self.actions.update()
