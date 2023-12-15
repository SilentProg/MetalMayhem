import os
import configparser
import pygame

PATH = os.path.abspath(__file__ + '/../..')

config_path = os.path.join(PATH, 'config.ini')

config = configparser.ConfigParser()

if not os.path.exists(config_path):
    from modules.config_writer import write_config
    write_config(config_path)

config.read(config_path)

WIDTH = int(config.get('SCREEN', 'WIDTH'))
HEIGHT = int(config.get('SCREEN', 'HEIGHT'))
COLS = int(config.get('SCREEN', 'COLS'))
ROWS = int(config.get('SCREEN', 'ROWS'))

SCREEN_SIZE = (WIDTH, HEIGHT)
STEP = HEIGHT // ROWS
WASD_PLAYER = {
    'weapon_rotate_r': int(config.get('WASD_PLAYER', 'weapon_rotate_r')),
    'weapon_rotate_l': int(config.get('WASD_PLAYER', 'weapon_rotate_l')),
    'w': int(config.get('WASD_PLAYER', 'w')),
    'a': int(config.get('WASD_PLAYER', 'a')),
    's': int(config.get('WASD_PLAYER', 's')),
    'd': int(config.get('WASD_PLAYER', 'd')),
    'weapon_fire': int(config.get('WASD_PLAYER', 'weapon_fire')),
    'weapon_reset': int(config.get('WASD_PLAYER', 'weapon_reset'))
}

NUMBERS_PLAYER = {
    'weapon_rotate_r': int(config.get('NUMBERS_PLAYER', 'weapon_rotate_r')),
    'weapon_rotate_l': int(config.get('NUMBERS_PLAYER', 'weapon_rotate_l')),
    'w': int(config.get('NUMBERS_PLAYER', 'w')),
    'a': int(config.get('NUMBERS_PLAYER', 'a')),
    's': int(config.get('NUMBERS_PLAYER', 's')),
    'd': int(config.get('NUMBERS_PLAYER', 'd')),
    'weapon_fire': int(config.get('NUMBERS_PLAYER', 'weapon_fire')),
    'weapon_reset': int(config.get('NUMBERS_PLAYER', 'weapon_reset'))
}

print(WASD_PLAYER)
print(NUMBERS_PLAYER)
