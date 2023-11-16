import pygame

from pygame.sprite import Sprite

class ShotBullet(Sprite):
    """管理外星人所发射的子弹的类"""

    def __init__(self, ai_game, shooter):
        """初始化一个外星人发射的子弹"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.ai_game = ai_game
        self.shooter = shooter
        # 创建一个圆点子弹
        self.image = pygame.image.load("images/bullets/dot_bullet.png")
        self.rect = self.image.get_rect()
        
        # 设置子弹的正确位置
        self.rect.center = self.shooter.rect.center

        # 存储用浮点数表示的子弹位置
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

        # 为每个子弹标记一个序号（默认为1）
        self.id = 1

    def set_id(self, id):
        """设置每个散弹的id为一个正整数"""
        self.id = id
       
    def initialize_flight_path(self):
        """根据其序号，设置该子弹的飞行速度及运动方向"""
        # 设置子弹的移动速度
        if self.id == 1 or self.id == 9:
            self.x_speed = 0
            self.y_speed = 2
        elif self.id == 2 or self.id == 8 or self.id == 10 or self.id == 16:
            self.x_speed = 0.5
            self.y_speed = 1.5
        elif self.id == 3 or self.id == 7 or self.id == 11 or self.id == 15:
            self.x_speed = 1
            self.y_speed = 1
        elif self.id == 4 or self.id == 6 or self.id == 12 or self.id == 14:
            self.x_speed = 1.5
            self.y_speed = 0.5
        elif self.id == 5 or self.id == 13:
            self.x_speed = 2
            self.y_speed = 0

        # 设置子弹的移动方向
        if self.id >= 0 and self.id <= 5:
            self.x_direction = 1
            self.y_direction = 1
        elif self.id >= 6 and self.id <= 9:
            self.x_direction = 1
            self.y_direction = -1
        elif self.id >= 10 and self.id <= 13:
            self.x_direction = -1
            self.y_direction = -1
        elif self.id >= 14 and self.id <= 16:
            self.x_direction = -1
            self.y_direction = 1

    def update(self):
        """更新子弹的位置"""
        self.x += self.x_speed * self.x_direction
        self.y += self.y_speed * self.y_direction
        self.rect.centerx = self.x
        self.rect.centery = self.y

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        self.screen.blit(self.image, self.rect)