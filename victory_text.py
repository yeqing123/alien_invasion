import pygame

class VictoryText:
    """创建过关后显示获胜信息的类"""
    def __init__(self, ai_game):
        """初始化资源属性"""
        self.screen = ai_game.screen
        # 定义字体大小的风格
        self.font = pygame.font.SysFont('italic', 150)
        # 设置文本颜色等属性并将其渲染为图像
        self.image = self.font.render("Victory!", True, (255, 0, 0))
        self.rect = self.image.get_rect()
        # 设置文本显示位置
        self.rect.center = self.screen.get_rect().center

    def blitme(self):
        """显示文本图像"""
        self.screen.blit(self.image, self.rect)