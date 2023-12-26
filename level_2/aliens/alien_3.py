import pygame

from pygame.sprite import Sprite
from random import randint
from math import sqrt
from math import degrees
from math import acos
from math import pow

from time import sleep

from level_2.bullets.alien.smart_green_bullet import SmartGreenBullet

class Alien_3(Sprite):
    """创建一个外星人，并控制它的行为"""
    
    def __init__(self, ai_game):
        """初始化一个从屏幕上边缘随机位置出现的外星人"""
        super().__init__()
        self.settings = ai_game.settings
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen_rect

        # 先从图像缓存提取，如果缓存中没有再加载文件
        self.image = ai_game.image_cacha.get('alien_3')
        if not self.image:
            # 加载文件
            self.image = pygame.image.load('images/aliens/alien_3.png')
            self.image = pygame.transform.scale(self.image, (60, 60))
            # 保存到缓存中
            ai_game.image_cacha['alien_3'] = self.image

         # 对图片进行优化处理
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()

        # 设置外星人移动的速度（每个外星人的移动速度都是不同的）
        self.moving_speed = 5.5

         # 设置该外星人的分值
        self.alien_points = 1

        # 初始化外星人的位置
        self.initialize_position()

    def initialize_position(self):
        """重置外星人的位置"""
        # 设置外星人的初始位置
        self.rect.x = randint(self.rect.width, 
                              self.screen_rect.width - self.rect.width)
       
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        # 设置血量
        self.blood_volume = 10

    def _rotate_alien(self):
        """根据外星人移动的方向，旋转外星人的角度"""
        a = self.ai_game.ship.rect.x - self.rect.x
        if a > 0:
            horizontal_direction = 1
        else:
            horizontal_direction = -1

        b = self.ai_game.ship.rect.y - self.rect.y
        # 根据勾股定律计算出第三条边
        c = sqrt(pow(a, 2) + pow(b, 2))

        try:
            angle = degrees(acos((a*a-b*b-c*c)/(-2*b*c)))
        except ZeroDivisionError:
            pass
        else:
            self.image = self.ai_game.image_cacha.get('alien_3')
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
        distance = self.ai_game.ship.rect.y - self.rect.y
        if distance <= 200:
            self._rotate_alien()
            if not self.ai_game.scheduler.get_job(job_id='fire_bullet'):
                self.fire_bullet()
                self.ai_game.scheduler.add_job(self.fire_bullet, 'interval', 
                                            id='fire_bullet', seconds=1)
        else:
            self.y += self.moving_speed
            self.rect.y = self.y

    def blitme(self):
        """将外星人的图像绘制在屏幕上"""
        self.screen.blit(self.image, self.rect)
