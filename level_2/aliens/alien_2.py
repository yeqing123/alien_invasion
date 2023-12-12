import pygame
from pygame.sprite import Sprite
from random import randint

from level_2.bullets.alien.smart_red_bullet import SmartRedBullet


class Alien_2(Sprite):
    """表示单个外星人的类"""

    def __init__(self, ai_game):
        """初始化外星人并设置其起始位置"""
        super().__init__()
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen_rect
        self.ai_game = ai_game

        # 加载外星人及其爆炸的图像并设置其rect属性
        self.image = pygame.image.load("images/aliens/alien_2.png")
         # 对图片进行优化处理
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()

        # 每个外星人都从屏幕上边缘随机出现
        self.rect.x = randint(
            0, self.screen_rect.width - self.rect.width)
        self.rect.y = -1 * self.rect.height

        # 初始化水平移动距离
        self.horizontal_moving = randint(1, self.screen_rect.width)

        # 存储外星人的精确水平位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
         # 设置该外星人的分值
        self.alien_points = 1
        # 移动速度
        self.moving_speed = self.settings.alien_speed
        # 水平移动方向
        self.direction = 1

    def fire_bullet(self):
        """外星人发射子弹"""
        new_bullet = SmartRedBullet(self.ai_game, self)
        self.ai_game.alien_bullets.add(new_bullet)

    def _check_edges(self):
        """判断外星人是否到达了屏幕边缘"""
        return (self.rect.left <= 0) or \
            (self.rect.right >= self.screen_rect.right)
    
    def update(self):
        """更新外星人位置"""
        # 当到达屏幕左右边缘时，就改变其移动方向
        if self._check_edges():
            self.direction *= -1
        
        self.x += self.moving_speed * self.direction
        self.y += self.moving_speed / 2

        # 缩小预设的水平移动距离
        self.horizontal_moving -= self.moving_speed

        # 重置水平移动距离，并随机改变其方向
        if self.horizontal_moving <= 0:
            self.horizontal_moving = randint(1, self.screen_rect.width)
            self.direction *= -1

        self.rect.x = self.x
        self.rect.y = self.y
