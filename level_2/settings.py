import pygame

class Settings:
    """存储游戏《外星人入侵》中所有设置的类"""

    def __init__(self):
        """初始化游戏的静态设置"""
        # 子弹设置
        self.alien_bullet_color = (255, 0, 0)
        self.alien_bullet_radius = 5
        
        # 以什么尺度来提高每个外星人分值        
        self.score_scale =  1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化游戏的动态设置"""
        # 设置飞船及其子弹移动速度
        self.ship_bullet_allow = 5
        self.ship_speed = 3.5
        self.ship_bullet_speed = 6.5

        # 设置外星人及其子弹移动速度
        self.alien_bullet_speed = 1.5
        self.boss_bullet_speed = 3.5
        self.alien_speed = 1.0
        self.alien_bullet_allow = 5
        
        # 设置外星人移动的方向，1表示向右，-1表示向左
        self.alien_direction = 1
        # 设置外星boss的移动方向
        self.boss_direction = 1

    def increase_speed(self):
        """增加动态设置的值，以加快游戏节奏"""
        print("提升游戏难度！")
        if self.ship_bullet_allow < 10:
            self.ship_bullet_allow += 1

        self.alien_bullet_allow += 1