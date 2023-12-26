import pygame

from pygame.sprite import Sprite
from  math import sqrt

class SmartRedBullet(Sprite):
    """管理外星人所发射的子弹的类"""

    def __init__(self, ai_game, shooter):
        """初始化一个外星人发射的子弹"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.ai_game = ai_game
        self.shooter = shooter
        # 在(0, 0)处创建一个表示子弹的红色的实心圆
        self.rect = pygame.draw.circle(
            self.screen, 
            self.settings.alien_bullet_color, 
            [0, 0], 
            self.settings.alien_bullet_radius
            )
        # 设置子弹的正确位置
        self.initialize_position(self.shooter)

        # 根据飞船当前的位置，计算子弹的飞行轨迹
        self._calculate_flight_path()


    def initialize_position(self, shooter):
        """动态设置子弹的初始位置"""
        self.shooter = shooter
        self.rect.center = self.shooter.rect.midbottom
        # 存储用浮点数表示的子弹位置
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

            
    def _calculate_flight_path(self):
        """计算从外星人射向飞船的子弹的飞行轨迹"""
        # 获得发射子弹的外星人中心点的x,y坐标
        x_alien = self.shooter.rect.centerx
        y_alien = self.shooter.rect.centery
        # 获得飞船中心点的x,y坐标
        x_ship = self.ai_game.ship.rect.centerx
        y_ship = self.ai_game.ship.rect.centery
        # 获得外星人与飞船分别在x,y轴上的距离
        # 此处得出的结果x_distance有可能是负数，但是我们不用管它，因为在计算子弹移动时
        # 加一个负数正好就表示减去x的值
        x_distance = x_ship - x_alien
        y_distance = y_ship - y_alien
        # 根据勾股定律，得出子弹从外星人飞到飞船的直线距离
        a_square = pow(x_distance, 2)
        b_square = pow(y_distance, 2)
        # 如果x_distance是负数，计算其平方时因为负负得正，所以也不影响计算结果
        c_square = a_square + b_square
        linear_distance = sqrt(c_square)
        # 根据settings.py中设置的子弹飞行速度，计算出子弹分别在x,y轴上的移动速度
        step_number = linear_distance / self.settings.alien_bullet_speed
        self.x_speed = float(x_distance / step_number)
        self.y_speed = float(y_distance / step_number)
       

    def update(self):
        """更新子弹的位置"""
        self.x += self.x_speed
        self.y += self.y_speed
        self.rect.centerx = self.x
        self.rect.centery = self.y

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.circle(
            self.screen, 
            self.settings.alien_bullet_color, 
            self.rect.center, 
            self.settings.alien_bullet_radius
            )