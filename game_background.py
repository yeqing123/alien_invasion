import pygame

class GameBackground:
    """负责管理游戏的背景图片的类"""

    def __init__(self, ai_game):
        """初始化各项属性"""
        self.settings = ai_game.settings
        self.screen = ai_game.screen

        # 加载一个图片，生成一个image对象
        self.image = pygame.image.load('images/space (1).jpg')
        self.rect = self.image.get_rect()

    def blitme(self):
        """在屏幕中显示图片"""
        self.screen.blit(self.image, self.rect)