import pygame
import math

from time import sleep
from pygame.sprite import Sprite
from pygame.sprite import Group
from random import randint

from level_2.bullets.alien.smart_green_bullet import SmartGreenBullet
from level_2.destination_point import DestinationPoint

class Alien_3(Sprite):
    """创建一个3号外星人，该外星人将在屏幕中一直随机到处飞行，直到被飞船击毁为止"""
    
    def __init__(self, ai_game):
        """初始化一个从屏幕上边缘随机位置出现的外星人"""
        super().__init__()
        self.settings = ai_game.settings
        self.ai_game = ai_game
        self.screen_rect = ai_game.screen_rect

        self.image = pygame.image.load('images/aliens/alien_3.png')
        self.rect = self.image.get_rect()

        # 设置外星人的初始位置
        self.rect.x = randint(0, self.screen_rect.width)
        self.rect.y = self.rect.height
        
        # 设置该外星人的移动速度
        self.moving_speed = float(self.settings.alien_speed * 1.5)

        # 为了便于精确计算，将其rect的中心点坐标设置为浮点数类型
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)
         # 设置该外星人的分值
        self.alien_points = 1
       
        # 指定外星人的目的地坐标
        self._specify_destination_coordinate()
        # 计算在x,y轴上的移动步长
        self._calculate_move_step_length()
        # 计算外星人将要旋转的角度
        self.angle = self._rotate_alien()


    def fire_bullet(self):
        """外星人发射子弹"""
        new_bullet = SmartGreenBullet(self.ai_game, self)
        self.ai_game.alien_bullets.add(new_bullet)

    def check_edges(self):
        """判断外星人是否到达了屏幕左右两侧的边缘"""
        return (self.rect.left <= 0) or \
            (self.rect.right >= self.screen_rect.right)
    
    def _calculate_move_step_length(self):
        """根据飞行的直线距离，计算外星人在x轴和y轴上的移动步长"""
        # 求出x,y轴上的距离，为了减小误差将运行结果变为浮点类型
        x_distance = float(self.x_des - self.rect.centerx)
        y_distance = float(self.y_des - self.rect.centery)

        # 根据直角三角形勾股定理，计算出斜边的长度即是外星人飞行的直线距离
        straight_line_distance = math.sqrt(
            math.pow(x_distance, 2) + math.pow(y_distance, 2))
        
        # 根据初始化时预设的飞行速度，计算总共需要移动多少步
        step_number = straight_line_distance / self.moving_speed

        # 计算x,y轴上的移动步长(如果x轴上的步长是负数，就向屏幕左边移动，
        # 如果y轴上的步长是负数，就向屏幕上方移动)，为了减小误差将运行结果变为浮点类型
        self.x_step_length = float(x_distance / step_number)
        self.y_step_length = float(y_distance / step_number)

    def _rotate_alien(self):
        """计算外星人将要旋转的角度, 并旋转其图像"""
        # 根据外星人x,y轴坐标形成的直角三角形的a,b,c三条边的长度
        # 首先求出x轴上的长度，并设置水平移动方向，1标志向右移动，-1表示向左移动
        if self.x_des > self.rect.centerx:
            a = self.x_des - self.rect.centerx
            horizontal_direction = 1
        else:
            a = self.rect.centerx - self.x_des
            horizontal_direction = -1

        # 求出y轴上的长度，并设置外星人是否为向上方移动
        if self.y_des > self.rect.centery:
            b = self.y_des - self.rect.centery
        else:
            b = self.rect.centery - self.y_des
            
        # 根据勾股定律得出c的边长
        c = math.sqrt(math.pow(a, 2) + math.pow(b, 2))

        # 计算将要旋转的夹角度数
        try:
            angle = math.degrees(math.acos((a*a-b*b-c*c)/(-2*b*c)))
        except ZeroDivisionError:
            pass
        else:
            # 判断是否要向屏幕上方移动
            if self.y_des < self.rect.centery:
                angle = 180 - angle

            self.image = pygame.image.load('images/aliens/alien_3.png')
            # 旋转图像，并根据水平移动方向设置旋转方向（负数为顺时针旋转，反之为逆时针）
            self.image = pygame.transform.rotate(
                self.image, angle * horizontal_direction)
            # 以图像中心点为轴心旋转
            self.rect = self.image.get_rect(center=self.rect.center)
    
    def _specify_destination_coordinate(self):
        """以随机的方式指定外星人要到达的位置坐标"""
        self.x_des = randint(0, self.screen_rect.width)
        self.y_des = randint(0, self.screen_rect.height)

    def _reach_destination(self):
        """判断外星人是否已经到达指定的地点"""
        # 因为移动过程中会存在误差，所以需要先计算出误差值(移动速度越快，误差越大)
        # 经测试，根据可接受的移动速度，误差值一直保持在-5~5之间比较合适
        x_deviation = float(self.rect.centerx - self.x_des)
        y_deviation = float(self.rect.centery - self.y_des)

        # 判断外星人中心点坐标值是否在误差值以内
        return (x_deviation >= -5 and x_deviation <= 5) and \
            (y_deviation >= -5 and y_deviation <= 5)

    def update(self):
        """更新外星人的位置"""
        self.x += self.x_step_length
        self.y += self.y_step_length
        self.rect.centerx = self.x
        self.rect.centery = self.y
        
        # 判断外星人是否已经到达指定地点
        if self._reach_destination():
            # 指定新的目的地坐标值
            self._specify_destination_coordinate()
            # 计算移动步长
            self._calculate_move_step_length()
            # 旋转外星人图像
            self.angle = self._rotate_alien()
        
