import pygame

class Settings:
    """存储游戏《外星人入侵》中所有设置的类"""

    def __init__(self):
        """初始化游戏的静态设置"""   
        # 屏幕的设置
        self.screen_width = 720
        self.screen_height = 1000
        self.bg_color = (230, 230, 230)

        # 设置备用飞船数量
        self.ship_limit = 3  
        # 设置飞船子弹速度
        self.ship_bullet_speed = 5.5   

        # 设置自定义事件的序列(从0开始，每创建一个自定义事件都加1)
        self.event_order = 0

        # 设置补给包的移动速度
        self.sp_speed = 1.5
        # 设置补给包移动的方向
        self.sp_direction = 1

    def get_custom_events(self):
        """创建一个新的自定义事件"""
        self.event_order += 1
        return pygame.USEREVENT + self.event_order