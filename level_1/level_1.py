import pygame
import random
import threading

from time import sleep
from random import randint
from functools import partial

from level_1.alien import Alien
from level_1.alien_boss_1 import AlienBoss_1
from level_1.supply_packages.missile_package import MissilePackage
from level_1.supply_packages.stealth_package import StealthPackage
from level_1.bullets.ship.ship_missile import ShipMissile

class Level_1:
    """管理游戏资源和行为的类"""

    def __init__(self, main):
        """初始化游戏并创建游戏资源"""
        self.main = main
        self.settings = main.settings
        self.stats = main.stats
        self.screen = main.screen
        self.screen_rect = main.screen_rect
        self.explosion = main.explosion
        self.play_button = main.play_button
        self.sb = main.sb
        self.ship = main.ship
        self.packages = main.packages
        self.ship_bullets = main.ship_bullets
        self.aliens = main.aliens
        # SoundsPlayer要在Scoreboard类之前创建，因为后者的定义中会用到前者的实例
        self.player = main.player
        self.scheduler = main.scheduler
        self.bg_image = main.bg_image
        self.game_text = main.game_text
        self.clock = pygame.time.Clock()

        # 创建存放外星人子弹的编组
        self.alien_bullets = pygame.sprite.Group()
        
        self.boss_1 = None
        # 提示是否出现Boss
        self.show_boss = False
        # 提示是否胜利
        self.victory = False
        # 提示游戏结束
        self.game_over = False

        # 提示补给包是否已经出现
        self.show_package = False

        # 创建一支外星舰队
        self._create_fleet()

        self.packages.add(StealthPackage(self))
        self.show_package = True

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self.main._check_events()

            if self.main.game_active:
                self.bg_image.update()
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._update_packages()
                if self.boss_1 and self.boss_1.blood_volume > 0:
                    self.boss_1.update()

            self._update_screen()   
            self.clock.tick(60)

    def _start_game(self):
        """游戏开始"""
        # 清空外星人列表和子弹列表
        self.ship_bullets.empty()
        self.alien_bullets.empty()
        self.aliens.empty()

        # 创建一支外星舰队
        self._create_fleet()
      
        # 将飞船放置在屏幕底部的中央
        self.main.ship_destroy = False
        self.show_boss = False
        self.game_over = False
        self.ship.ship_center()
       
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
            print("补充一个补给包！")
            # 补给包对飞船做出了相应的增强
            collided_package.enhance_ship()
            # 清除补给包
            self.packages.remove(collided_package)

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
        while current_y < (self.settings.screen_height - 8 * alien_height):
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
        # 提升游戏等级
        self.stats.level += 1
        self.sb.prep_level()

        # 当水平提升到3时，Boss出现。同时创建一个补给包，强化飞船火力
        if self.stats.level == 3:
            # 创建Boss
            self.boss_1 = AlienBoss_1(self)
            self.show_boss = True
            # 创建补给包
            self.missile_package = MissilePackage(self)
            self.packages.add(self.missile_package)
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
            # 如果击中Boss的是导弹，则设置一个爆炸效果
            if isinstance(collied_any, ShipMissile):
                self.player.play('explode', 0, 1)
                self.explosion.set_effect(collied_any.rect.x, collied_any.rect.y)
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
        self.scheduler.remove_all_jobs()

    def _game_over_effect(self):
        """当游戏失败时播放的游戏结束的效果"""
        self.game_over = True
        self.player.stop()
        self.player.play('game_over', 0, 1)

    def _check_ship_hit(self):
        """检查飞船是否被击中（与外星人发生碰撞或有外星人到达屏幕底部），并做出响应"""
        # 判断是否有外星人到达了屏幕底部
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.screen.get_rect().height:
                self.main.ship_destroy = True
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
        if collided_bullet and not self.main.ship_destroy:
            self.alien_bullets.remove(collided_bullet)
            self._ship_destroyed() 

        # 当飞船与外星人碰撞时，做出相应的操作
        if collided_alien and not self.main.ship_destroy:
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
        if collided_bullet and not self.main.ship_destroy:
            self.boss_1.ordinary_bullets.remove(collided_bullet)
            self._ship_destroyed()

        if collided_bomb and not self.main.ship_destroy:
            self.boss_1.bombs.remove(collided_bomb)
            self._ship_destroyed()

    def _ship_destroyed(self):
        """响应飞船被击毁"""
        # 播放声音
        self.player.play('explode', 0, 1)
        # 设置爆炸图片显示的正确位置
        self.explosion.set_effect(self.ship.rect.x, self.ship.rect.y)
        self.main.ship_destroy = True
        # 设置多线程定时器，延迟三秒后将执行self._ship_hit()方法
        threading.Timer(3, self._ship_hit).start()
      
    def _ship_hit(self):
        """当飞船被击中时，做出响应"""
        print("时间到，重整旗鼓！")
        # 如果还有备用飞船，开启新一局游戏，否则结束游戏
        if self.stats.ship_left > 0:
            # 启用一搜备用飞船
            self.stats.ship_left -= 1
            # 刷新剩余飞船的图像，然后开启新的一局
            self.sb.ships.empty()          
        #    self.aliens.empty()
            self.ship_bullets.empty()
            self.alien_bullets.empty()
            if self.boss_1:  
                self.boss_1.bombs.empty()
                self.boss_1.ordinary_bullets.empty()
            self.sb.prep_ships()
            self.ship.ship_center()
            self.main.ship_destroy = False
        else:  # 备用飞船全部用完，游戏结束
            self.scheduler.remove_all_jobs()
            self.player.stop()  # 背景音乐停止播放
            sleep(3)
            self.game_over = True
            self.main.game_active = False
            self._game_over_effect()
            pygame.mouse.set_visible(True)  

    def _alien_fire_bullet(self):
        """外星人发射子弹"""
        if len(self.alien_bullets) == 0:
            number = 0
            # 每次循环时都要判断一下aliens是否为空，
            # 因为在游戏运行时_ship_hit()函数随时都可能被调用，从而清空aliens
            while number < 3 and len(self.aliens) > 0:
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
        if not self.main.ship_destroy:
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
        if not self.main.game_active:
            self.play_button.draw_button()

        if self.victory:
            self.game_text.show_victory_text()
        if self.game_over:
            self.game_text.show_game_over_text()

        # 显示窗口
        pygame.display.flip()