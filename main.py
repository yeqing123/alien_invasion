import sys
import pygame

from settings import Settings
from button import Button 
from game_stats import GameStats     
from game_begin_background import GameBeginBackground

from level_1.level_1 import Level_1  
from level_2.level_2 import Level_2
  
class Alien_invasion:
    """负责游戏的主程序类的管理"""

    def __init__(self):
        """初始化主程序所需的各类属性"""    
        pygame.init()    
        self.settings = Settings()  
        # 创建游戏窗口，为了提高游戏运行速度使用双缓冲技术
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height), 
            pygame.DOUBLEBUF)
        
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Alien Invasion")  

        # 创建游戏开始界面的背景图像
        self.begin_image = GameBeginBackground(self)
        
        # 创建游戏按钮    
        self.start_button = Button(self, '开始')   
          # 创建管理游戏状态的类
        self.stats = GameStats(self) 
        
    def _check_events(self): 
        """响应按键和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit() 
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_button(mouse_pos)
    
    def _check_button(self, mouse_pos): 
        """在玩家点击Play按钮时开始游戏"""
        if self.start_button.rect.collidepoint(mouse_pos): 
            self.start_game()

    def start_game(self):
        """游戏开始"""
        # 根据GameStats类中保存的数据，运行相应的关卡
        if self.stats.level == 1:
                Level_1(self).run_game()
        elif self.stats.level == 2:
                Level_2(self).run_game()
        
    def _update_screen(self):       
        """更新游戏开始界面"""
        self.begin_image.blitme()
        self.start_button.draw_button()  
        # 显示窗口
        pygame.display.flip()
 
    def main(self):
        while True:
            self._check_events()
            self._update_screen()

if __name__  == '__main__':
    Alien_invasion().main()