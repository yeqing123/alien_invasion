import pygame
from ship import Ship

class Scoreboard:
    """显示得分信息的类"""

    def __init__(self, ai_game):
        """初始化涉及得分的属性"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.stats = ai_game.stats
        self.settings = ai_game.settings

        self.ships = pygame.sprite.Group()
        # 设置显示得分的字体
        self.font = pygame.font.SysFont(None, 48)
        self.text_color = (30, 30, 30)
        # 初始化游戏状态信息的图像
        self.prep_images()

    def prep_images(self):
        """将所有的状态信息渲染为图像"""
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """将得分渲染为图像"""
        # 将得分舍入到最近的10的整数倍
        rounded_score = round(self.stats.score, -1)
        # 使用格式说明符，使用冒号和逗号（:,）表示让Python在数值的合适位置插入逗号
        score_str = f"{rounded_score:,}"
        self.score_image = self.font.render(
            score_str, True, self.text_color, self.settings.bg_color)
        # 将得分放置在屏幕的右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top =  20

    def prep_high_score(self):
        """将最高得分渲染为图像"""
        rounded_high_score = round(self.stats.high_score, -1)
        high_score_str = f"{rounded_high_score:,}"
        self.high_score_image = self.font.render(
            high_score_str, True, self.text_color, self.settings.bg_color)
        # 将最高得分放置在屏幕顶部的中央
        self.high_score_rect = self.score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """将玩家的等级渲染为图像"""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(
            level_str, True, self.text_color, self.settings.bg_color)
        self.level_rect = self.level_image.get_rect()
        # 设置表示等级数字的位置
        self.level_rect.top = 10 + self.score_rect.bottom
        self.level_rect.right = self.score_rect.right

    def prep_ships(self):
        """显示余下多少艘飞船"""
        # 将所有余下的飞船存放在编组中
        
        for ship_number in range(self.stats.ship_left):
            ship = Ship(self.ai_game)
            ship.rect.top = 10
            ship.rect.left = ship_number * ship.rect.width + 20
            self.ships.add(ship)

    def check_high_score(self):
        """检查是否诞生了新的最高分"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def show_score(self):
        """将所有的状态信息都显示在屏幕上"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
