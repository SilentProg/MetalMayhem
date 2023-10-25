from os.path import join as path_join
import pygame.sprite

from modules.const import PATH, WASD_PLAYER, NUMBERS_PLAYER


class TankWeapon:
    def __init__(self) -> None:
        self.image = pygame.transform.rotozoom(
            pygame.image.load(path_join(PATH, 'assets/images/tank_weapon.png')).convert_alpha(), 0, 0.6)
        self.rect = self.image.get_rect()
        self.angle = 0

    def rotate(self, angle):
        rotate = (360 - self.angle + angle)
        self.image = pygame.transform.rotate(self.image, rotate)
        self.rect = self.image.get_rect()
        self.angle = angle


class TankBase:
    def __init__(self) -> None:
        self.image = pygame.transform.rotozoom(
            pygame.image.load(path_join(PATH, 'assets/images/tank_base.png')).convert_alpha(), 0, 0.6)
        self.rect = self.image.get_rect()
        self.rect.move_ip(-50, 0)
        self.angle = 0
        print(f'width = {self.image.get_width()} | height = {self.image.get_height()}')

    def rotate(self, angle):
        rotate = (360 - self.angle + angle)
        self.image = pygame.transform.rotate(self.image, rotate)
        self.rect = self.image.get_rect()
        self.rect.move_ip(self.rect.centerx - 15, self.rect.centery)
        self.angle = angle


class Shell:
    def __init__(self, window) -> None:
        self.image = pygame.transform.rotozoom(
            pygame.image.load(path_join(PATH, 'assets/images/shell.png')).convert_alpha(), 0, 0.5)
        self.rect = self.image.get_rect()
        self.direction = 0
        self.window = window
        self.speed = 20
        self.count = 0

    def set_angle(self, angle, center):
        if self.direction != angle:
            rotate = (360 - self.direction + angle)
            self.image = pygame.transform.rotate(self.image, rotate)
            self.rect = self.image.get_rect()
            self.direction = angle
        self.rect.center = center

    def move(self):
        if self.count != 0:
            self.window.blit(self.image, (self.rect.x, self.rect.y))
            if self.direction == 0:
                self.rect.x += self.speed
            elif self.direction == 180:
                self.rect.x -= self.speed
            elif self.direction == 90:
                self.rect.y -= self.speed
            elif self.direction == 270:
                self.rect.y += self.speed
            self.count -= 1
            if self.count == 0:
                self.stop()

    def stop(self):
        self.count = 0
        self.rect.x = 100000


class FireEffect:
    def __init__(self) -> None:
        self.image = pygame.transform.rotozoom(
            pygame.image.load(path_join(PATH, 'assets/images/fire.png')).convert_alpha(), 0, 0.5)
        self.rect = self.image.get_rect()
        self.start_time = None
        self.direction = 0
        self.display_duration = 500
        self.image_visible = False

    def show(self, window, angle, pos):
        if not self.image_visible: return
        current_time = pygame.time.get_ticks()
        if self.start_time is None:
            self.start_time = current_time
        if current_time - self.start_time < self.display_duration:
            rotate = (360 - self.direction + angle)
            self.image = pygame.transform.rotate(self.image, rotate)
            self.rect = self.image.get_rect()
            self.rect.center = pos
            self.direction = angle
            window.blit(self.image, self.rect)
            self.image_visible = True
        else:
            self.image_visible = False
            self.start_time = None


