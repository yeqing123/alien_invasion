import sys
import json
import pygame
import random
import threading
from pathlib import Path
from time import sleep
from random import randint
from apscheduler.schedulers.background import BackgroundScheduler
from functools import partial

from settings import Settings
from game_stats import GameStats
from ship import Ship
from alien import Alien
from button import Button
from scoreboard import Scoreboard
from sounds_player import SoundsPlayer
from game_bg_image import GameBgImage
from explosion_effect import ExplosionEffect
from alien_boss_1 import AlienBoss_1
from victory_text import VictoryText
from supply_package import SupplyPackage

class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.settings = Settings()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Alien Invasion")

        # 初始化游戏所需的各类资源
        self.stats = GameStats(self)
        # SoundsPlayer要在Scoreboard类之前创建，因为后者的定义中会用到前者的实例
        self.player = SoundsPlayer()
        self.ship = Ship(self)
        self.sb = Scoreboard(self)
        self.bg_image = GameBgImage(self)
        self.victory_text = VictoryText(self)

        self.explosion = ExplosionEffect(self)
        self.ship_bullets = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.packages = pygame.sprite.Group()
        # 创建任务调度器
        self.scheduler = BackgroundScheduler()
        
        # 创建Play按钮
        self.play_button = Button(self, 'Play')
        
        # 飞船是否已被击毁
        self.ship_destroy = False

        # 游戏是否启动
        self.game_active = False

        self.boss_1 = None
        # 提示是否出现Boss
        self.show_boss = False
        # 提示是否胜利
        self.victory = False

        # 提示补给包是否已经出现
        self.show_package = False

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()

            if self.game_active:
                self.bg_image.update()
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._update_packages()
                if self.boss_1 and self.boss_1.blood_volume > 0:
                    self.boss_1.update()

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
            elif event.type == self.explosion.SHOW_IMAGE_EVENT:
                # 事件触发说明爆炸延迟时间已到
                self.explosion.show_image = False
            elif self.boss_1:  
                # 注意：这一判断一定要放在最后，否则放在它后面的事件都会被忽略
                self._check_boss_events(event)

    def _check_boss_events(self, event):
        """检测AlienBoss对象触发的事件"""
        if event.type == self.boss_1.FIRE_BULLET_EVENT and \
                self.boss_1.blood_volume > 0:
            self.boss_1.fire_ordinary_bullet()
        elif event.type == self.boss_1.FIREFULL_EVENT and \
                self.boss_1.blood_volume > 0:
            self.boss_1.begin_dive = True

    def _check_play_button(self, mouse_pos):
        """在玩家点击Play按钮时开始游戏"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)  
        if button_clicked and not self.game_active:
            self._start_game()

    def _start_game(self):
        """游戏开始"""
        # 重置游戏开始的所有状态
        self.stats.reset_stats()
        # 将需要再屏幕上显示的状态信息渲染为图像
        self.sb.prep_images()
        self.game_active = True

        # 清空外星人列表和子弹列表
        self.ship_bullets.empty()
        self.alien_bullets.empty()
        self.aliens.empty()

        # 创建一支外星舰队
        self._create_fleet()
      
        # 将飞船放置在屏幕底部的中央
        self.ship_destroy = False
        self.ship.ship_center()
        # 开始播放背景音乐
        self.player.play('bg_music_2', -1, 0.1)

        # 隐藏光标
        pygame.mouse.set_visible(False)
        # 完成动态设置初始化
        self.settings.initialize_dynamic_settings()

        self.ship.turn_on_stealth_mode()

        self.rocket_package = SupplyPackage(self, "images/rocket_package.png", 'rocket')
        self.packages.add(self.rocket_package)
        self.show_package = True

    def _close_game(self):
        """如果最高得分被刷新，则保存在文件中，然后退出游戏"""
        saved_high_score = self.stats.get_saved_high_score()
        if saved_high_score < self.stats.high_score:
            path = Path('high_score.json')
            contents = json.dumps(self.stats.high_score)
            path.write_text(contents)

        self.scheduler.shutdown()
        sys.exit()

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

    def _update_bullets(self):
        """更新屏幕上所有子弹的位置，并删除已飞出屏幕顶部的子弹"""
        # 更新所有子弹的位置
        self.ship_bullets.update()
        self.alien_bullets.update()
        if self.show_boss:
            self.boss_1.bombs.update()
            self.boss_1.ordinary_bullets.update()

        # 删除已消失的子弹
        for bullet in self.ship_bullets.copy():
            if bullet.rect.bottom <= 0:
                self.ship_bullets.remove(bullet)

        for bullet in self.alien_bullets.copy():
            if bullet.rect.top > self.screen.get_rect().bottom:
                self.alien_bullets.remove(bullet)

        if self.show_boss:
            for bullet in self.boss_1.bombs.sprites().copy():
                if bullet.rect.top > self.screen.get_rect().bottom:
                    self.boss_1.bombs.remove(bullet)

            for bullet in self.boss_1.ordinary_bullets.sprites().copy():
                if bullet.rect.top > self.screen.get_rect().bottom:
                    self.boss_1.ordinary_bullets.remove(bullet)


    def _check_package_ship_collisitions(self):
        """检测补给包与飞船发生碰撞，并做出响应"""
        collided_package = pygame.sprite.spritecollideany(self.ship, self.packages)
        if collided_package:
            print("发生碰撞了！")
            self.player.play('enhance', 0, 1)
            self._enhance_ship(collided_package)
            self.packages.remove(collided_package)

    def _enhance_ship(self, package):
        print("调用_enhance_ship()")
        if package.type == 'rocket':
            print("OK!!!")
            self.scheduler.add_job(self.ship.launch_missile, 'interval', seconds=3)
            self.scheduler.start()

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
        while current_y < (self.settings.screen_height - 7 * alien_height):
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
                for alien in aliens:
                    # 设置外星人被继承的效果
                    self._alien_hit(alien)

            # 如果舰队全部被消灭，就将游戏递增一个新的子层次
            if not self.aliens:
                self._winding_level()

    def _alien_hit(self, alien):
        """创建一个外星人被击中的效果"""
        self.player.play('explode', 0, 1)
        self.explosion.set_effect(alien.rect.x, alien.rect.y)
        self.aliens.remove(alien)

    def _winding_level(self):
        """将游戏提升一个新的等级"""
        # 删除现有子弹，并创建一支新的外星舰队
        self.ship_bullets.empty()
        self.alien_bullets.empty()
        self._create_fleet()
        # 加快游戏节奏
        self.settings.increase_speed()
        # 提升游戏水平
        self.stats.level += 1
        self.sb.prep_level()
        print(f"sublevel = {self.stats.level}")
        # 当水平提升到2时，Boss出现。同时创建子弹包，用于强化飞船活力
        if self.stats.level == 2:
            self.boss_1 = AlienBoss_1(self)
            
            self.show_boss = True
            self.show_package = True

    def _set_boss_explosions_range(self):
        """根据Boss所在为值，获得其连续爆炸的随机位置"""
        # 设置爆炸点范围的最小值
        self.min_x = self.boss_1.rect.x + self.explosion.rect.width
        self.min_y = self.boss_1.rect.y + self.explosion.rect.height
        # 设置爆炸点范围的最小值
        self.max_x = self.boss_1.rect.x + self.boss_1.rect.width - \
            self.explosion.rect.width
        self.max_y = self.boss_1.rect.y + self.boss_1.rect.height - \
            self.explosion.rect.height

    def _check_boss_hit(self):
        """检查Boss是否被飞船发射的子弹击中"""
        # 检测Boss是否与飞船的子弹发生了碰撞
        collied_any = pygame.sprite.spritecollideany(
            self.boss_1, self.ship_bullets)
        
        # 如果碰撞了，就高亮Boss，并删除子弹
        if collied_any:
            self.boss_1.high_light = True
            self.boss_1.boss_high_light()
            self.ship_bullets.remove(collied_any)
            # 每次Boss被击中都会掉血
            self.boss_1.blood_volume -= 1
        
            # 每当Boss被子弹击中，都判断其血量是否已耗尽
            if self.boss_1.blood_volume == 0:
                # 设置连续爆炸的次数
                self.number = 10
                # 设置连续爆炸位置区间
                self._set_boss_explosions_range()
                # 创建连续爆炸效果
                self._boss_end()
                
    def _boss_end(self):
        """以递归方式设置多线程定时器，制造Boss的连续爆炸效果"""
        # 如果number小于等于0，则制造最后的一次大爆炸效果，然后结束递归
        if self.number <= 0:
            self._last_big_explosion()
            self.alien_bullets.empty()
            self.aliens.empty()
            self.show_boss = False
            sleep(5)
            self._victory_effect()
            return
    
        # 每递归一次，number就减1
        self.number -= 1
        # 播放音效
        self.player.play('boss_explode', 0, 0.5)
        # 以随机方式设置连续爆炸的位置，并设置爆炸图片显示的延迟时间
        self.explosion.set_effect(
            randint(self.min_x, self.max_x), randint(self.min_y, self.max_y), 200)

        # 创建多线程定时器，每隔0.3秒执行一次self._boss_end()函数,
        # 直到number小于等于0为止
        timer = threading.Timer(0.3, self._boss_end)
        timer.start()

    def _last_big_explosion(self):
        """创建Boss最后一次大爆炸的效果"""
        # 加载新的爆炸图片
        self.explosion.load_image("images/big_explosion.png")
        # 设置图片的显示的位置和延迟时间
        self.explosion.set_effect(
            self.boss_1.rect.x + 50, self.boss_1.rect.y + 30, 1000)
        # 播放爆炸音效
        self.player.play('boss_explode', 0, 1)
        # 设定在3.1秒后恢复默认的爆炸效果（3.1秒正好是10次连续爆炸持续时间的总和多一点点）
        timer = threading.Timer(3.1, self.explosion.reset)
        timer.start()

    def _victory_effect(self):
        """每当打败Boss都会播放的胜利效果"""
        self.victory = True
        self.player.stop()
        self.player.play('victory', -1, 1)


    def _check_ship_hit(self):
        """检查飞船是否被击中（与外星人发生碰撞或有外星人到达屏幕底部），并做出响应"""
        # 判断是否有外星人到达了屏幕底部
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.screen.get_rect().height:
                self.ship_destroy = True
                sleep(2)
                self._ship_hit()
                # 因为已经重启了一局，所以for循环无需再继续
                break

        # 获取与飞船发生碰撞的子弹
        collided_bullet = pygame.sprite.spritecollideany(
            self.ship, self.alien_bullets)
        
        # 获取与飞船发生碰撞的外星人
        collided_alien = pygame.sprite.spritecollideany(
            self.ship, self.aliens)
        
        # 当飞船与子弹碰撞时，做出相应的操作
        if collided_bullet and not self.ship_destroy:
            self.alien_bullets.remove(collided_bullet)
            self._ship_destroyed() 

        # 当飞船与外星人碰撞时，做出相应的操作
        if collided_alien and not self.ship_destroy:
            self.aliens.remove(collided_alien)
            self._ship_destroyed()

        # 如果Boss已经出现，则检测飞船是否被Boss发射的子弹击中
        if self.show_boss:
            self._check_boss_bullet_hits_ship()

    def _check_boss_bullet_hits_ship(self):
        """检查Boss的子弹命中飞船"""
        # 检测与飞船发生碰撞的Boss子弹
        collided_bullet = pygame.sprite.spritecollideany(
            self.ship, self.boss_1.ordinary_bullets)
        collided_bomb = pygame.sprite.spritecollideany(
            self.ship, self.boss_1.bombs)
        
        # 当飞船与子弹碰撞时，做出相应的操作
        if collided_bullet and not self.ship_destroy:
            self.boss_1.ordinary_bullets.remove(collided_bullet)
            self._ship_destroyed()

        if collided_bomb and not self.ship_destroy:
            self.boss_1.bombs.remove(collided_bomb)
            self._ship_destroyed()

    def _ship_destroyed(self):
        """响应飞船被击毁"""
        # 播放声音
        self.player.play('explode', 0, 1)
        # 设置爆炸图片显示的正确位置
        self.explosion.set_effect(self.ship.rect.x, self.ship.rect.y)
        self.ship_destroy = True
        # 设置多线程定时器，延迟三秒后将执行self._ship_hit()方法
        self.timer = threading.Timer(3, self._ship_hit)
        # 定时器启动
        self.timer.start()

    def _ship_hit(self):
        """当飞船被击中时，做出响应"""
        print("时间到，重整旗鼓！")
        # 如果还有备用飞船，开启新一局游戏，否则结束游戏
        if self.stats.ship_left > 0:
            # 启用一搜备用飞船
            self.stats.ship_left -= 1
            # 刷新剩余飞船的图像，然后开启新的一局
            self.sb.ships.empty()          
            self.aliens.empty()
            self.ship_bullets.empty()
            self.alien_bullets.empty()
            if self.boss_1:  
                self.boss_1.bombs.empty()
                self.boss_1.ordinary_bullets.empty()
            self.sb.prep_ships()
            self.ship.ship_center()
            self.ship_destroy = False
            self._create_fleet()
        else:
            self.player.stop()  # 背景音乐停止播放
            self.game_active = False
            pygame.mouse.set_visible(True)  

    def _alien_fire_bullet(self):
        """外星人发射子弹"""
        if len(self.alien_bullets) == 0:
            number = 0
            # 每次循环时都要判断一下aliens是否为空，
            # 因为在游戏运行时_ship_hit()函数随时都可能被调用，从而清空aliens
            while number < self.settings.bullet_allow and len(self.aliens) > 0:
                index = random.randint(0, len(self.aliens) - 1)
                alien = self.aliens.sprites()[index]
                alien.fire_bullet()
                number += 1

    def _update_aliens(self):
        """更新所有外星人的位置，并对其相关事件做出响应"""
        self.aliens.update()
        self._alien_fire_bullet()
        self._check_fleet_edges()
        self._check_alien_bullet_collisions()
        if self.show_boss:
            self._check_boss_hit()  
        if not self.ship.stealth_mode:
            self._check_ship_hit()
        
    def _update_packages(self):
        """更新屏幕上消失的补给包"""
        # 更新所有补给包的位置
        self.packages.update()
        # 检测补给包是否与飞船发生碰撞
        self._check_package_ship_collisitions()
        # 删除已经消失的补给包
        for package in self.packages.sprites().copy():
            if package.rect.top > self.screen_rect.bottom:
                self.packages.remove(package)

    def _update_screen(self):
        """更新屏幕上的图像"""
        self.bg_image.blitme()
        self.aliens.draw(self.screen)
        self.ship_bullets.draw(self.screen)
        if not self.ship_destroy:
            self.ship.blitme()
        for bullet in self.alien_bullets.sprites():
            bullet.draw_bullet()
        
        if self.show_boss:
            if self.boss_1.drop_bomb_done:
                self.boss_1.bombs.draw(self.screen)
            self.boss_1.ordinary_bullets.draw(self.screen)
            self.boss_1.blitme()

        self.explosion.blitme()
        self.packages.draw(self.screen)
        self.sb.ships.draw(self.screen)
        self.sb.show_score()
        # 如果游戏处于非活动状态，就绘制Play按钮
        if not self.game_active:
            self.play_button.draw_button()

        if self.victory:
            self.victory_text.blitme()

        # 显示窗口
        pygame.display.flip()
  

if __name__  == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()