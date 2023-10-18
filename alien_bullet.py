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
        # 在(0, 0)处创建一个表示子弹的红色的实心圆
        self.rect = pygame.draw.circle(
            self.screen, 
            self.settings.alien_bullet_color, 
            [0, 0], 
            self.settings.alien_bullet_radius
            )
        # 初始化属性，并设置子弹的正确位置
        self.initialize_settings()

        # 根据飞船当前的位置，计算子弹的飞行轨迹
        self._calculate_flight_path()

        # 存储用浮点数表示的子弹位置
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

    def initialize_settings(self):
        """在创建子弹时完成初始化"""
        # 设置子弹的位置
        self.rect.center = self.shooter.rect.midbottom
        self.alien_x = self.shooter.rect.centerx
        self.alien_y = self.shooter.rect.centery
        # 设置子弹的飞行速度
        self.y_speed = 1.0
            
    def _calculate_flight_path(self):
        """计算从外星人射向飞船的子弹的飞行轨迹"""
        ship_x = self.ai_game.ship.rect.centerx
        ship_y = self.ai_game.ship.rect.centery
        x_distance = ship_x - self.alien_x
        y_distance = ship_y - self.alien_y
        self.x_speed = x_distance / (y_distance / self.y_speed)

    def update(self):
        """更新子弹的位置"""
        self.x += self.x_speed
        self.y += self.y_speed
        self.rect.centerx = self.x
        self.rect.centery = self.y
    
    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.circle(
            self.screen, 
            self.settings.alien_bullet_color, 
            self.rect.center, 
            self.settings.alien_bullet_radius
            )