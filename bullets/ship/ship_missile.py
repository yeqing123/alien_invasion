import pygame

from pygame.sprite import Sprite
from math import sqrt
import math

class ShipMissile(Sprite):
    """创建并管理可以追踪外星人的导弹的类"""

    def __init__(self, ai_game, target):
        """初始化各类属性"""
        super().__init__()
        self.ai_game = ai_game
        self.ship = self.ai_game.ship
        self.settings = ai_game.settings
        self.target = target

        self.image = pygame.image.load("images/rocket.png")
        self.rect = self.image.get_rect()
        self.rect.center = self.ship.rect.center

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.flight_speed = 3.5

        self.rotate_direction = 1
        self.angle_scale = 0
        self.number = 0
        self.not_kown = 20

    def _calculate_flight_path(self):
        """计算导弹的飞行轨迹"""
        # 获得导弹当前的位置
        x_missile = self.rect.centerx
        y_missile = self.rect.centery
        # 获得目标当前的位置坐标
        x_target = self.target.rect.centerx
        y_target = self.target.rect.centery
        # 获得导弹与目标分别在x,y轴上的距离
        # 此处得出的结果x_distance有可能是负数，但是我们不用管它，因为在计算子弹移动时
        # 加一个负数正好就表示减去x的值
        x_distance = (x_missile - x_target)
        y_distance = y_missile - y_target
        # 根据勾股定律，得出导弹与目标之前的直线距离
        a_square = pow(x_distance, 2)
        b_square = pow(y_distance, 2)
        # 如果x_distance是负数，计算其平方时因为负负得正，所以也不影响计算结果
        c_square = a_square + b_square
        linear_distance = sqrt(c_square)
        # 计算出导弹分别在x,y轴上的移动速度
        self.step_number = linear_distance / self.flight_speed
        self.x_speed = float(x_distance / self.step_number)
        self.y_speed = float(y_distance / self.step_number)

        if x_distance > 0:
            self.rotate_direction = 1
        else:
            self.rotate_direction = -1

        self._caculate_flight_angle(x_distance, y_distance)

    def _caculate_flight_angle(self, a, b):
        """计算导弹的飞行角度"""
        c = sqrt(pow(a, 2) + pow(b, 2))
        self.angle = math.degrees(math.acos((a*a-b*b-c*c)/(-2*b*c)))
        self.angle_scale = float(self.angle / self.step_number)
        print(self.angle)
        


    def _rotate_missile(self):
        """旋转导弹"""
        if self.number < self.angle:
            self.number += self.angle_scale
        
        self.image = pygame.image.load("images/rocket.png")
        self.image = pygame.transform.rotate(self.image, self.number * self.rotate_direction)
        core = (self.rect.centerx, self.rect.centery)
        self.rect = self.image.get_rect(center=core)

    def update(self):
        """更新导弹位置"""
        self._calculate_flight_path()
   #    self._rotate_missile()
        if self.not_kown > 0:
            self.y -= self.flight_speed
            self.not_kown -= self.flight_speed
            self.rect.centery = self.y
        else:    
            self.x -= self.x_speed
            self.y -= self.y_speed
            self.rect.centerx = self.x
            self.rect.centery = self.y

