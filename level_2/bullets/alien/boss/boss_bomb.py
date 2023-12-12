import pygame

from pygame.sprite import Sprite

class BossBomb(Sprite):
    """创建Boss发射的炸弹的类"""
    
    def __init__(self, ai_game, position):
        """初始化各类属性"""
        super().__init__()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.drop_speed = 4.5

        self.image = pygame.image.load('level_1/images/nzd5 (2).png')
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()

        self._set_position(position)

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def _set_position(self, position):
        """设置出现的坐标位置，position为包含一对坐标值的元组"""
        self.rect.centerx = position[0]
        self.rect.centery = position[1]

    def update(self):
        """更新其位置"""
        self.y += self.drop_speed
        self.rect.y = self.y

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        self.screen.blit(self.image, self.rect)

