import pygame

from pygame.sprite import Sprite
from random import randint

from level_2.bullets.alien.dot_bullet import DotBullet

class Alien_1(Sprite):
    """创建一个外星人，并控制它的行为"""
    
    def __init__(self, ai_game):
        """初始化一个从屏幕上边缘随机位置出现的外星人"""
        super().__init__()
        self.settings = ai_game.settings
        self.ai_game = ai_game
        self.screen_rect = ai_game.screen_rect

        self.image = pygame.image.load('images/aliens/alien_1.png')
        self.rect = self.image.get_rect()

        # 外星人的x坐标位置为随机值
        x_max = self.screen_rect.width - self.rect.width
        y_max = -1 * self.rect.height
        y_min = -1 * (self.screen_rect.height / 2)
        
        self.rect.x = randint(0, x_max)
        self.rect.y = randint(y_min, y_max)

        # 设置外星人移动的速度（每个外星人的移动速度都是不同的）
        self.moving_speed = self.settings.alien_speed

        # 为了便于精确计算，将其rect的x,y坐标设置为浮点数类型
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

         # 设置该外星人的分值
        self.alien_points = 1
        # 设置水平移动方向
        self.direction = 1

    def fire_bullet(self):
        """外星人发射子弹"""
        new_bullet = DotBullet(self.ai_game, self)
        self.ai_game.alien_bullets.add(new_bullet)

    def _check_edges(self):
        """判断外星人是否到达了屏幕左右两侧的边缘"""
        return (self.rect.left <= 0) or \
            (self.rect.right >= self.screen_rect.right)

    def update(self):
        """更新外星人的位置"""
        if self._check_edges():
            self.direction *= -1

        self.x += self.moving_speed * self.direction
        self.y += self.moving_speed
        
        self.rect.x = self.x
        self.rect.y = self.y
