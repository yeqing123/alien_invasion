import pygame

from pygame.sprite import Sprite
from  math import sqrt

class DotBullet(Sprite):
    """管理外星人所发射的子弹的类"""

    def __init__(self, ai_game, shooter):
        """初始化一个外星人发射的子弹"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.ai_game = ai_game
        self.shooter = shooter
        
        # 先从缓存中提取
        self.image = ai_game.image_cacha.get('dot_bullet')
        if not self.image:
            # 加载文件
            self.image = pygame.image.load("images/bullets/dot_bullet.png")
            # 存入缓存
            ai_game.image_cacha['dot_bullet'] = self.image

         # 对图片进行优化处理
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        
        # 设置子弹的正确位置
        self.initialize_position(self.shooter)

    def initialize_position(self, shooter):
        """动态设置子弹的初始位置"""
        # 更新发射者的位置
        self.shooter = shooter
        self.rect.center = self.shooter.rect.midbottom
        # 存储用浮点数表示的子弹位置
        self.y = float(self.rect.centery)

    def update(self):
        """更新子弹的位置"""
        self.y += self.settings.alien_bullet_speed
        self.rect.centery = self.y

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        self.screen.blit(self.image, self.rect)