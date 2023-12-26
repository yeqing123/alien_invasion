import pygame

from pygame.sprite import Sprite
from random import randint
from  math import sqrt
from math import degrees
from math import acos

from level_2.bullets.alien.smart_green_bullet import SmartGreenBullet

class Alien_1(Sprite):
    """创建一个外星人，并控制它的行为"""
    
    def __init__(self, ai_game):
        """初始化一个从屏幕上边缘随机位置出现的外星人"""
        super().__init__()
        self.settings = ai_game.settings
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen_rect

        # 先从图像缓存提取，如果缓存中没有再加载文件
        self.image = ai_game.image_cacha.get('alien_1')
        if not self.image:
            # 加载文件
            self.image = pygame.image.load('images/aliens/alien_1.png')
            self.image = pygame.transform.scale(self.image, (60, 60))
            # 保存到缓存中
            ai_game.image_cacha['alien_1'] = self.image

         # 对图片进行优化处理
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        

        # 设置外星人移动的速度（每个外星人的移动速度都是不同的）
        self.moving_speed = 5.5

         # 设置该外星人的分值
        self.alien_points = 1
      
        # 初始化外星人的位置
        self.initialize_position()

        # 计算外星人的飞行轨迹
        self._calculate_flight_path()

    def initialize_position(self):
        """重置外星人的位置"""
        # 设置外星人的初始位置
        self.rect.x = randint(-1*self.rect.width, self.screen_rect.width)
        self.rect.y = randint(-1 * self.rect.height, self.ai_game.ship.rect.y)

        # 保存初始位置坐标
        self.initial_x = self.rect.centerx
        self.initial_y = self.rect.centery
       
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        # 设置血量
        self.blood_volume = 10

    def _calculate_flight_path(self):
        """计算从外星人射向飞船的子弹的飞行轨迹"""
        # 获得飞船中心点的x,y坐标
        x_ship = self.ai_game.ship.rect.centerx
        y_ship = self.ai_game.ship.rect.centery
        # 获得从外星人初始化位置到飞船的x,y轴上的距离
        # 此处得出的结果x_distance有可能是负数，但是我们不用管它，因为在计算子弹移动时
        # 加一个负数正好就表示减去x的值
        x_distance = x_ship - self.initial_x
        y_distance = y_ship - self.initial_y
        # 根据勾股定律，得出子弹从外星人飞到飞船的直线距离
        a_square = pow(x_distance, 2)
        b_square = pow(y_distance, 2)
        # 如果x_distance是负数，计算其平方时因为负负得正，所以也不影响计算结果
        c_square = a_square + b_square
        linear_distance = sqrt(c_square)
        # 根据设置的外星人飞行速度，计算出子弹分别在x,y轴上的移动速度
        step_number = linear_distance / self.moving_speed
        self.x_speed = float(x_distance / step_number)
        self.y_speed = float(y_distance / step_number)

        self._rotate_alien(x_distance, y_distance, linear_distance)

    def _rotate_alien(self, a, b, c):
        """根据外星人移动的方向，旋转外星人的角度"""
        if a > 0:
            horizontal_direction = 1
        else:
            horizontal_direction = -1

        try:
            angle = degrees(acos((a*a-b*b-c*c)/(-2*b*c)))
        except ZeroDivisionError:
            pass
        else:
            self.image = self.ai_game.image_cacha.get('alien_1')
            # 旋转图像，并根据水平移动方向设置旋转方向（负数为顺时针旋转，反之为逆时针）
            self.image = pygame.transform.rotate(
                self.image, angle * horizontal_direction)
            # 以图像中心点为轴心旋转
            self.rect = self.image.get_rect(center=self.rect.center)

    def fire_bullet(self):
        """外星人发射子弹"""
        new_bullet = SmartGreenBullet(self.ai_game, self)
        self.ai_game.alien_bullets.add(new_bullet)

    def update(self):
        """更新外星人的位置"""
        self.x += self.x_speed
        self.y += self.y_speed
        
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        """将外星人的图像绘制在屏幕上"""
        self.screen.blit(self.image, self.rect)
