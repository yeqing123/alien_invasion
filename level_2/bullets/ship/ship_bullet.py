import pygame
from pygame.sprite import Sprite

class ShipBullet(Sprite):
    """管理飞船所发射的子弹的类"""

    def __init__(self, ai_game):
        """在飞船的当前位置创建一个子弹对象"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # 加载一个字典图片，生成一个image对象
        self.image = pygame.image.load('level_1/images/1 (3).png')
        self.rect = self.image.get_rect()
        self.rect.midtop = ai_game.ship.rect.midtop    
        # 设置为浮点数类型
        self.y = float(self.rect.y)

    def update(self):
        """向上移动子弹"""
        # 更新飞船的子弹的准确位置
        self.y -= self.settings.ship_bullet_speed
        # 更新表示子弹的rect的位置
        self.rect.y = self.y
    
    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        self.screen.blit(self.image, self.rect)
