import pygame

class GameBgImage_2:
    """负责管理游戏的背景图片的类"""

    def __init__(self, ai_game):
        """初始化所需的各项属性"""
        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        #加载并生成两张背景图像的image对象
        self.image_1 = pygame.image.load('images/bg_images/img_bg_level_2.jpg')
        self.image_2 = pygame.image.load('images/bg_images/img_bg_level_2.jpg')

         # 对图片进行优化处理
        self.image_1 = self.image_1.convert_alpha()
        self.image_2 = self.image_2.convert_alpha()
        
        self.rect_1 = self.image_1.get_rect()
        self.rect_2 = self.image_2.get_rect()

        # 设置图片的位置，并让两张图像上下拼接
        self.rect_1.midbottom = self.screen_rect.midbottom
        self.rect_2.midbottom = self.rect_1.midtop
        
        # 设置为浮点类型，便于增加计算精度
        self.top_1 = float(self.rect_1.top)
        self.top_2 = float(self.rect_2.top)

    def update(self):
        """更新两张背景图像的位置，让其呈现连续滚动的效果"""
        # 在滚动过程中当上面的图片的顶部到达屏幕上边缘，则将最下面的图片换到上面去
        # 重新拼接。这样不断的调换，就呈现处图片连续滚动的效果
        if (self.rect_2.top >= self.screen_rect.top and 
            self.rect_2.midbottom == self.rect_1.midtop):

            self.rect_1.midbottom = self.rect_2.midtop
            self.top_1 = float(self.rect_1.top)

        if (self.rect_1.top >= self.screen_rect.top and 
            self.rect_1.midbottom == self.rect_2.midtop):

            self.rect_2.midbottom = self.rect_1.midtop
            self.top_2 = float(self.rect_2.top)
        
        # 更新两张图片的位置
        self.top_1 += self.settings.bg_speed
        self.top_2 += self.settings.bg_speed
        self.rect_1.top = self.top_1
        self.rect_2.top = self.top_2

    def blitme(self):
        """在屏幕中显示图片"""
        self.screen.blit(self.image_1, self.rect_1)
        self.screen.blit(self.image_2, self.rect_2)