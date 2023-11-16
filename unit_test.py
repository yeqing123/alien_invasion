import pygame

from settings import Settings
from level_2.bullets.alien.boss.rotating_bullet import RotatingBullet

class UnitTest:
    """进行游戏的单元测试的类"""
    def __init__(self):
        """初始化主程序所需的各类属性"""    
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        self.rect = self.screen.get_rect()

        self.clock = pygame.time.Clock()

        self.rb = RotatingBullet(self, self)

    def run_test(self):
        """运行测试"""
        while True:
            self._update_screen()
            self.clock.tick(60)

    def _update_screen(self):
        """更新屏幕内容"""
        # 给屏幕填充黑色的背景色
        self.screen.fill((0, 0, 0))
        self.rb.update()
        self.rb.blitme()
        # 显示屏幕
        pygame.display.flip()

if __name__ == "__main__":
    UnitTest().run_test()