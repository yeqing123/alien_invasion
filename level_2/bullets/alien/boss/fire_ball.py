import pygame

from pygame.sprite import Group
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

        self.image = pygame.image.load("images/bullets/fire_ball.png")
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()

        # 设置子弹的初始位置
        self.rect.centerx = self.shooter.rect.left + 133
        self.rect.centery = self.shooter.rect.top + 183

        # 子弹在y轴上的移动速度
        self.y_speed = 2.0

        self.y = float(self.rect.y)

        # 存放散弹的编组
        self.shotguns = Group()
        # 设置散弹的序号（默认从1开始）
        self.number = 1

        # 记录自己移动的距离
        self.move_distance = 0

    def fire_ball_burst(self):
        """火球炸裂变成16个分散的小子弹"""
        # 当火球向下移动了150个像素后，就要炸裂成16个向四面散开的散弹
        if self.move_distance >= 150:
            # 播放声音效果
            self.ai_game.player.play('launch_shotgun', 0, 1)
            # 因为炸裂后火球就要消失，所以要从编组中删除火球
            self.shooter.bullets.remove(self)
            
            # 创建16个小散弹
            self.number = 1
            while(self.number < 17):
                new_bullet = ShotBullet(self.ai_game, self)
                # 为每个散弹设置一个id
                new_bullet.set_id(self.number)
                # 因为每个散弹的移动方向不同，所以要初始化它们的飞行路线
                new_bullet.initialize_flight_path()
                # 加入编组
                self.shooter.bullets.add(new_bullet)
                self.number += 1
            
            # 重置移动距离
            self.move_distance = 0

    def update(self):
        """更新火球的位置"""
        self.y += self.y_speed
        self.rect.y = self.y
        self.move_distance += self.y_speed