from abc import ABC, abstractmethod
from pygame.sprite import Sprite
from random import randint


class BasicPackage(ABC, Sprite):
    """
    补给包的基础类型，其中包含抽象方法和所有补给包都通用的属性及方法。
    该类不可以直接使用，只用于所有补给包的父类。
    """

    def __init__(self, ai_game):
        """初始化所有的补给包都通用的属性"""
        super().__init__()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings

        # 初始化补给包的移动距离(最小50个像素，最大为屏幕宽度)
        self.remove_distance = randint(50, self.settings.screen_width)

    def update(self):
        """更新补给包的移动位置"""
        # 先检测是否到达屏幕两侧边缘
        self._check_edge()
        # 更新位置
        self.x += self.settings.sp_speed * self.settings.sp_direction
        self.y += self.settings.sp_speed
        self.rect.x = self.x
        self.rect.y = self.y
        
        # 更新需要移动的距离
        self.remove_distance -= self.settings.sp_speed
        #当距离缩小到小于或等于0时，重新获取一个新的值
        if self.remove_distance <= 0:
            # 随机变换移动方向
            self.settings.sp_direction *= -1
            self.remove_distance = randint(50, self.settings.screen_width)

    def _check_edge(self):
        """检查补给包是否移动到了屏幕的边缘"""
        # 当补给包触碰到屏幕两侧边缘时，改变其移动方向
        if self.rect.left <= 0 or self.rect.right >= self.screen_rect.right:
            self.settings.sp_direction *= -1

    def blitme(self):
        """在屏幕上绘制补给包图像"""
        self.screen.blit(self.image, self.rect)

    @abstractmethod
    def enhance_ship(self):
        """抽象方法，根据补给包的类型对飞船进行相应的增强"""
        pass