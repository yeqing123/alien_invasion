import pygame

from pygame.sprite import Sprite

class RotatingBullet(Sprite):
    """旋转的四角星子弹"""

    def __init__(self, ai_game, shooter):
        """初始化各类属性"""
        super().__init__()
        self.ai_game = ai_game
        self.shooter = shooter

        # 加载名为“four_pointed_star.png”的图片
        self.image = pygame.image.load("images/bullets/four_pointed_star.png")
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()

        # 初始化子弹的位置
        self.rect.x = self.shooter.rect.x + 111
        self.rect.y = self.shooter.rect.y + 70

        # 设置子弹的移动速度
        self.speed = 5.5
        # 因为图像是以中心点为轴心旋转的，所以要以centery来计算图像的移动
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)
        
        # 设置自转角度
        self.angle = 0.0

          # 为每个子弹标记一个序号（默认为1）
        self.id = 1

    def set_id(self, id):
        """设置每个散弹的id为一个正整数"""
        self.id = id
       
    def initialize_flight_path(self):
        """根据其序号，设置该子弹的飞行速度及运动方向"""
        # 设置四角星子弹在x,y轴上的移动速度
        if self.id == 1 or self.id == 9:
            self.x_speed = 0
            self.y_speed = 2
        elif self.id == 2 or self.id == 8 or self.id == 10 or self.id == 16:
            self.x_speed = 0.5
            self.y_speed = 1.5
        elif self.id == 3 or self.id == 7 or self.id == 11 or self.id == 15:
            self.x_speed = 1
            self.y_speed = 1
        elif self.id == 4 or self.id == 6 or self.id == 12 or self.id == 14:
            self.x_speed = 1.5
            self.y_speed = 0.5
        elif self.id == 5 or self.id == 13:
            self.x_speed = 2
            self.y_speed = 0

        # 设置子弹的移动方向
        if self.id >= 0 and self.id <= 5:
            self.x_direction = 1
            self.y_direction = 1
        elif self.id >= 6 and self.id <= 9:
            self.x_direction = 1
            self.y_direction = -1
        elif self.id >= 10 and self.id <= 13:
            self.x_direction = -1
            self.y_direction = -1
        elif self.id >= 14 and self.id <= 16:
            self.x_direction = -1
            self.y_direction = 1

    def update(self):
        """更新子弹的位置"""
        self.centerx += self.x_speed * self.x_direction
        self.centery += self.y_speed * self.y_direction
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

        # 旋转图像角度
        self._rotate_itself()

    def _rotate_itself(self):
        """让四角星子弹自转"""
        # 重新加载图片
        self.image = pygame.image.load("images/bullets/four_pointed_star.png")
        self.image = self.image.convert_alpha()
        # 旋转图片
        self.image = pygame.transform.rotate(self.image, self.angle)
        # 以图像的中心点为旋转轴心
        self.rect = self.image.get_rect(center=self.rect.center)
        # 递增角度
        self.angle = self.angle % 360 + 10
    
    def blitme(self):
        """在屏幕上绘制子弹"""
        self.ai_game.screen.blit(self.image, self.rect)


