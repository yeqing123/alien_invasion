import pygame
import random
import threading

from time import sleep
from random import randint
from apscheduler.schedulers.background import BackgroundScheduler

from ship import Ship
from level_2.settings import Settings
from level_2.game_bg_image import GameBgImage_2
from level_2.aliens.alien_1 import Alien_1
from level_2.aliens.alien_2 import Alien_2
from level_2.aliens.alien_3 import Alien_3
from level_2.aliens.alien_4 import Alien_4
from level_2.aliens.alien_boss_2 import AlienBoss_2
from supply_packages.missile_package import MissilePackage
from supply_packages.stealth_package import StealthPackage
from level_2.bullets.ship.ship_missile import ShipMissile
from level_2.bullets.alien.smart_red_bullet import SmartRedBullet

class Level_2:
    """管理游戏资源和行为的类"""

    def __init__(self, main):
        """初始化游戏并创建游戏资源"""
        self.main = main
        self.settings = Settings()
        self.stats = main.stats
        self.screen = main.screen
        self.screen_rect = main.screen_rect
        self.explosion = main.explosion
        self.continue_button = main.continue_button
        self.sb = main.sb
        self.packages = main.packages
        self.ship_bullets = main.ship_bullets
        # SoundsPlayer要在Scoreboard类之前创建，因为后者的定义中会用到前者的实例
        self.player = main.player
        self.game_text = main.game_text
        self.bg_image = GameBgImage_2(self.main)
        self.clock = pygame.time.Clock()

        # 创建存放外星人子弹的编组
        self.alien_bullets = pygame.sprite.Group()
        # 创建存放外星人的编组
        self.aliens = pygame.sprite.Group()  
        
        # 创建一个任务调度器，并立即启动
        self.scheduler = BackgroundScheduler()
       
        self.scheduler.start()
        
        self.boss_2 = None
        # 提示是否出现Boss
        self.show_boss = False
        # 提示是否胜利
        self.victory = False
        # 提示游戏结束
        self.game_over = False

        # 提示补给包是否已经出现
        self.show_package = False

        self.packages.add(StealthPackage(self))

        self.show_package = True
        # 设置飞船是否给销毁
        self.ship_destroy = False
        # 创建本关卡的飞船
        self.ship = Ship(self)

    def run_game(self):
        """开始游戏的主循环"""
        self._start_game()
        print("第二关开始运行！")
        while True:
            self.main._check_events()

            if self.main.game_active:
                self.bg_image.update()
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._update_packages()
                if self.boss_2 and self.boss_2.blood_volume > 0:
                    self.boss_2.update()

            self._update_screen()   
            self.clock.tick(60)

    def _start_game(self):
        """游戏开始"""
        # 重置有关设置
        self.settings.initialize_dynamic_settings()
    
        # 清空外星人列表和子弹列表
        self.ship_bullets.empty()
        self.alien_bullets.empty()
        self.aliens.empty()

        # 创建各类外星人
        self._create_all_aliens()

        # 播放背景音乐
        self.player.stop()
        self.player.play('bg_music_2', -1, 0.3)
      
        # 将飞船放置在屏幕底部的中央
        self.ship_destroy = False
        self.show_boss = False
        self.game_over = False
        self.ship.ship_center()

        # 每隔15秒钟就提升一次游戏难度
        self.scheduler.add_job(
            self._increase_difficulty, 'interval', seconds=15)
       
    def _update_bullets(self):
        """更新屏幕上所有子弹的位置，并删除已飞出屏幕顶部的子弹"""
        # 更新所有子弹的位置
        self.ship_bullets.update()
        self.alien_bullets.update()
        if self.show_boss:
            self.boss_2.rotating_bullets.update()
            self.boss_2.shotguns.update()
            self.boss_2.laser.update()

        # 删除已消失的子弹
        for bullet in self.ship_bullets.copy():
            if bullet.rect.bottom <= 0:
                self.ship_bullets.remove(bullet)

        for bullet in self.alien_bullets.copy():
            if bullet.rect.top > self.screen.get_rect().bottom:
                self.alien_bullets.remove(bullet)

        if self.show_boss:
            for bullet in self.boss_2.rotating_bullets.sprites().copy():
                if bullet.rect.top > self.screen.get_rect().bottom:
                    self.boss_2.rotating_bullets.remove(bullet)

            for bullet in self.boss_2.shotguns.sprites().copy():
                if bullet.rect.top > self.screen.get_rect().bottom or \
                        bullet.rect.right > self.screen_rect.right or \
                        bullet.rect.left < 0 or \
                        bullet.rect.bottom < 0: 
                    self.boss_2.shotguns.remove(bullet)

    def _check_package_ship_collisitions(self):
        """检测补给包与飞船发生碰撞，并做出响应"""
        collided_package = pygame.sprite.spritecollideany(
            self.ship, self.packages, pygame.sprite.collide_mask)
        if collided_package:
            # 补给包对飞船做出了相应的增强
            collided_package.enhance_ship()
            # 清除补给包
            self.packages.remove(collided_package)

    def _create_alien_1(self):
        """以随机的方式创建1号外星人"""
        new_alien = Alien_1(self)
        self.aliens.add(new_alien)

    def _create_alien_2(self):
        """创建一个2号外星人"""
        new_alien = Alien_2(self)
        self.aliens.add(new_alien)

    def _create_alien_3(self):
        """以随机方式创造3号外星人"""
        self.alien_3 = Alien_3(self)
        self.aliens.add(self.alien_3)

    def _create_alien_4(self):
        """创建4号外星人"""
        self.alien_4 = Alien_4(self)
        self.aliens.add(self.alien_4)

    def _create_all_aliens(self):
        """添加创建各类外星人的任务，负责创建所有的外星人"""
        print("定时创建所有的外星人！")
        # 定时创建外星人Alien_1
        #self.scheduler.add_job(self._create_alien_1, 'interval', seconds=2)
        # # 定时创建外星人Alien_2
        self.scheduler.add_job(self._create_alien_2, 'interval', seconds=2)
        # # 定时创建外星人Alien_3
        #self.scheduler.add_job(self._create_alien_3, 'interval', seconds=8)
        # 定时创建外星人Alien_4
        #self.scheduler.add_job(self._create_alien_4, 'interval', seconds=10)
    

    def _check_alien_bullet_collisions(self):
        """检查是否有飞船发射的子弹和外星人发生碰撞（即是否中了外星人），并做出响应"""
        # 获取一个以子弹为一个键，以与该子弹碰撞的所有外星人组成的列表为值的字典
        collisions = pygame.sprite.groupcollide(
            self.ship_bullets, self.aliens, True, False, pygame.sprite.collide_mask)
        
        if collisions:
            # 将每个被击落的外星人都得计入得分
            for aliens in collisions.values():
                for alien in aliens:
                    self.stats.score += alien.alien_points
                    self.sb.prep_score()
                    self.sb.check_high_score()
                    # 设置外星人被击中的效果
                    self._alien_hit(alien)

            # 如果舰队全部被消灭，就将游戏递增一个新的子层次
            if not self.aliens:
                self._increase_difficulty()

    def _check_alien_gone(self):
        """检测已经飞出屏幕消失的外星人"""
        for alien in self.aliens.sprites().copy():
            if alien.rect.y > self.screen_rect.height:
                self.aliens.remove(alien)
            elif isinstance(alien, Alien_4):  
                # 当4号外星人回撤后消失在屏幕上方后，删除该外星人
                if alien.reach_nadir and alien.rect.bottom < self.screen_rect.top:
                    self.aliens.remove(alien)

    def _alien_hit(self, alien):
        """创建一个外星人被击中的效果"""
        # 如果是Alien_4被击毁，并且它正在执行开火任务，则需要将该任务删除
        if isinstance(alien, Alien_4):
            if alien.blood_volume > 0:
                alien.blood_volume -= 1
                alien.hight_light = True
            else:
                if self.scheduler.get_job(f"{id(alien)} open fire"):
                    self.scheduler.remove_job(f"{id(alien)} open fire")
                
                self.player.play('explode', 0, 1)
                self.explosion.set_effect(alien.rect.x, alien.rect.y)
                self.aliens.remove(alien)
        else:
            self.player.play('explode', 0, 1)
            self.explosion.set_effect(alien.rect.x, alien.rect.y)
            self.aliens.remove(alien)

    def _increase_difficulty(self):
        """增加游戏难度，并依据条件增加Boss"""
        # 提升游戏难度
        self.stats.difficulty += 1
        self.settings.increase_speed()

        # 当水平提升到5时，Boss出现。同时创建一个补给包，强化飞船火力
        if self.stats.difficulty == 2:
            # 创建Boss
            self.boss_2 = AlienBoss_2(self)
            self.show_boss = True
            self.player.stop()
            self.player.play_multiple_sounds(
                ['boss_2_apear', 'great_war_boss_2'], [0, -1])
           
            # 创建补给包
            self.missile_package = MissilePackage(self)
            self.packages.add(self.missile_package)
            self.show_package = True

    def _set_boss_explosions_range(self):
        """根据Boss所在为值，获得其连续爆炸的随机位置"""
        # 设置爆炸点范围的最小值
        self.min_x = self.boss_2.rect.x + self.explosion.rect.width
        self.min_y = self.boss_2.rect.y + self.explosion.rect.height
        # 设置爆炸点范围的最小值
        self.max_x = self.boss_2.rect.x + self.boss_2.rect.width - \
            self.explosion.rect.width
        self.max_y = self.boss_2.rect.y + self.boss_2.rect.height - \
            self.explosion.rect.height

    def _check_boss_hit(self):
        """检查Boss是否被飞船发射的子弹击中"""
        # 检测Boss是否与飞船的子弹发生了碰撞
        collied_any = pygame.sprite.spritecollideany(
            self.boss_2, self.ship_bullets, pygame.sprite.collide_mask)
        
        # 如果碰撞了，就高亮Boss，并删除子弹
        if collied_any:
            # 如果击中Boss的是导弹，则设置一个爆炸效果
            if isinstance(collied_any, ShipMissile):
                self.player.play('explode', 0, 1)
                self.explosion.set_effect(collied_any.rect.x, collied_any.rect.y)
            self.boss_2.high_light = True
            self.boss_2.boss_high_light()
            self.ship_bullets.remove(collied_any)
            # 每次Boss被击中都会掉血
            self.boss_2.blood_volume -= 1
        
            # 每当Boss被子弹击中，都判断其血量是否已耗尽
            if self.boss_2.blood_volume == 0:
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
            self.boss_2.rect.x + 50, self.boss_2.rect.y + 30, 1000)
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
        self.scheduler.shutdown()

    def _game_over_effect(self):
        """当游戏失败时播放的游戏结束的效果"""
        self.game_over = True
        self.player.stop()
        self.player.play('game_over', 0, 1)

    def _change_fleet_direction(self):
        """改变外星舰队的左右运动方向"""
        for alien in self.alien_team.sprites():
            alien.rect.y += self.subsettings.alien_drop_speed
        self.subsettings.alien_direction *= -1

    def _check_ship_hit(self):
        """检查飞船是否被击中（与外星人发生碰撞或有外星人到达屏幕底部），并做出响应"""
        # 获取与飞船发生碰撞的子弹
        collided_bullet = pygame.sprite.spritecollideany(
            self.ship, self.alien_bullets)
        
        # 获取与飞船发生碰撞的外星人
        collided_alien = pygame.sprite.spritecollideany(
            self.ship, self.aliens, pygame.sprite.collide_mask)
        
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
        collided_shopguns = pygame.sprite.spritecollideany(
            self.ship, self.boss_2.shotguns, pygame.sprite.collide_mask)
        collided_rotating_bullets = pygame.sprite.spritecollideany(
            self.ship, self.boss_2.rotating_bullets, pygame.sprite.collide_mask)
        collided_laser = pygame.sprite.spritecollideany(
            self.ship, self.boss_2.rotating_bullets, pygame.sprite.collide_mask)
        
        # 当飞船与子弹碰撞时，做出相应的操作
        if collided_shopguns and not self.main.ship_destroy:
            self.boss_2.shotguns.remove(collided_shopguns)
            self._ship_destroyed()

        if collided_rotating_bullets and not self.ship_destroy:
            self.boss_2.rotating_bullets.remove(collided_rotating_bullets)
            self._ship_destroyed()

        if collided_laser and not self.ship_destroy:
            self.boss_2.laser.remove(collided_laser)
            self._ship_destroyed()

    def _ship_destroyed(self):
        """响应飞船被击毁"""
        # 播放声音
        self.player.play('explode', 0, 1)
        # 设置爆炸图片显示的正确位置
        self.explosion.set_effect(self.ship.rect.x, self.ship.rect.y)
        self.ship_destroy = True
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
            if self.boss_2:  
                self.boss_2.bombs.empty()
                self.boss_2.shotguns.empty()
            self.sb.prep_ships()
            self.ship.ship_center()
            self.ship_destroy = False
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
        if len(self.aliens) > 0:
            # 屏幕上的子弹最多不超过设置中限定的数量
            while len(self.alien_bullets) < self.settings.alien_bullet_allow:
                index = random.randint(0, len(self.aliens) - 1)
                alien = self.aliens.sprites()[index]
                if not isinstance(alien, Alien_4):
                    alien.fire_bullet()

    def _update_aliens(self):
        """更新所有外星人的位置，并对其相关事件做出响应"""
        self.aliens.update()  
        self._alien_fire_bullet()
        self._check_alien_bullet_collisions()
        self._check_alien_gone()
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
            self.boss_2.update_screen()

        self.explosion.blitme()
        self.packages.draw(self.screen)
        self.sb.ships.draw(self.screen)
        self.sb.show_score()

        if self.victory:
            self.game_text.show_victory_text()
            self.main.continue_button.draw_button()
        if self.game_over:
            self.game_text.show_game_over_text()
            self.main.restart_button.draw_button()

        # 显示窗口
        pygame.display.flip()