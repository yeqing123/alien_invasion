import pygame

from pygame.sprite import Sprite

class ShipRocket(Sprite):
    """负责管理飞船发射的火箭弹"""
    
    def __init__(self, ship, direction):
        """初始化各类属性"""
        super().__init__()
        self.ship = ship
        self.flight_speed = 4.5

        self.image = pygame.image.load('images/rocket.png')
         # 对图片进行优化处理
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = self.ship.rect.center

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # 设置导弹在x轴上的运动方向，0表示在x轴上不移动，-1表示向左，1表示向右
        self.x_direction = 0
        # 设置导弹在x轴上的移动速度
        self.x_move_speed = 1.0
        # 设置在x轴上移动的距离(设立设置为15个像素)
        self.x_distance = float(self.ship.rect.width / 2)
        # 初始化x轴移动方向
        self._set_direction(direction)

    def _set_direction(self, direction):
        """
        设置导弹在x轴上的移动方向，direction是一个字符串，
        它的值应该是：‘left’或‘right’，
        分别表示导弹在x轴上向左移动或向右移动，默认为空字符串表示不移动
        """
        if direction == 'left':
            self.x_direction = -1
        elif direction == 'right':
            self.x_direction = 1

    def update(self):
        """更新其位置"""
        # 现在x轴上移动设置好的距离，然后再在y轴上移动
        if self.x_distance > 0:
            print(self.x_direction)
            self.x += self.flight_speed * self.x_direction
            self.rect.x = self.x
            self.x_distance -= self.flight_speed
        else:
            self.y -= self.flight_speed
            self.rect.y = self.y

