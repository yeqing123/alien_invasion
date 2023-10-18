import pygame
from pygame.sprite import Sprite

class ShipBullet(Sprite):
    """管理飞船所发射的子弹的类"""

    def __init__(self, ai_game):
        """在飞船的当前位置创建一个子弹对象"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # 在(0, 0)处创建一个表示子弹的矩形，再设置正确的位置
        self.rect = pygame.Rect(0, 0, self.settings.ship_bullet_width,
                                self.settings.ship_bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop    
        # 设置为浮点数类型
        self.y = float(self.rect.y)

    def update(self):
        """向上移动子弹"""
        # 更新飞船的子弹的准确位置
        self.y -= self.settings.bullet_speed
        # 更新表示子弹的rect的位置
        self.rect.y = self.y
    
    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(
            self.screen, self.settings.ship_bullet_color, self.rect)
