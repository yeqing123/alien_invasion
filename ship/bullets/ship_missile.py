import pygame

from pygame.sprite import Sprite
from math import sqrt
import math

class ShipMissile(Sprite):
    """创建并管理可以追踪外星人的导弹的类"""

    def __init__(self, ai_game):
        """初始化各类属性"""
        super().__init__()
        self.ai_game = ai_game
        self.ship = self.ai_game.ship
        self.settings = ai_game.settings

        self.image = ai_game.image_cacha.get('ship_missile')
        if not self.image:
            # 加载文件
            self.image = pygame.image.load("level_1/images/rocket.png")
            # 存入缓存中
            ai_game.image_cacha['ship_missile'] = self.image

         # 对图片进行优化处理
        self.image = self.image.convert_alpha()
        
        self.rect = self.image.get_rect()

        # 设置导弹的初始位置
        self.initialize_position()

        # 设置导弹飞行速度
        self.flight_speed = 4.5
        # 设置每次更新后旋转的尺度
        self.degree = 0

        # 设置杀伤力
        self.lethality = 20

    def initialize_position(self):
        """动态设置导弹的初始位置"""
        self.rect.center = self.ship.rect.center

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)


    def lock_target(self, target):
        """为导弹锁定目标"""
        self.target = target

    def _calculate_flight_path(self):
        """计算导弹的飞行轨迹"""
        # 获得导弹当前的位置
        x_missile = self.rect.centerx
        y_missile = self.rect.centery
        # 获得目标当前的位置坐标
        x_target = self.target.rect.centerx
        y_target = self.target.rect.centery
        # 获得导弹与目标分别在x,y轴上的距离
        a = (x_missile - x_target)
        b = y_missile - y_target
        # 根据勾股定律，得出导弹与目标之前的直线距离
        c = sqrt(pow(a, 2) + pow(b, 2))
        # 计算出导弹分别在x,y轴上的移动速度
        try:
            self.step_number = c / self.flight_speed
            self.x_speed = float(a / self.step_number)
            self.y_speed = float(b / self.step_number)
        except ZeroDivisionError:
            pass    
        else:
            self._caculate_flight_angle(a, b, c)

    def _caculate_flight_angle(self, a, b, c):
        """计算导弹的飞行角度"""
        # 如果目标在导弹的右侧，就顺时针旋转，否则就逆时针旋转
        if self.rect.x < self.target.rect.x:
            self.rotate_direction = -1
        else:
            self.rotate_direction = 1
        # 根据a,b,c的长度，计算导弹b与c之间的夹角，即导弹的旋转角度
        self.angle = math.degrees(math.acos((a*a-b*b-c*c)/(-2*b*c)))
        # 计算每次旋转时的尺度
        self.rotate_scale = float(self.angle / self.step_number)

    def _rotate_missile(self):
        """旋转导弹"""
        # 更新导弹的飞行角度，直到达到预期的旋转角度
        if self.degree < self.angle:
            self.degree += self.rotate_scale
        # 从缓存中提取
        self.image = self.ai_game.image_cacha.get('ship_missile')
         # 对图片进行优化处理
        self.image = self.image.convert_alpha()
        # 旋转导弹图像
        self.image = pygame.transform.rotate(self.image, self.degree * self.rotate_direction)
        # 设置导弹已弹头为轴心旋转
        self.rect = self.image.get_rect(center=self.rect.midtop)

    def update(self):
        """更新导弹位置"""
        # 因为在游戏进行中导弹还在飞行途中，目标就已经消失了，所以这里要先进行判断
        if self.ai_game.aliens.has(self.target):
            self._calculate_flight_path()
            self._rotate_missile()  
              
        self.x -= self.x_speed
        self.y -= self.y_speed
        self.rect.centerx = self.x
        self.rect.centery = self.y

