import os

import pygame

from modules.mapsetting import Block, map
from modules.menu import Menu
from modules.const import PATH, SCREEN_SIZE, WIDTH, HEIGHT, NUMBERS_PLAYER, STEP, COLS, ROWS
from modules.tank import Tank


class Game:
    def __init__(self):
        pygame.init()
        self.is_running = True
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption('Metal Mayhem: Tanktopia64 2D')
        self.pygame_icon = pygame.image.load(os.path.join(PATH, 'assets/images/favicon.png')).convert_alpha()
        self.pygame_icon_transformed = pygame.transform.scale(self.pygame_icon, (200, 200))
        self.pygame_icon_transformed_rect = self.pygame_icon_transformed.get_rect(midright=(WIDTH - 100, HEIGHT // 2))
        pygame.display.set_icon(self.pygame_icon)
        self.clock = pygame.time.Clock()
        self.stage = 0
        self.is_winner = False
        self.winner = None
        self.background = pygame.image.load(os.path.join(PATH, 'assets/images/background_map.png'))
        self.background = pygame.transform.scale(self.background, SCREEN_SIZE)

        font = pygame.font.Font(None, 120)
        self.winner1_text = font.render('BLUE WIN', True, (0, 0, 255))
        self.winner2_text = font.render('RED WIN', True, (255, 0, 0))

    def exit_game(self):
        self.is_running = False

    def play_one(self):
        print('stage = 1')
        self.stage = 1

    def play(self):
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
        # ------------------------------

        menu = Menu(size=(WIDTH, HEIGHT))
        menu.add_action('1 Player', self.play_one)
        menu.add_action('2 Player')
        menu.add_action('Settings')
        menu.add_action('Creators')
        menu.add_action('Exit', on_action=self.exit_game)
        tank = Tank(self.screen, blocks_list)
        single_tank = pygame.sprite.GroupSingle(tank)

        tank1 = Tank(self.screen, blocks_list, pos=(500, 500), keys=NUMBERS_PLAYER)
        single_tank1 = pygame.sprite.GroupSingle(tank1)

        while self.is_running:
            tank.set_enemies([tank1.collide_rect])
            tank1.set_enemies([tank.collide_rect])
            if self.stage != 0:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                if event.type == pygame.KEYDOWN:
                    tank.control_input()
                    tank1.control_input()
            if self.stage == 0:
                menu.update()
                # menu.background.blit(self.pygame_icon_transformed, self.pygame_icon_transformed_rect)
                self.screen.blit(menu, (0, 0))
            else:
                self.screen.fill('Black')
                for block in blocks_list:
                    block.blit()
                    if block.colliderect(tank1.tank_shell):
                        tank1.tank_shell.stop()
                        if block.type_block == 1:
                            map[block.y // STEP][block.x // STEP] = 0
                            block.x = 1000000
                    if block.colliderect(tank.tank_shell):
                        tank.tank_shell.stop()
                        if block.type_block == 1:
                            map[block.y // STEP][block.x // STEP] = 0
                            block.x = 1000000

                single_tank.update()
                single_tank.draw(self.screen)

                if tank.check_collide(tank1):
                    self.winner = 1
                    self.is_running = False
                    self.is_winner = True
                if tank1.check_collide(tank):
                    self.winner = 2
                    self.is_running = False
                    self.is_winner = True

                single_tank1.update()
                single_tank1.draw(self.screen)
                # self.screen.blit(tank, (100, 100))
                self.draw_grid()

            pygame.display.update()
            self.clock.tick(60)

            cors = (WIDTH // 2 - self.winner1_text.get_width() // 2,
                    HEIGHT // 2 - self.winner1_text.get_height() // 2)
            while self.is_winner:
                self.screen.blit(self.background, (0, 0))
                if self.winner == 1:
                    self.screen.blit(self.winner1_text, cors)
                elif self.winner == 2:
                    self.screen.blit(self.winner2_text, cors)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.is_winner = False
                pygame.display.flip()

    def draw_grid(self):
        for c in range(COLS + 1):
            pygame.draw.line(self.screen, 'white', (c * STEP, 0), (c * STEP, HEIGHT))
        for c in range(ROWS + 1):
            pygame.draw.line(self.screen, 'white', (0, c * STEP), (WIDTH, c * STEP))


def main():
    game = Game()
    game.play()


if __name__ == "__main__":
    main()
