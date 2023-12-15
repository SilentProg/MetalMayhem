import os

import pygame
from tkinter import messagebox

from modules.mapsetting import Block, map
from modules.menu import Menu
from modules.button import Button
from modules.const import PATH, SCREEN_SIZE, WIDTH, HEIGHT, NUMBERS_PLAYER, STEP, COLS, ROWS
from modules.tank import Tank


class Game:
    def __init__(self):
        pygame.init()
        self.is_running = True
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption('Metal Mayhem: Tanktopia64 2D')
        self.pygame_icon = pygame.image.load(os.path.join(PATH, 'assets/images/favicon.png')).convert_alpha()
        pygame.display.set_icon(self.pygame_icon)
        self.clock = pygame.time.Clock()
        self.stage = 0
        self.winner = None
        # Backgrounds
        self.main_bg = pygame.transform.scale(
            pygame.image.load(os.path.join(PATH, 'assets/images/Background.png')).convert_alpha(), SCREEN_SIZE)
        # Fonts
        self.font40 = pygame.font.Font(os.path.join(PATH, 'assets/fonts/PixelifySans-Medium.ttf'), 40)
        self.font30 = pygame.font.Font(os.path.join(PATH, 'assets/fonts/PixelifySans-Regular.ttf'), 30)

        # Players
        self.new_game: bool = True
        self.tank = None
        self.tank1 = None
        self.single_tank = None
        self.single_tank1 = None
        self.blocks_list: [] = None
        self.background_tiles: [] = None
        self.start_game()

    def exit_game(self):
        if messagebox.askquestion("Exit", "Are you sure you want to exit?") == 'yes':
            self.is_running = False

    def open_game(self):
        print('stage = 1')
        self.stage = 1

    def start_game(self):
        self.background_tiles = self.create_background()
        self.blocks_list = self.load_map()
        self.tank, self.tank1, self.single_tank, self.single_tank1 = self.create_players()
        self.new_game = False

    def open_creators(self):
        print('stage = 2')
        self.stage = 2

    def open_settings(self):
        print('stage = 3')
        self.stage = 3

    def open_menu(self):
        self.stage = 0
        self.new_game = True
        print('stage = 0')

    def create_menu(self):
        menu = Menu(size=(WIDTH, HEIGHT))
        menu.add_action('1V1 Player', on_action=self.open_game)
        menu.add_action('Settings', on_action=self.open_settings)
        menu.add_action('Creators', on_action=self.open_creators)
        menu.add_action('Exit', on_action=self.exit_game)
        return menu

    def create_players(self):
        tank = Tank(self.screen, self.blocks_list, tank_base_image='tank_base_blue.png',
                    tank_weapon_image='tank_weapon_blue.png')
        tank.rect.topleft = (STEP, STEP)
        single_tank = pygame.sprite.GroupSingle(tank)

        tank1 = Tank(self.screen, self.blocks_list, keys=NUMBERS_PLAYER, tank_base_image='tank_base_red.png',
                     tank_weapon_image='tank_weapon_red.png')
        tank1.rect.bottomright = (WIDTH - STEP, HEIGHT - STEP)
        tank1.rotate_base(180)
        tank1.rotate_weapon(180)
        single_tank1 = pygame.sprite.GroupSingle(tank1)
        return tank, tank1, single_tank, single_tank1

    def create_background(self):
        grass = os.path.join(PATH, 'assets/images/grass.png')
        background = []
        x = 0
        y = 0
        for row in map:
            for i in row:
                background.append(Block(x, y, self.screen, 0, grass))
                x += STEP
            y += STEP
            x = 0
        return background

    def load_map(self):
        blocks_list = []

        wall_image1 = os.path.join(PATH, 'assets/images/wall.png')
        wall_image2 = os.path.join(PATH, 'assets/images/wall1.png')
        x = 0
        y = 0
        for row in map:
            for i in row:
                if i == 1:
                    blocks_list.append(Block(x, y, self.screen, 1, wall_image1))
                elif i == 2:
                    blocks_list.append(Block(x, y, self.screen, 2, wall_image2))
                x += STEP
            y += STEP
            x = 0
        return blocks_list

    def play(self):
        menu = self.create_menu()

        button_back_gr = pygame.sprite.GroupSingle()
        self.button_back = Button('Back', size=(100, 50), command=lambda: self.back(0))
        button_back_gr.add(self.button_back)

        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                if event.type == pygame.KEYDOWN:
                    self.tank.control_input()
                    self.tank1.control_input()
                if self.stage == 1 and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if messagebox.askquestion("Pause", "Are you sure you want to exit to menu?") == 'yes':
                        self.open_menu()
            if self.stage != 0:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            if self.stage == 0:
                menu.update()
                self.screen.blit(menu, (0, 0))
            elif self.stage == 1:
                # for i in self.background_tiles:
                #     i.blit()
                self.screen.blit(self.main_bg, (0, 0))
                if self.new_game:
                    self.start_game()

                self.tank.set_enemies([self.tank1.collide_rect])
                self.tank1.set_enemies([self.tank.collide_rect])

                self.check_bullets_collision([self.tank, self.tank1])
                if self.tank.check_collide(self.tank1):
                    self.winner = 1
                    self.stage = 4
                if self.tank1.check_collide(self.tank):
                    self.winner = 2
                    self.stage = 4

                self.single_tank.update()
                self.single_tank.draw(self.screen)

                self.single_tank1.update()
                self.single_tank1.draw(self.screen)
            elif self.stage == 2:
                self.show_creators()
                button_back_gr.update()
                button_back_gr.draw(self.screen)
            elif self.stage == 3:
                self.show_settings()
                button_back_gr.update()
                button_back_gr.draw(self.screen)
            elif self.stage == 4:
                self.show_winner()
                button_back_gr.update()
                button_back_gr.draw(self.screen)

            pygame.display.update()
            self.clock.tick(60)

    def back(self, stage):
        self.stage = stage
        print(f'stage = {self.stage}')

    def show_creators(self):
        # Background
        self.screen.blit(self.main_bg, (0, 0))

        # Background for text
        bg_surf = pygame.transform.rotozoom(
            pygame.image.load(os.path.join(PATH, 'assets/images/BG.png')).convert_alpha(), 0, 2)
        bg_rect = bg_surf.get_rect()
        bg_rect.center = self.main_bg.get_rect().center

        # Title
        title_surf = self.font40.render('Creators', True, '#caa84f')
        title_rect = title_surf.get_rect()
        title_rect.center = (bg_rect.width // 2, 35)
        bg_surf.blit(title_surf, title_rect)

        # Content
        content = [self.font30.render('Developer: ', False, '#caa84f'),
                   self.font30.render('***SilentProg***', False, '#caa84f'),
                   self.font30.render('Asset design:', False, '#caa84f'),
                   self.font30.render('***Open Source***', False, '#caa84f')]

        start_y = 90
        for i, text in enumerate(content):
            rect = text.get_rect()
            rect.center = (bg_rect.width // 2, start_y)
            bg_surf.blit(text, rect)
            start_y += rect.height + 10

        # Button back
        self.button_back.rect.center = (self.main_bg.get_rect().centerx, self.main_bg.get_rect().centery + 140)

        self.screen.blit(bg_surf, bg_rect)

    def show_settings(self):
        # Background
        self.screen.blit(self.main_bg, (0, 0))

        # Background for text
        bg_surf = pygame.transform.rotozoom(
            pygame.image.load(os.path.join(PATH, 'assets/images/BG.png')).convert_alpha(), 0, 2)
        bg_rect = bg_surf.get_rect()
        bg_rect.center = self.main_bg.get_rect().center

        # Title
        title_surf = self.font40.render('Settings', True, '#caa84f')
        title_rect = title_surf.get_rect()
        title_rect.center = (bg_rect.width // 2, 35)
        bg_surf.blit(title_surf, title_rect)

        # Settings
        volume_rect = pygame.rect.Rect(bg_rect.width, 50, 0, 90)
        # volume_slider = UIHorizontalSlider(relative_rect=volume_rect, start_value=0, value_range=100, click_increment=10)

        coming_soon = self.font30.render('Coming soon', True, '#caa84f')
        coming_soon_rect = coming_soon.get_rect()
        coming_soon_rect.center = (bg_rect.width//2, 90)
        bg_surf.blit(coming_soon, coming_soon_rect)

        # Button back
        self.button_back.rect.center = (self.main_bg.get_rect().centerx, self.main_bg.get_rect().centery + 140)
        self.screen.blit(bg_surf, bg_rect)

    def check_bullets_collision(self, players: []):
        # grass = os.path.join(PATH, 'assets/images/grass.png')
        for block in self.blocks_list:
            block.blit()
            for tank in players:
                if block.colliderect(tank.tank_shell):
                    tank.tank_shell.stop()
                    if block.type_block == 1:
                        # new_block = Block(block.x, block.y, self.screen, 0, grass)
                        # self.blocks_list.append(new_block)
                        block.x = 1000000

    def show_winner(self):
        # Background
        self.screen.blit(self.main_bg, (0, 0))
        # Background for text
        bg_surf = pygame.transform.rotozoom(
            pygame.image.load(os.path.join(PATH, 'assets/images/BG.png')).convert_alpha(), 0, 2)
        bg_rect = bg_surf.get_rect()
        bg_rect.center = self.main_bg.get_rect().center

        # Title
        title_surf = self.font40.render('Winner', True, '#caa84f')
        title_rect = title_surf.get_rect()
        title_rect.center = (bg_rect.width // 2, 35)
        bg_surf.blit(title_surf, title_rect)

        winner_text = None
        if self.winner == 1:
            winner_text = self.font30.render('Blue win!', True, 'Blue')
        if self.winner == 2:
            winner_text = self.font30.render('Red win!', True, 'Red')
        winner_rect = winner_text.get_rect()
        winner_rect.center = (bg_rect.width // 2, 90)

        bg_surf.blit(winner_text, winner_rect)

        # Button back
        self.button_back.rect.center = (self.main_bg.get_rect().centerx, self.main_bg.get_rect().centery + 140)

        self.screen.blit(bg_surf, bg_rect)
        self.new_game = True


def main():
    game = Game()
    game.play()


if __name__ == "__main__":
    main()
