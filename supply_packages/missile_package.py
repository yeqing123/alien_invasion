import pygame

from random import randint
from pygame.sprite import Sprite

from supply_packages.basic_package import BasicPackage

class MissilePackage(BasicPackage):
    """该类用于创建导弹补给包，使得飞船可以拥有发射导弹的能力"""

    def __init__(self, ai_game):
        """初始化各类属性"""
        super().__init__(ai_game)

        # 加载补给包的显示图像
        self.image = pygame.image.load("images/rocket_package.png")
        self.rect = self.image.get_rect()

        # 初始化补给包的位置
        self.rect.midbottom = self.screen_rect.midtop
    
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        # 设置补给包的类型
        self.type = "missile"

    def enhance_ship(self):
        print("调用enhance_ship()")
        if self.type == 'missile':
            print("OK!!!")
            self.ai_game.player.play('enhance', 0, 0.5)
            # 向任务调度器中添加定时任务，即每个三秒发射一枚导弹
            self.ai_game.scheduler.add_job(
                self.ai_game.ship.launch_missile, 'interval', seconds=3)
            self.ai_game.scheduler.start()

    
     

        