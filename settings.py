import pygame

class Settings:
    """存储游戏《外星人入侵》中所有设置的类"""

    def __init__(self):
        """初始化游戏的静态设置"""        
        # 屏幕的设置
        self.screen_width = 720
        self.screen_height = 1000
        self.bg_color = (230, 230, 230)
        self.bg_speed = 1.5
        
        # 飞船的设置
        self.ship_limit = 3

        # 子弹设置
        self.ship_bullet_width = 3
        self.ship_bullet_height = 15
        self.ship_bullet_color = (60, 60, 60)

        self.alien_bullet_color = (255, 0, 0)
        self.alien_bullet_radius = 4.5
        # 允许连续开火次数的上限
        self.bullet_allow = 10

        # 外星人设置
        self.alien_drop_speed = 10
        # 设置得分
        self.alien_points = 1
        
        # 以什么速度加快游戏的节奏
        self.speedup_scale = 1.1
        # 以什么尺度提高得分
        self.score_scale = 1.5

        # 设置自定义事件的序列(从0开始，每创建一个自定义事件都加1)
        self.event_order = 0

        # 设置补给包的移动速度
        self.sp_speed = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化游戏的动态设置"""
        self.ship_speed = 2.5
        self.ship_bullet_speed = 5.5
        self.alien_bullet_speed = 1.5
        self.boss_bullet_speed = 3.5
        self.alien_speed = 1.0
        # 设置外星人移动的方向，1表示向右，-1表示向左
        self.alien_direction = 1
        # 设置外星boss的移动方向
        self.boss_direction = 1
        # 设置补给包移动的方向
        self.sp_direction = 1

    def increase_speed(self):
        """增加动态设置的值，以加快游戏节奏"""
        self.ship_speed *= self.speedup_scale
        self.ship_bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.bullet_allow += 1

        self.alien_points = int(self.alien_points * self.score_scale)

    def get_custom_events(self):
        """创建一个新的自定义事件"""
        self.event_order += 1
        return pygame.USEREVENT + self.event_order