import pygame

from pygame.sprite import Sprite

class BossBullet(Sprite):
    """负责管理外星人Boss发射的子弹的类"""

    def __init__(self, ai_game, position):
        """"初始化各类属性"""
        super().__init__()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.boss = ai_game.boss_1

        self.image = pygame.image.load('images/processed_1_13.png')
        self.rect = self.image.get_rect()

        if position == 'left':
            self.rect.centerx = self.boss.rect.x + 23
        if position == 'right':
            self.rect.centerx = self.boss.rect.x + 302

        self.rect.centery = self.boss.rect.y + 193

        self.y = float(self.rect.y)

    def update(self):
        """更新子弹的位置"""
        self.y += self.settings.boss_bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        self.screen.blit(self.image, self.rect)