import pygame

class ExplosionEffect:
    """管理外星人爆炸效果的类"""

    def __init__(self, ai_game):
        """初始化爆炸效果图的属性"""
        self.ai_game = ai_game
        self.screen = ai_game.screen

        # 加载图片文件
        self.image = pygame.image.load("images/Progear_FireExplosions.png")
        self.rect = self.image.get_rect()
        # 设置是否显示的标识
        self.show_image = False
        # 设置图片显示延迟时间（以毫秒为单位）
        self.show_image_delay = 150
        self.clock = pygame.time.Clock()

        # 自定义事件
        self.SHOW_IMAGE_EVENT = pygame.USEREVENT + 1

    def set_effect(self, x_position, y_position):
        """设置外星人或飞船爆炸时的显示效果"""
        # 设置爆炸点位
        self.rect.x = x_position
        self.rect.y = y_position
        self.show_image = True
        # 设置爆炸延迟时间，当延迟时间一到就发送一个事件
        pygame.time.set_timer(self.SHOW_IMAGE_EVENT, self.show_image_delay, True)
    
    def blitme(self):
        """在屏幕上显示图片"""
        # 爆炸图片只在延迟时间内显示
        if self.show_image:
            self.screen.blit(self.image, self.rect)
        
           