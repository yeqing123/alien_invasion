import pygame

from pygame.sprite import Sprite

class DotBullet(Sprite):
    """负责管理小圆点子弹"""
    
    def __init__(self, ai_game, x_position, y_position):
        """初始化各类属性"""
        super().__init__()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.flight_speed = 3.5

        self.image = pygame.image.load('images/dot_bullet.png')
        self.rect = self.image.get_rect()

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self._set_position(x_position, y_position)

    def _set_position(self, x_position, y_position):
        """设置出现的坐标位置"""
        self.rect.centerx = x_position
        self.rect.centery = y_position

    def update(self):
        """更新其位置"""
        self.y += self.flight_speed
        self.rect.y = self.y

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        self.screen.blit(self.image, self.rect)

