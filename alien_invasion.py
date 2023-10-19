import sys
import json
import pygame
import random
from time import sleep
from pathlib import Path

from settings import Settings
from game_stats import GameStats
from ship import Ship
from alien import Alien
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.settings = Settings()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # 初始化游戏所需的各类资源
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.ship_bullets = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        
        # 在初始化时创建一支外星舰队
        self._create_fleet()
        
        # 创建Play按钮
        self.play_button = Button(self, 'Play')
        
        # 设置游戏是否启动
        self.game_active = False

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()   
            self.clock.tick(60)

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

    def _check_play_button(self, mouse_pos):
        """在玩家点击Play按钮时开始游戏"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self._start_game()

    def _start_game(self):
        """游戏开始"""
        # 重置游戏状态
        self.stats.reset_stats()
        # 将需要再屏幕上显示的状态信息渲染为图像
        self.sb.prep_images()
        self.game_active = True

        # 清空外星人列表和子弹列表
        self.ship_bullets.empty()
        self.alien_bullets.empty()
        self.aliens.empty()

        # 创建一支外星舰队，并将飞船放在屏幕底部的中央
        self._create_fleet()
        self.ship.ship_center()

        # 游戏开始后隐藏光标
        pygame.mouse.set_visible(False)
        # 初始化动态设置
        self.settings.initialize_dynamic_settings()

    def _close_game(self):
        """如果最高得分被刷新，则保存在文件中，然后退出游戏"""
        saved_high_score = self.stats.get_saved_high_score()
        if saved_high_score < self.stats.high_score:
            path = Path('high_score.json')
            contents = json.dumps(self.stats.high_score)
            path.write_text(contents)
        
        sys.exit()

    def _check_keydown_events(self, event):
        """响应按下按键"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self.ship.fire_bullet()
        elif event.key == pygame.K_q:
            self._close_game()
        
    def _check_keyup_events(self, event):
        """响应释放按键"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    
    def _update_bullets(self):
        """更新所有子弹的位置，并删除已飞出屏幕顶部的子弹"""
        # 更新子弹的位置
        self.ship_bullets.update()
        self.alien_bullets.update()
        # 删除已消失的子弹
        for bullet in self.ship_bullets.copy():
            if bullet.rect.bottom <= 0:
                self.ship_bullets.remove(bullet)
        for bullet in self.alien_bullets.copy():
            if bullet.rect.top > self.screen.get_rect().bottom:
                self.alien_bullets.remove(bullet)

    def _create_alien(self, x_position, y_position):
        """创建一个外星人，并根据实参设置其位置"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _create_fleet(self):
        """创建一支排列整齐的外星舰队"""
        alien = Alien(self)
        # 外星人之间的间距为一个外星人的宽度和高度
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 6 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            # 每添加一行外星人后，重置x值并递增y值
            current_x = alien_width
            current_y += 2 * alien_height

    def _check_fleet_edges(self):
        """检查是否有外星人到达了屏幕两侧边缘，如果有就改变外星舰队的运动方向"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """改变外星舰队的左右运动方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.alien_drop_speed
        self.settings.alien_direction *= -1

    def _check_alien_bullet_collisions(self):
        """检查是否有飞船发射的子弹和外星人发生碰撞（即是否中了外星人），并做出响应"""
        # 获取一个以子弹为一个键，以与该子弹碰撞的所有外星人组成的列表为值的字典
        collisions = pygame.sprite.groupcollide(
            self.ship_bullets, self.aliens, True, True)
        
        if collisions:
            # 将每个被击落的外星人都得计入得分
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                self.sb.prep_score()
                self.sb.check_high_score()
        # 如果舰队全部被消灭，就将游戏递增一个新的等级
        if not self.aliens:
            self._start_new_level()


    def _start_new_level(self):
        """将游戏提升一个新的等级"""
        # 删除现有子弹，并创建一支新的外星舰队
        self.ship_bullets.empty()
        self.alien_bullets.empty()
        self._create_fleet()
        # 加快游戏节奏
        self.settings.increase_speed()
        # 提升玩家的等级
        self.stats.level += 1
        self.sb.prep_level()

    def _check_ship_hit(self):
        """检查飞船是否被击中（与外星人发生碰撞或有外星人到达屏幕底部），并做出响应"""
        # 判断是否有外星人到达了屏幕底部
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.screen.get_rect().height:
                self._ship_hit()
                # 因为已经重启了一局，所以for循环无需再继续
                break
        # 判断子弹是否击中的飞船
        if pygame.sprite.spritecollideany(self.ship, self.alien_bullets):
            self._ship_hit()
        # 判断飞船是否与外星人发生了碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

    def _ship_hit(self):
        """当飞船被击中时，做出响应"""
        # 如果还有备用飞船，开启新一局游戏，否则结束游戏
        if self.stats.ship_left > 0:
            # 启用一搜备用飞船
            self.stats.ship_left -= 1
            # 刷新剩余飞船的图像，然后开启新的一句
            self.sb.prep_ships()
            self.aliens.empty()
            self.ship_bullets.empty()
            self.alien_bullets.empty()  
            self.ship.ship_center()
            self._create_fleet()
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _alien_fire_bulle(self):
        """外星人发射子弹"""
        if len(self.alien_bullets) == 0:
            number = 0
            while number < self.settings.bullet_allow:
                index = random.randint(0, len(self.aliens) - 1)
                alien = self.aliens.sprites()[index]
                alien.fire_bullet()
                number += 1

    def _update_aliens(self):
        """更新所有外星人的位置，并对其相关事件做出响应"""
        self.aliens.update()
        self._alien_fire_bulle()
        self._check_fleet_edges()
        self._check_alien_bullet_collisions()
        # 当有外星人到达屏幕底部，或者与飞船发生碰撞时，做出响应
        self._check_ship_hit()
        
    def _update_screen(self):
        """更新屏幕上的图像"""
        self.screen.fill(self.settings.bg_color)
        self.aliens.draw(self.screen)
        for bullet in self.ship_bullets.sprites():
            bullet.draw_bullet()
        for bullet in self.alien_bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.sb.show_score()
        # 如果游戏处于非活动状态，就绘制Play按钮
        if not self.game_active:
            self.play_button.draw_button()
        # 显示窗口
        pygame.display.flip()
  

if __name__  == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()