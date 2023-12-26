import pygame

from pygame.sprite import Sprite

class LaserBeam(Sprite):
    """负责激光发射时的图像显示"""
    def __init__(self, ai_game, shooter):
        """初始化各类属性"""
        super().__init__()
        self.ai_game = ai_game
        self.shooter = shooter

        self.image = ai_game.image_cacha.get('laser_beam')
        if not self.image:
            # 加载显示激光束的图片
            self.image = pygame.image.load("images/bullets/laser_beam.bmp")
            # 加入缓存中
            ai_game.image_cacha['laser_beam'] = self.image

        # 优化图像
        self.image = self.image.convert_alpha()
        
        self.rect = self.image.get_rect()

        self.initialize_position()

    def initialize_position(self):
        """初始化激光束的位置"""
        self.rect.centerx = self.shooter.rect.x + 110
        self.rect.top = self.shooter.rect.y + 268

    def update(self):
        """更新子弹的状态及位置"""
        # 因为Boss是在移动中的，所以激光始终要与Boss保持同步移动
        self.rect.centerx = self.shooter.rect.x + 110
        self.rect.top = self.shooter.rect.y + 268
    
    def blitme(self):
        """在屏幕上绘制子弹"""
        self.ai_game.screen.blit(self.image, self.rect)