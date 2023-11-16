import pygame

from pygame.sprite import Sprite

class DestinationPoint(Sprite):
    """创建目的地标记点"""

    def __init__(self, ai_game):
        """初始化一个外星人发射的子弹"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.ai_game = ai_game
        
        # 在(0, 0)处创建一个表示子弹的红色的实心圆
        self.rect = pygame.draw.circle(
            self.screen, 
            self.settings.alien_bullet_color, 
            [0, 0], 
            self.settings.alien_bullet_radius
            )
        
    def set_position(self, x, y):
        """设置位置"""
        self.rect.centerx = x
        self.rect.centery = y
        
    def draw_point(self):
        """在屏幕上绘制子弹"""
        pygame.draw.circle(
            self.screen, 
            self.settings.alien_bullet_color, 
            self.rect.center, 
            self.settings.alien_bullet_radius
            )