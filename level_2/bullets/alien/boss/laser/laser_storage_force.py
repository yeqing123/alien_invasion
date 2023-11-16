import pygame

from pygame.sprite import Sprite

class LaserStorageForce(Sprite):
    """负责激光器蓄力时的图像显示"""
    def __init__(self, ai_game, shooter):
        """初始化各类属性"""
        super().__init__()
        self.ai_game = ai_game
        self.shooter = shooter

        # 加载激光器积蓄能量时的图片
        self.image = pygame.image.load("images/bullets/laser_storage_force.bmp")
        self.rect = self.image.get_rect()

        # 初始化子弹的位置
        self.rect.centerx = self.shooter.rect.x + 110
        self.rect.centery = self.shooter.rect.y + 258

    def update(self):
        """更新子弹的状态及位置"""
        # 因为Boss是在移动中的，所以在子弹在发射之前要与Boss保持同步移动
        self.rect.centerx = self.shooter.rect.x + 110

    
    def blitme(self):
        """在屏幕上绘制子弹"""
        self.ai_game.screen.blit(self.image, self.rect)