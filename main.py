import sys
import json
import pygame

from pathlib import Path
from apscheduler.schedulers.background import BackgroundScheduler

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from explosion_effect import ExplosionEffect
from button import Button
from sounds_player import SoundsPlayer
from ship import Ship
from game_bg_image import GameBgImage
from game_text import GameText
from level_1.level_1 import Level_1

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
        
        # 创建管理游戏状态的类
        self.stats = GameStats(self) 
        # 创建渲染爆炸效果的类
        self.explosion = ExplosionEffect(self)
        # 创建负责播放声音的类
        self.player = SoundsPlayer()
        # 创建管理游戏背景图像的类
        self.bg_image = GameBgImage(self)
        # 创建管理每通过一关后的胜利效果的类
        self.game_text = GameText(self)
        # 创建一个任务调度器
        self.scheduler = BackgroundScheduler()
        # 创建Play按钮
        self.play_button = Button(self, 'Play')
        # 飞船是否已被击毁
        self.ship_destroy = False
        # 创建游戏状态面板
        self.sb = Scoreboard(self)
        # 创建飞船
        self.ship = Ship(self) 

        # 创建三个编组，分别存放飞船的子弹、补给包和所有的外星人
        self.ship_bullets = pygame.sprite.Group()
        self.packages = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()  
        # 表示游戏是否激活
        self.game_active = False
        
        self.level_1 = None
        # 启动任务调度器
        self.scheduler.start()

    def _check_events(self):
        """响应按键和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._close_game()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == self.explosion.SHOW_IMAGE_EVENT:
                # 事件触发说明爆炸延迟时间已到
                self.explosion.show_image = False

    def _check_keydown_events(self, event):
        """响应按下按键"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            if not self.ship_destroy:
                self.ship.fire_bullet()
        elif event.key == pygame.K_q:
            self._close_game()
        
    def _check_keyup_events(self, event):
        """响应释放按键"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False 

    def _check_play_button(self, mouse_pos):
        """在玩家点击Play按钮时开始游戏"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)  
        if button_clicked and not self.game_active:  
            self._start_game() 

    def _close_game(self):
        """如果最高得分被刷新，则保存在文件中，然后退出游戏"""
        saved_high_score = self.stats.get_saved_high_score()
        if saved_high_score < self.stats.high_score:
            path = Path('high_score.json')
            contents = json.dumps(self.stats.high_score)
            path.write_text(contents)
        
        # 关闭任务调度器
        self.scheduler.shutdown()
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
        # 完成动态设置初始化
        self.settings.initialize_dynamic_settings()
        # 开始播放背景音乐
        if self.stats.level == 1:
            self.player.play('bg_music_1', -1, 0.3)
            self.level_1._start_game()

    def main(self):
        if self.stats.level == 1:
            self.level_1 = Level_1(self)
            self.level_1.run_game()

if __name__  == '__main__':
    Alien_invasion().main()