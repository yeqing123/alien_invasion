import pygame
from pygame.sprite import Sprite

class AlienBullet(Sprite):
    """管理外星人所发射的子弹的类"""

    def __init__(self, ai_game, shooter):
        """初始化一个外星人发射的子弹"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.ai_game = ai_game
        self.shooter = shooter

        # 在(0, 0)处创建一个表示子弹的矩形，再设置正确的位置
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                                self.settings.bullet_height)
        # 根据射手的类型，完成初始化设置
        self.initialize_settings()
        # 如果是外星人发射的子弹，则计算其飞行轨迹
        self._calculate_flight_path()


    def initialize_settings(self):
        """在创建子弹时完成初始化"""
        # 设置子弹的位置
        self.rect.midbottom = self.shooter.rect.midbottom
        self.alien_x = self.shooter.rect.centerx
        self.alien_y = self.shooter.rect.centery
        # 设置子弹的飞行速度
        self.y_speed = 1.0

        # 存储用浮点数表示的子弹位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
            
    def _calculate_flight_path(self):
        """计算从外星人射向飞船的子弹的飞行轨迹"""
        ship_x = self.ai_game.ship.rect.x
        ship_y = self.ai_game.ship.rect.y
        x_distance = ship_x - self.alien_x
        y_distance = ship_y - self.alien_y
        self.x_speed = x_distance / (y_distance / self.y_speed)

    def update(self):
        """更新子弹的位置"""
        self.x += self.x_speed
        self.y += self.y_speed
        self.rect.x = self.x
        self.rect.y = self.y
    
    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(
            self.screen, self.settings.alien_bullet_color, self.rect)
