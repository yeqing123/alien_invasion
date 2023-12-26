import pygame

from pygame.sprite import Sprite
from level_2.bullets.alien.boss.shot_bullet import ShotBullet

class FireBall(Sprite):
    """创建一个Boss发射的火球状子弹"""
    
    def __init__(self, shooter):
        """初始化各类属性"""
        super().__init__()

        self.shooter = shooter
        self.ai_game = shooter.ai_game
        self.screen = self.ai_game.screen

        # 先从缓存中提取
        self.image = self.ai_game.image_cacha.get('fire_ball')
        if not self.image:
            self.image = pygame.image.load("images/bullets/fire_ball.png")
            # 存入缓存中
            self.ai_game.image_cacha['fire_ball'] = self.image

        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()

        # 设置子弹的初始位置
        self.rect.centerx = self.shooter.rect.left + 133
        self.rect.centery = self.shooter.rect.top + 183

        # 子弹在y轴上的移动速度
        self.y_speed = 2.0

        self.y = float(self.rect.y)

        # 设置散弹的序号（默认从1开始）
        self.number = 1

        # 记录自己移动的距离
        self.move_distance = 0

    def fire_ball_burst(self):
        """火球炸裂变成16个分散的小子弹"""
        # 当火球向下移动了150个像素后，就要炸裂成16个向四面散开的散弹
        if self.move_distance >= 150:
            # 因为炸裂后火球就要消失，所以要从编组中删除火球
            self.shooter.shotguns.remove(self)
            
            # 创建16个小散弹
            self.number = 1
            while(self.number < 17):
                try:
                    # 从列表末尾弹出一个闲置的ShotBullet对象
                    shotgun = self.shooter.idle_shotguns.pop()
                    # 重置该散弹的初始位置
                    shotgun.initialize_position(self)
                except IndexError:  # 如果列表为空，就创建一个新的对象
                    shotgun = ShotBullet(self.ai_game, self)
            
                # 为散弹设置id值
                shotgun.set_id(self.number)
                # 初始化它的飞行路线
                shotgun.initialize_flight_path()
                # 加入编组
                self.shooter.shotguns.add(shotgun)
                self.number += 1
            
            # 重置移动距离
            self.move_distance = 0

    def update(self):
        """更新火球的位置"""
        self.y += self.y_speed
        self.rect.y = self.y
        self.move_distance += self.y_speed