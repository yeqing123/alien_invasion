class Settings:
    """存储游戏《外星人入侵》中所有设置的类"""

    def __init__(self):
        """初始化游戏的静态设置"""        
        # 屏幕的设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        
        # 飞船的设置
        self.ship_limit = 3

        # 子弹设置
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allow = 3

        # 外星人设置
        self.alien_drop_speed = 40
        # 设置得分
        self.alien_points = 50
        
        # 以什么速度加快游戏的节奏
        self.speedup_scale = 1.1
        # 以什么尺度提高得分
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化游戏的动态设置"""
        self.ship_speed = 2.5
        self.bullet_speed = 5.5
        self.alien_speed = 1.0
        # 设置外星人移动的方向，1表示向右，-1表示向左
        self.alien_direction = 1

    def increase_speed(self):
        """增加动态设置的值，以加快游戏节奏"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)