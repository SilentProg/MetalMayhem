import pygame
import os
from modules.const import PATH


class Button(pygame.sprite.Sprite):
    def __init__(self, text="Click", pos=(0, 0), parent_pos=(0, 0), command=lambda: print("No command activated for this button"),
                 auto_size=False, size=(86, 37)):
        super().__init__()
        self.text = text
        self.command = command
        self.parent_pos = parent_pos
        self.font = pygame.font.Font(os.path.join(PATH, 'assets/fonts/PixelifySans-SemiBold.ttf'), 20)
        self.pos = pos
        self.pressed = 0
        self.size = size
        self.text_original_surf = self.font.render(self.text, True, '#664f11')
        self.text_hover_surf = self.font.render(self.text, True, '#caa84f')

        self.original_image = pygame.image.load(os.path.join(PATH, 'assets/images/BTN.png')).convert_alpha()
        self.hover_image = pygame.image.load(os.path.join(PATH, 'assets/images/BTN HOVER.png')).convert_alpha()

        if self.text_original_surf.get_width() + 20 > self.original_image.get_width() and auto_size:
            self.original_image = pygame.transform.scale(self.original_image, (
                self.text_original_surf.get_width() + 40, self.text_original_surf.get_height() + 20))
            self.hover_image = pygame.transform.scale(self.hover_image, (
                self.text_original_surf.get_width() + 40, self.text_original_surf.get_height() + 20))
        elif self.size != (86, 37):
            self.original_image = pygame.transform.scale(self.original_image, self.size)
            self.hover_image = pygame.transform.scale(self.hover_image, self.size)

        self.text_rect = self.text_original_surf.get_rect(
            center=(self.original_image.get_rect().w // 2, self.original_image.get_rect().h // 2))
        self.original_image.blit(self.text_original_surf, self.text_rect)
        self.hover_image.blit(self.text_hover_surf, self.text_rect)

        self.image = self.original_image
        self.rect = self.image.get_rect(topleft=self.pos)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        relative_pos = (mouse_pos[0] - self.parent_pos[0], mouse_pos[1] - self.parent_pos[1])

        if self.rect.collidepoint(relative_pos):
            # pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            self.image = self.hover_image
            self.check_if_click(relative_pos)
        else:
            # pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            self.image = self.original_image

    def check_if_click(self, pos):
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and self.pressed == 1:
                self.command()
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                self.pressed = 0
            if pygame.mouse.get_pressed() == (0, 0, 0):
                self.pressed = 1
