import pygame
from pygame.sprite import Sprite

class Shotgun_2(Sprite):
    """管理飞船所发射的子弹的类"""

    def __init__(self, ai_game):
        """在飞船的当前位置创建一个子弹对象"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.ai_game = ai_game

        self.image = ai_game.image_cacha.get('shotgun_2')
        if not self.image:
            # 加载一个字典图片，生成一个image对象
            self.image = pygame.image.load('images/bullets/ship_bullet.png')
            # 存入缓存中
            ai_game.image_cacha['shotgun_2'] = self.image

        # 对图片进行优化处理
        self.image = self.image.convert_alpha()

        self.rect = self.image.get_rect()
        
        # 初始化子弹位置
        self.initialize_position()
        
        # 设置该子弹的杀伤力（每击中一次会使对方的血量减10）
        self.lethality = 10

    def initialize_position(self):
        """动态设置子弹的初始位置"""
        self.rect.midtop = self.ai_game.ship.rect.midtop    
        # 设置为浮点数类型
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        """向上移动子弹"""
        # 更新飞船的子弹的准确位置
        self.x -= self.settings.ship_bullet_speed
        self.y -= self.settings.ship_bullet_speed
        # 更新表示子弹的rect的位置
        self.rect.x = self.x
        self.rect.y = self.y
    
    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        self.screen.blit(self.image, self.rect)
