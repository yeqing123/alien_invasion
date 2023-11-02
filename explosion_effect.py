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

        # 自定义事件
        self.SHOW_IMAGE_EVENT = pygame.USEREVENT + 1

    def load_image(self, filepath):
        """重新加载指定路径上的爆炸图片"""
        self.image = pygame.image.load("images/big_explosion.png")
        self.rect = self.image.get_rect()

    def reset(self):
        """重置爆炸图片为默认效果图"""
        self.image = pygame.image.load("images/Progear_FireExplosions.png")
        self.rect = self.image.get_rect()
        pygame.time.set_timer(self.SHOW_IMAGE_EVENT, 150, True)

    def set_effect(self, x_position, y_position, image_delay=150):
        """设置爆炸效果图的位置，x_position和y_position表示图像rect对象的x,y值"""
        # 设置爆炸点位
        self.rect.x = x_position
        self.rect.y = y_position
        self.show_image = True

        # 设置爆炸延迟时间，当延迟时间一到就发送一个事件
        pygame.time.set_timer(self.SHOW_IMAGE_EVENT, image_delay, True)
    
    def blitme(self):
        """在屏幕上显示图片"""
        # 爆炸图片只在延迟时间内显示
        if self.show_image:
            self.screen.blit(self.image, self.rect)
        
           