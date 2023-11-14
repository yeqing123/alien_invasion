import pygame
from pygame.sprite import Sprite

from level_1.bullets.alien.alien_bullet import AlienBullet


class Alien(Sprite):
    """表示单个外星人的类"""

    def __init__(self, ai_game):
        """初始化外星人并设置其起始位置"""
        super().__init__()
        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.ai_game = ai_game

        # 加载外星人及其爆炸的图像并设置其rect属性
        self.image = pygame.image.load("level_1/images/processed_image.png")
        self.rect = self.image.get_rect()

        # 每个外星人最初都在屏幕的左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储外星人的精确水平位置
        self.x = float(self.rect.x)

    def fire_bullet(self):
        """外星人发射子弹"""
        new_bullet = AlienBullet(self.ai_game, self)
        self.ai_game.alien_bullets.add(new_bullet)

    def check_edges(self):
        """判断外星人是否到达了屏幕边缘"""
        screen_rect = self.screen.get_rect()
        return (self.rect.left <= 0) or (self.rect.right >= screen_rect.right)

    def update(self):
        """更新外星人位置"""
        self.x += (self.settings.alien_speed * self.settings.alien_direction)
        self.rect.x = self.x
