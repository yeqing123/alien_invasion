import pygame

class GameBeginInterfaceBG:
    """负责管理游戏开始界面的背景图的类"""

    def __init__(self, ai_game):
        """初始化各项属性"""
        self.settings = ai_game.settings
        self.screen = ai_game.screen

        self.image = pygame.image.load("images/game_begin_image.PNG")
        self.rect = self.image.get_rect()
        self.rect.center = self.screen.get_rect().center

    def blitme(self):
        """将背景图像绘制在屏幕中"""
        self.screen.blit(self.image, self.rect)