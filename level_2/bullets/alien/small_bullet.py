import pygame

from pygame.sprite import Sprite
from  math import sqrt

class SmallBullet(Sprite):
    """管理外星人所发射的子弹的类"""

    def __init__(self, ai_game, x_position, y_position):
        """初始化一个外星人发射的子弹"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.ai_game = ai_game

        # 创建一个表示小的红色的条形子弹，并初始化其位置
        self.rect = pygame.rect.Rect(x_position, y_position, 3, 7)

        # 存储用浮点数表示的子弹位置
        self.y = float(self.rect.y)
        # 设置子弹移动的速度
        self.y_speed = 3.5

    def initialize_position(self, x_position, y_position):
        """动态设置子弹的初始位置"""
        self.rect.x = x_position
        self.rect.y = y_position

        self.y = float(self.rect.y)

    def update(self):
        """更新子弹的位置"""
        self.y += self.y_speed
        self.rect.centery = self.y

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen, self.settings.alien_bullet_color, self.rect)