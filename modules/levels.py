import glob
import os
import pygame

from modules.const import PATH, STEP


class Level:
    def __init__(self) -> None:
        self.blocks: [] = []
        self.tiles: [] = []
        pass

    def load_tiles(self):
        for f in glob.glob(os.path.join(PATH, 'assets\images\Tiles\*.png')):
            self.tiles.append(pygame.transform.scale(pygame.image.load(f).convert_alpha(), (STEP, STEP)))

    def load_level(self, name: str = ''):
        pass
