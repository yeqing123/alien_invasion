import sys
import json
import pygame

from pathlib import Path
from apscheduler.schedulers.background import BackgroundScheduler

from game_being_interface_bg import GameBeginInterfaceBG
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from explosion_effect import ExplosionEffect
from button import Button 
from sounds_player import SoundsPlayer
from game_text import GameText
from level_1.level_1 import Level_1  
from level_2.level_2 import Level_2
  
class Alien_invasion:
    """负责游戏的主程序类的管理"""

    def __init__(self):
        """初始化主程序所需的各类属性"""    
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Alien Invasion")  

        # 创建游戏开始界面的背景图像
        self.begin_image = GameBeginInterfaceBG(self)
        # 创建管理游戏状态的类
        self.stats = GameStats(self) 
        # 创建渲染爆炸效果的类
        self.explosion = ExplosionEffect(self)
        # 创建负责播放声音的类
        self.player = SoundsPlayer()
        # 创建管理每通过一关后的胜利效果的类
        self.game_text = GameText(self)
        
        # 创建游戏按钮
        self.start_button = Button(self, '开始')
        self.continue_button = Button(self, '继续')
        self.restart_button = Button(self, '重新开始')

        # 创建一个任务调度器
        self.scheduler = BackgroundScheduler() 
        # 创建游戏状态面板
        self.sb = Scoreboard(self)   

        # 创建两个编组，分别存放飞船的子弹、补给包
        self.ship_bullets = pygame.sprite.Group()
        self.packages = pygame.sprite.Group()
        
        # 表示游戏是否激活
        self.game_active = False
    
        # 设置游戏正在哪一关运行
        self.activing_level = None
    
    def _check_events(self): 
        """响应按键和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._close_game()  
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == self.explosion.SHOW_IMAGE_EVENT:
                # 事件触发说明爆炸延迟时间已到
                self.explosion.show_image = False
 
    def _check_button(self, mouse_pos): 
        """在玩家点击Play按钮时开始游戏"""
        if (self.start_button.rect.collidepoint(mouse_pos) or \
                self.continue_button.rect.collidepoint(mouse_pos) or \
                self.restart_button.rect.collidepoint(mouse_pos) ) and \
                not self.game_active: 
            self._start_game()

    def _check_keydown_events(self, event):
        """响应按下按键"""
        if event.key == pygame.K_RIGHT:
            self.activing_level.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.activing_level.ship.moving_left = True
        elif event.key == pygame.K_UP and self.stats.level >= 2:
            self.activing_level.ship.moving_up = True
        elif event.key == pygame.K_DOWN and self.stats.level >= 2:
            self.activing_level.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
                self.activing_level.ship.fire_bullet()
        elif event.key == pygame.K_q:
            self._close_game()
        
    def _check_keyup_events(self, event):
        """响应释放按键"""
        if event.key == pygame.K_RIGHT:
            self.activing_level.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.activing_level.ship.moving_left = False 
        elif event.key == pygame.K_UP:
            self.activing_level.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.activing_level.ship.moving_down = False

    def _close_game(self):
        """如果最高得分被刷新，则保存在文件中，然后退出游戏"""
        saved_high_score = self.stats.get_saved_high_score()
        if saved_high_score < self.stats.high_score:
            path = Path('high_score.json')
            contents = json.dumps(self.stats.high_score)
            path.write_text(contents)
        
        # 重置游戏等级
        self.stats.level = 1
        sys.exit()

    def _start_game(self):
        """游戏开始"""
        # 重置游戏开始的所有状态
        self.stats.reset_stats()
   
        # 将需要再屏幕上显示的状态信息渲染为图像
        self.sb.prep_images()  
        self.game_active = True
  
        # 隐藏光标  
        pygame.mouse.set_visible(False)
        
        if self.stats.level == 1:
            if not isinstance(self.activing_level, Level_1):
                self.activing_level = Level_1(self)
        elif self.stats.level == 2:
            if not isinstance(self.activing_level, Level_2):
                self.activing_level = Level_2(self)
        
        self.activing_level.run_game()

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