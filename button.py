import pygame

class Button:
    """用于在屏幕中绘制一个开始游戏的按钮"""

    def __init__(self, hs_game, msg):
        """初始化用于绘制按钮的资源"""
        self.screen = hs_game.screen
        # 设置按钮和文本的颜色
        self.button_color = (0, 135, 0)
        self.text_color = (255, 255, 255)
        # 设置按钮的尺寸
        self.button_width = 200
        self.button_height = 50
        # 创建一个用于放置按钮的矩形，并将该矩形放置在屏幕中心
        self.rect = pygame.rect.Rect(0, 0, self.button_width, self.button_height)
        self.rect.center = self.screen.get_rect().center
        self.rect.y += 300
        # 创建用于在按钮上渲染文本的Font对象
        self.font = pygame.font.SysFont('fangsong', 48)
        # 按钮只需创建一次
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """在按钮上渲染文本"""
        # pygame是将要渲染的文本作为图像来处理的
        self.msg_image = self.font.render(
            msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        # 文本位置与按钮位置一致
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """在屏幕中绘制一个中颜色填充的按钮，然后再绘制文本"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
        