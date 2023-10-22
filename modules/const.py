import os

import pygame

PATH = os.path.abspath(__file__ + '/../..')
# WIDTH = 1920
# HEIGHT = 1080
WIDTH = 1400
HEIGHT = 800
SCREEN_SIZE = (WIDTH, HEIGHT)
WASD_PLAYER = {
    'weapon_rotate_r': pygame.K_e,
    'weapon_rotate_l': pygame.K_q,
    'w': pygame.K_w,
    'a': pygame.K_a,
    's': pygame.K_s,
    'd': pygame.K_d,
    'weapon_fire': pygame.K_SPACE,
    'weapon_reset': pygame.K_c
}

NUMBERS_PLAYER = {
    'weapon_rotate_r': pygame.K_o,
    'weapon_rotate_l': pygame.K_u,
    'w': pygame.K_i,
    'a': pygame.K_j,
    's': pygame.K_k,
    'd': pygame.K_l,
    'weapon_fire': pygame.K_SLASH,
    'weapon_reset': pygame.K_BACKSLASH
}
