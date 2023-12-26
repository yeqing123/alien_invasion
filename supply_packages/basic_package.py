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
        self.settings = ai_game.main.settings

    def update(self):
        """更新补给包的移动位置"""
        # 更新位置
        self.y += self.settings.sp_speed
        self.rect.y = self.y

    def blitme(self):
        """在屏幕上绘制补给包图像"""
        self.screen.blit(self.image, self.rect)

    @abstractmethod
    def enhance_ship(self):
        """抽象方法，根据补给包的类型对飞船进行相应的增强"""
        pass