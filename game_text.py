import pygame

class GameText:
    """创建过关后显示获胜信息的类"""
    def __init__(self, ai_game):
        """初始化资源属性"""
        self.screen = ai_game.screen
        # 定义字体大小的风格
        self.font = pygame.font.SysFont('italic', 150)
        # 设置文本颜色等属性并将其渲染为图像
        self.v_image = self.font.render("Victory!", True, (255, 0, 0))
        self.o_image = self.font.render("Game Over!", True, (255, 0, 0))
        self.v_rect = self.v_image.get_rect()
        self.o_rect = self.o_image.get_rect()
        # 设置文本显示位置
        self.v_rect.center = self.screen.get_rect().center
        self.o_rect.center = self.screen.get_rect().center

    def show_victory_text(self):
        """如果游戏过关，则显示胜利的文本图像"""
        self.screen.blit(self.v_image, self.v_rect)

    def show_game_over_text(self):
        """如果游戏失败，则显示结束的文本图像"""
        self.screen.blit(self.o_image, self.o_rect)
    