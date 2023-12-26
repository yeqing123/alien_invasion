import pygame

from threading import Timer
from random import randint

from supply_packages.basic_package import BasicPackage

class StealthPackage(BasicPackage):
    """该类用于创建可使飞船隐身的补给包"""

    def __init__(self, ai_game):
        """初始化各类属性"""
        super().__init__(ai_game)
        self.scheduler = ai_game.scheduler

        # 加载补给包的显示图像
        self.image = pygame.image.load("images/supply_packages/stealth_package.png")
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()

         # 初始化补给包的位置
        self.rect.x = randint(0, self.screen_rect.width - self.rect.width)
        self.rect.y = -1 * self.rect.height

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        # 设置补给包的类型
        self.type = "stealth"

    def enhance_ship(self):
        print("调用enhance_ship()")
        if self.type == 'stealth':
            print("OK!!!")
            self.ai_game.player.play('enhance', 0, 0.5)

            # 开启飞船隐身模式
            self.scheduler.add_job(
                self.ai_game.ship.turn_on_stealth_mode,
                id='stealth_mode')
    
            # 10秒后自动关闭
            #Timer(10, self.ai_game.ship.turn_off_stealth_mode).start()
            