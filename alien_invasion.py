import sys
import json
import pygame
from time import sleep
from pathlib import Path

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        
        pygame.display.set_caption("Alien Invasion")
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        # Group实例用于保存和管理多个Sprite对象的容器类
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        # 在初始化时调用该方法，是的游戏刚开始就自动创建一个外星人舰队
        self._create_fleet()
        self.clock = pygame.time.Clock()
        # 标识游戏是否启动
        self.game_active = False
        # 创建Play按钮
        self.play_button = Button(self, 'Play')

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
            # 重置游戏的统计信息
            self.stats.reset_stats()
            # 更新得分信息
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active = True

            # 清空外星人列表和子弹列表
            self.bullets.empty()
            self.aliens.empty()

            # 创建一个新的外星舰队，并将飞船放在屏幕底部的中央
            self._create_fleet()
            self.ship.ship_center()

            # 游戏开始后隐藏光标
            pygame.mouse.set_visible(False)
            # 重置游戏的动态设置
            self.settings.initialize_dynamic_settings()

    def _check_keydown_events(self, event):
        """响应按下按键"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            self._close_game()
        
    def _check_keyup_events(self, event):
        """响应释放按键"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组bullets"""
        if len(self.bullets) < self.settings.bullet_allow:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """更新子弹的位置并删除已经消失的子弹"""
        # 更新子弹的位置
        self.bullets.update()
        # 删除已消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _create_alien(self, x_opsition, y_opsition):
        """创建一个外星人并指定其位置"""
        new_alien = Alien(self)
        new_alien.x = x_opsition
        new_alien.rect.x = x_opsition
        new_alien.rect.y = y_opsition
        self.aliens.add(new_alien)

    def _create_fleet(self):
        """创建一个外星人舰队"""
        # 先创建一个外星人然后不断添加，直至组成一支完整的舰队为止
        # 外星人之间的间距为外星人的宽度和高度
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 6 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            # 添加一行外星人后，重置x值并递增y值
            current_x = alien_width
            current_y += 2 * alien_height

    def _check_fleet_edges(self):
        """在有外星人到达屏幕边缘时做出响应"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """当有外星人到达边缘时，将整个舰队向下移动，并改变它们的方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.alien_drop_speed
        self.settings.alien_direction *= -1

    def _check_alien_bullet_collisions(self):
        """对子弹和外星人的碰撞做出响应"""
        # groupcollide（）方法将返回，以子弹为一个键，
        # 以与该子弹碰撞的所有外星人组成的列表为值的字典
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        # 每击中一个外星人就记录得分
        if collisions:
            # 将每个被击落的外星人都得计入得分
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                self.sb.prep_score()
                self.sb.check_high_score()
        # 如果舰队全部被消灭，就再创建一支舰队
        if not self.aliens:
            # 删除现有子弹，并创建一支新的外星舰队
            self.bullets.empty()
            self._create_fleet()
            # 加快游戏节奏
            self.settings.increase_speed()
            # 提升玩家的等级
            self.stats.level += 1
            self.sb.prep_level()

    def _ship_hit(self):
        """清空屏幕上的外星人和子弹，
        然后重建一支外星人舰队并让飞船居中"""
        if self.stats.ship_left > 0:
            # 每重置一次，就将飞船限额减1，直至限额为0
            self.stats.ship_left -= 1
            # 刷新屏幕上备用飞船的图像
            self.sb.prep_ships()
            self.aliens.empty()
            self.bullets.empty()
            self.ship.ship_center()
            self._create_fleet()
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """当有外星人到达屏幕底部时做出响应"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.screen.get_rect().height:
                self._ship_hit()
                # 因为已经重置，所以for循环无需再继续
                break

    def _update_aliens(self):
        """更新所有外星人的位置，并响应子弹与外星人的碰撞"""
        self._check_fleet_edges()
        self.aliens.update()
        self._check_alien_bullet_collisions()
        # 检查飞船是否与外星人发生了碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()

    def _close_game(self):
        """退出游戏前，保存新的最高得分"""
        saved_high_score = self.stats.get_saved_high_score()
        if saved_high_score < self.stats.high_score:
            path = Path('high_score.json')
            contents = json.dumps(self.stats.high_score)
            path.write_text(contents)
        
        sys.exit()

    def _update_screen(self):
        """更新屏幕上的图像"""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.ship.blitme()
        self.sb.show_score()
        # 如果游戏处于非活动状态，就绘制Play按钮
        if not self.game_active:
            self.play_button.draw_button()
        # 显示窗口
        pygame.display.flip()

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
        

if __name__  == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()