class Tank(pygame.sprite.Sprite):
    def __init__(self, window: pygame.Surface, walls: [], pos=(200, 200), keys: {} = WASD_PLAYER) -> None:
        super().__init__()
        self.image = pygame.Surface((100, 100), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.previous_pos = pos
        self.walls = walls
        self.window = window
        self.control_keys = keys
        self.tank_base = TankBase()
        self.__tank_weapon = TankWeapon()
        self.collide_surface = pygame.Surface((self.tank_base.rect.width + 2, self.tank_base.rect.height + 2))
        self.collide_rect = self.collide_surface.get_rect()
        self.collide_rect.center = self.rect.center
        self.tank_base.rect.center = (self.rect.width // 2, self.rect.height // 2)
        self.tank_shell = Shell(self.window)
        self.__tank_fire_effect = FireEffect()
        self.rotate_weapon(0)
        self.rotate_base(0)
        self.enemies: [] = []

    def set_enemies(self, enemies: []):
        self.enemies = enemies

    def fire(self):
        if self.tank_shell.count == 0:
            self.tank_shell.set_angle(self.__tank_weapon.angle, self.rect.center)
            self.tank_shell.count = 100
            self.__tank_fire_effect.image_visible = True

    def check_collide(self, tank):
        if self.tank_shell.rect.colliderect(tank.collide_rect):
            return True

    def rotate_weapon(self, angle):
        if angle == 360:
            angle = 0
        if angle == -90:
            angle = 270
        print(angle)
        self.__tank_weapon.rotate(angle)
        if self.__tank_weapon.angle == 0:
            self.__tank_weapon.rect.center = (self.tank_base.rect.centerx + 15, self.tank_base.rect.centery)
        elif self.__tank_weapon.angle == 180:
            self.__tank_weapon.rect.center = (self.tank_base.rect.centerx - 15, self.tank_base.rect.centery)
        elif self.__tank_weapon.angle == 90:
            self.__tank_weapon.rect.center = (self.tank_base.rect.centerx, self.tank_base.rect.centery - 15)
        elif self.__tank_weapon.angle == 270:
            self.__tank_weapon.rect.center = (self.tank_base.rect.centerx, self.tank_base.rect.centery + 15)

    def rotate_base(self, angle):
        rotate = (360 - self.tank_base.angle + angle)
        self.collide_surface = pygame.transform.rotate(self.collide_surface, rotate)
        self.collide_rect = self.collide_surface.get_rect()
        self.collide_rect.center = self.rect.center
        self.tank_base.rotate(angle)
        self.tank_base.rect.center = self.rect.center
        self.tank_base.rect.center = (self.rect.width // 2, self.rect.height // 2)

    def get_rotate_collied_rect(self, angle):
        rotate = (360 - self.tank_base.angle + angle)
        collide_surface = pygame.transform.rotate(self.collide_surface, rotate)
        collide_rect = collide_surface.get_rect()
        collide_rect.center = self.rect.center
        return collide_rect

    def control_input(self):
        keys = pygame.key.get_pressed()

        if keys[self.control_keys['weapon_rotate_r']]:
            self.rotate_weapon(self.__tank_weapon.angle - 90)
        if keys[self.control_keys['weapon_rotate_l']]:
            self.rotate_weapon(self.__tank_weapon.angle + 90)
        if keys[self.control_keys['weapon_fire']]:
            self.fire()
        if keys[self.control_keys['weapon_reset']]:
            self.rotate_weapon(self.tank_base.angle)

    def update(self):
        # self.image.fill((0, 255, 0, 255))
        self.image.fill((0, 0, 0, 0))
        keys = pygame.key.get_pressed()
        collide_enemies = self.collide_rect.collidelist(self.enemies)
        collide = self.collide_rect.collidelist(self.walls)
        if collide == -1 and collide_enemies == -1:
            self.previous_pos = (self.rect.centerx, self.rect.centery)
            if keys[self.control_keys['w']]:
                if self.get_rotate_collied_rect(90).collidelist(self.walls) == -1 and self.get_rotate_collied_rect(90).collidelist(self.enemies) == -1:
                    self.rotate_base(90)
                    self.rect.centery = self.rect.centery - 2
            elif keys[self.control_keys['s']]:
                if self.get_rotate_collied_rect(270).collidelist(self.walls) == -1 and self.get_rotate_collied_rect(270).collidelist(self.enemies) == -1:
                    self.rotate_base(270)
                    self.rect.centery = self.rect.centery + 2
            elif keys[self.control_keys['a']]:
                if self.get_rotate_collied_rect(180).collidelist(self.walls) == -1 and self.get_rotate_collied_rect(180).collidelist(self.enemies) == -1:
                    self.rotate_base(180)
                    self.rect.centerx = self.rect.centerx - 2
            elif keys[self.control_keys['d']]:
                if self.get_rotate_collied_rect(0).collidelist(self.walls) == -1 and self.get_rotate_collied_rect(0).collidelist(self.enemies) == -1:
                    self.rotate_base(0)
                    self.rect.centerx = self.rect.centerx + 2
        else:
            self.rect.center = self.previous_pos

        self.image.blit(self.tank_base.image, self.tank_base.rect)
        self.tank_shell.move()
        self.image.blit(self.__tank_weapon.image, self.__tank_weapon.rect)
        self.show_fire_effect()
        self.collide_rect.center = self.rect.center

    def show_fire_effect(self):
        fire_effect_pos = None
        if self.__tank_weapon.angle == 0:
            fire_effect_pos = self.__tank_weapon.rect.midright
        elif self.__tank_weapon.angle == 90:
            fire_effect_pos = self.__tank_weapon.rect.midtop
        elif self.__tank_weapon.angle == 180:
            fire_effect_pos = self.__tank_weapon.rect.midleft
        elif self.__tank_weapon.angle == 270:
            fire_effect_pos = self.__tank_weapon.rect.midbottom
        self.__tank_fire_effect.show(self.image, self.__tank_weapon.angle, fire_effect_pos)
