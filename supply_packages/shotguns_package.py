import pygame

from pygame.sprite import Sprite
from random import randint
from threading import Timer
from time import sleep

class ShotGunsPackage(Sprite):
    """负责管理飞船散弹补给包的管理"""

    def __init__(self, ai_game):
        """初始化类的属性值"""
        super().__init__()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        # 在主程序的设置文件中，获取补给包的移动速度
        self.moving_speed = ai_game.main.settings.sp_speed
        self.screen_rect = self.screen.get_rect()

        self.image = self.ai_game.image_cacha.get('shotguns_package')
        if not self.image:
            self.image = pygame.image.load("images/supply_packages/shotguns_package.png")
            self.image = pygame.transform.scale(self.image, (50, 34))
            self.image = self.image.convert_alpha()
            self.ai_game.image_cacha['shotguns_package'] = self.image

        self.rect = self.image.get_rect()

        # 设置在x,y轴上的移动方向
        self.x_moving_direction = -1
        self.y_moving_direction = -1

        # 设置补给包的初始位置
        self.initialize_position()
        # 经过设定的时间后消失
        Timer(self.ai_game.main.settings.sp_time, self._package_gone).start()

    def initialize_position(self):
        """设置补给包的初始位置"""
        self.rect.x = self.screen_rect.width / 2
        self.rect.y = self.screen_rect.height / 2

        # 以浮点类型计算补给包的移动
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # x轴上的移动距离是随机的
        self.x_moving_distance = randint(100, self.screen_rect.width )
        # y轴上的移动距离也是随机的
        self.y_moving_distance = randint(100, self.screen_rect.height)

    def update(self):
        """更新补给包的位置"""
        self._check_edges()
        # 在随机方向上移动
        self.x += self.x_moving_direction * self.moving_speed
        self.y += self.y_moving_direction * self.moving_speed

        # 缩小移动的距离
        self.x_moving_distance -= self.moving_speed
        self.y_moving_distance -= self.moving_speed

        self.rect.x = self.x
        self.rect.y = self.y

    def _check_edges(self):
        """检测补给包是否已经移动到了屏幕边界"""
        # 如果已经移动到了屏幕边缘，就改变方向，并重置移动距离
        if self.rect.x < 0 or self.rect.x > self.screen_rect.width:
            self.x_moving_direction *= -1
        if self.rect.y < self.screen_rect.height / 2 or \
                self.rect.y > self.screen_rect.height:
            self.y_moving_direction *= -1
        
        # 如果已经走完x或y上设定的距离后，就重新设定距离，并改变移动方向
        if self.x_moving_distance <= 0:
            self.x_moving_distance = randint(100, self.screen_rect.width)
            self.x_moving_direction *= -1
        if self.y_moving_distance <= 0:
            self.y_moving_distance = randint(100, self.screen_rect.height)
            self.y_moving_direction *= -1

    def _package_gone(self):
        """当补给包经过设定的时间后还没有被飞船吸收，就闪烁5次后消失"""
        number = 0
        while number < 5:
            self.ai_game.packages.remove(self)
            sleep(0.5)
            self.ai_game.packages.add(self)
            sleep(0.5)
            number += 1
        # 彻底消失
        self.ai_game.packages.remove(self)


