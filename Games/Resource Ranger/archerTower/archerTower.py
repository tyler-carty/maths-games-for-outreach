import os.path
import math
import pygame
from .tower import Tower
from menu.menu import Menu

menu_bg = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "table_2.png")), (123, 70))
upgrade_btn = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "upgrade.png")), (50, 50))

tower_imgs1 = []  # list of images for the first tower
archer_imgs1 = []  # list of images for the first tower

for x in range(10, 13):
    tower_imgs1.append(
        pygame.transform.scale(pygame.image.load(os.path.join("archeryTowerAssets/archerTower1/", str(x) + ".png")),
                               (90, 90)))

for x in range(51, 57):
    archer_imgs1.append(
        pygame.transform.scale(pygame.image.load(os.path.join("archeryTowerAssets/archerTower2/", str(x) + ".png")),
                               (40, 40)))


# Crossbow Tower
class ArcherTower(Tower):

    def __init__(self, x, y):
        super().__init__(x, y)  # call the parent class constructor
        self.tower_imgs = tower_imgs1
        self.archer_imgs = archer_imgs1
        self.archer_count = 0
        self.range = 200
        self.original_range = self.range
        self.inRange = False
        self.left = True
        self.damage = 1
        self.original_damage = self.damage
        self.width = self.height = 90
        self.moving = False
        self.name = "crossbow"

        self.menu = Menu(self, self.x, self.y, menu_bg, [2000, 5000, "Max"])
        self.menu.add_btn(upgrade_btn, "Upgrade")

    def get_upgrade_cost(self):
        return self.menu.get_item_cost()

    def draw(self, win):
        super(ArcherTower, self).draw_radius(win)
        super().draw(win)

        if self.inRange and not self.moving:
            self.archer_count += 1
            if self.archer_count >= len(self.archer_imgs) * 10:
                self.archer_count = 0
        else:
            self.archer_count = 0

        archer = self.archer_imgs[self.archer_count // 10]
        if self.left:
            add = -25
        else:
            add = -archer.get_width() + 10
        win.blit(archer, ((self.x + add), (self.y - archer.get_height() - 25)))

    def change_range(self, r):

        self.range = r

    def attack(self, enemies):

        """
        This method will be called every frame.
        :param enemies:
        :return: None
        """
        money = 0
        self.inRange = False
        enemy_closest = []

        for enemy in enemies:
            x = enemy.x
            y = enemy.y
            dis = math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)
            if dis < self.range:
                self.inRange = True
                enemy_closest.append(enemy)

        enemy_closest.sort(key=lambda x: x.x)
        if len(enemy_closest) > 0:
            first_enemy = enemy_closest[0]
            if self.archer_count == 6:
                if first_enemy.hit(self.damage) == True:
                    money = first_enemy.money
                    enemies.remove(first_enemy)

            if first_enemy.x > self.x and not (self.left):
                self.left = True
                for x, img in enumerate(self.archer_imgs):
                    self.archer_imgs[x] = pygame.transform.flip(img, True, False)
            elif self.left and first_enemy.x < self.x:
                self.left = False
                for x, img in enumerate(self.archer_imgs):
                    self.archer_imgs[x] = pygame.transform.flip(img, True, False)

        return money


tower_imgs = []
archer_imgs = []

for x in range(7, 10):
    tower_imgs.append(
        pygame.transform.scale(pygame.image.load(os.path.join("archeryTowerAssets/archerTower1/", str(x) + ".png")),
                               (90, 90)))

for x in range(38, 44):
    archer_imgs.append(
        pygame.transform.scale(pygame.image.load(os.path.join("archeryTowerAssets/archerTower2/", str(x) + ".png")),
                               (45, 45)))


# Archers Tower
class ArcherTowerShort(ArcherTower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.tower_imgs = tower_imgs
        self.archer_imgs = archer_imgs
        self.archer_count = 0
        self.range = 100
        self.original_range = self.range
        self.inRange = False
        self.left = True
        self.damage = 3
        self.original_damage = self.damage

        self.menu = Menu(self, self.x, self.y, menu_bg, [2500, 5500, "Max"])
        self.menu.add_btn(upgrade_btn, "Upgrade")
        self.name = "archer"

