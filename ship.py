import pygame
from pygame.sprite import Sprite

from bullets.ship_bullet import ShipBullet

class Ship(Sprite):
    """管理飞船的类"""
    
    def __init__(self, ai_game):
        """初始化飞船并设置其初始位置"""
        super().__init__()
        self.screen = ai_game.screen
        self.ai_game = ai_game
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # 飞船移动标志（刚开始不移动）
        self.moving_right = False
        self.moving_left = False

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/processed_ship.bmp')
        self.rect = self.image.get_rect()

        # 每艘新飞船都放在屏幕底部的中央
        self.rect.midbottom = self.screen_rect.midbottom
        # 在飞船的位置属性x中，存放一个浮点数
        self.x = float(self.rect.x)

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)

    def ship_center(self):
        """当飞船被击毁后让其重新居中"""
        self.rect.midbottom = self.screen_rect.midbottom
        # 不要忘记将self.x也重置，因为它才是负责计算飞船的位置
        self.x = float(self.rect.x)

    def fire_bullet(self):
        """飞船发射子弹"""
        if len(self.ai_game.ship_bullets) < self.settings.bullet_allow:
            new_bullet = ShipBullet(self.ai_game)
            self.ai_game.ship_bullets.add(new_bullet)


    def update(self):
        """根据移动标志，调整飞船位置"""
        # 更新飞船的x属性的值，而不是其rect对象的x属性的值
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # 根据self.x更新飞船的rect对象
        self.rect.x = self.x

        