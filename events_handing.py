import pygame
import sys
import json

from pathlib import Path

class EventsHanding:
    """负责游戏中按键、鼠标等事件的检测和处理"""

    def __init__(self, game):
        """初始化类中要用到的属性"""
        self.game = game
        self.stats = game.stats
        self.explosion = game.explosion
        self.ship = game.ship
        self.continue_button = game.continue_button
        self.restart_button = game.restart_button

    def check_events(self): 
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
        # 如果玩家点击了“继续”按钮，就执行主程序的start_game()函数进入下一关
        if self.continue_button.rect.collidepoint(mouse_pos):
            self.game.main.start_game()
        # 如果玩家点解了“重新开始”按钮，就再次执行当前层级的start_game()函数
        elif self.restart_button.rect.collidepoint(mouse_pos):
            self.game.start_game()

    def _check_keydown_events(self, event):
        """响应按下按键"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP and self.stats.level >= 2:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN and self.stats.level >= 2:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
                self.ship.launch_shotguns()
        elif event.key == pygame.K_q:
            self._close_game()
        
    def _check_keyup_events(self, event):
        """响应释放按键"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False 
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

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

   