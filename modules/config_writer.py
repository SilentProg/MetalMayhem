import configparser
import pygame

config = configparser.ConfigParser()

# Додаємо розділ та значення
config['WASD_PLAYER'] = {
    'weapon_rotate_r': pygame.K_e,
    'weapon_rotate_l': pygame.K_q,
    'w': pygame.K_w,
    'a': pygame.K_a,
    's': pygame.K_s,
    'd': pygame.K_d,
    'weapon_fire': pygame.K_SPACE,
    'weapon_reset': pygame.K_c
}

config['NUMBERS_PLAYER'] = {
    'weapon_rotate_r': pygame.K_o,
    'weapon_rotate_l': pygame.K_u,
    'w': pygame.K_i,
    'a': pygame.K_j,
    's': pygame.K_k,
    'd': pygame.K_l,
    'weapon_fire': pygame.K_SLASH,
    'weapon_reset': pygame.K_BACKSLASH
}

config['SCREEN'] = {
    'WIDTH': 1400,
    'HEIGHT': 800,
    'COLS': 28,
    'ROWS': 16,
}


def write_config(config_path):
    # Записуємо конфігурацію у файл
    with open(config_path, 'w') as configfile:
        config.write(configfile)
