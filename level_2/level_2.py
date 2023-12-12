import pygame
import random
import threading

from time import sleep
from random import randint
from apscheduler.schedulers.background import BackgroundScheduler

from ship import Ship
from button import Button 
from game_text import GameText
from scoreboard import Scoreboard
from sounds_player import SoundsPlayer
from explosion_effect import ExplosionEffect
from events_handing import EventsHanding
from supply_packages.missile_package import MissilePackage
from supply_packages.stealth_package import StealthPackage

from level_2.settings import Settings
from level_2.sounds_path import sounds_path
from level_2.game_bg_image import GameBgImage_2
from level_2.aliens.alien_1 import Alien_1
from level_2.aliens.alien_2 import Alien_2
from level_2.aliens.alien_3 import Alien_3
from level_2.aliens.alien_4 import Alien_4
from level_2.aliens.alien_boss_2 import AlienBoss_2
from level_2.bullets.ship.ship_missile import ShipMissile
from level_2.bullets.alien.boss.laser_beam import LaserBeam

class Level_2:
    """管理游戏资源和行为的类"""
  
    def __init__(self, main):
        """初始化游戏并创建游戏资源"""
        self.main = main
        self.settings = Settings()
        self.screen = main.screen
        self.stats = main.stats
        self.screen_rect = main.screen_rect


        # 创建管理游戏第二关背景的实例
        self.bg_image = GameBgImage_2(self)
        # 创建渲染爆炸效果的类
        self.explosion = ExplosionEffect(self)
        # 创建管理每通过一关后的胜利效果的类
        self.game_text = GameText(self)
        # 创建负责第二关音效播放的实例
        self.player = SoundsPlayer(sounds_path)
        # 创建游戏进行中用到的按钮
        self.continue_button = Button(self, '继续')
        self.restart_button = Button(self, '重新开始')
        self.clock = pygame.time.Clock()

        # 创建存放飞船的子弹的编组
        self.ship_bullets = pygame.sprite.Group()
        # 创建存放飞船补给包的编组
        self.packages = pygame.sprite.Group()
        # 创建存放外星人的编组
        self.aliens = pygame.sprite.Group()  
        # 将Boss放入一个单独的编组中
        self.boss_group = pygame.sprite.Group()
        # 创建存放外星人子弹的编组
        self.alien_bullets = pygame.sprite.Group()
        
        # 创建一个任务调度器，并立即启动
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

        # 创建显示游戏当前得分面、历史最高分、备用飞船等信息的实例
        self.sb = Scoreboard(self)   
        # 创建本关卡的飞船
        self.ship = Ship(self)
        # 创建Boss，并加入编组（加入编组的目的是为了进行碰撞检测），
        # 因为普通的外星人和Boss有着完全不同的操作模式，如果放在同一个编组中将无法区别，
        # 所以给Boss单独创建一个编组。
        self.boss_2 = AlienBoss_2(self)
        self.boss_group.add(self.boss_2)
        
        # 创建检测并处理事件的类
        self.events_handing = EventsHanding(self)

         # 表示本关游戏是否激活
        self.game_active = False
        # 表示游戏是否结束
        self.game_over = False
        # 表示玩家是否胜利
        self.victory = False
        # 是否显示Boss
        self.boss_show = False


    def run_game(self):
        """开始游戏的主循环"""
        self.start_game()
        print("第二关开始运行！")
        while True:
            self.events_handing.check_events()

            if self.game_active:
                self.bg_image.update()
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._update_packages()
                if self.boss_show and self.boss_2.blood_volume > 0:
                    self.boss_2.update()

            self._update_screen()   
            self.clock.tick(60)

    def start_game(self):
        """游戏开始"""
        self.packages.add(StealthPackage(self))

        # 重置游戏开始的所有状态
        self.stats.reset_stats()
        # 将需要再屏幕上显示的状态信息渲染为图像
        self.sb.prep_images()  
  
        # 隐藏光标  
        pygame.mouse.set_visible(False)
        # 重置有关设置
        self.settings.initialize_dynamic_settings()
    
        # 清空外星人列表和子弹列表
        self.ship_bullets.empty()
        self.alien_bullets.empty()
        self.aliens.empty()

        # 重置Boss的有关属性
        self.boss_2.initialize_state()

        # 创建各类外星人
        self._create_all_aliens()
        # 飞船重新居中
        self.ship.ship_center()

        # 播放背景音乐
        self.player.stop()
        self.player.play('bg_music_2', -1, 0.3)
      
        # 重置有关状态标识
        self.ship_destroy = False
        self.game_over = False
        self.game_active = True
        self.boss_show = False

        # 添加一个任务，每隔15秒钟调用一次self._increase_difficulty()函数，提升游戏难度
        self.scheduler.add_job(
            self._increase_difficulty, 'interval', seconds=15)
       
    def _update_bullets(self):
        """更新屏幕上所有子弹的位置，并删除已飞出屏幕顶部的子弹"""
        # 更新所有子弹的位置
        self.ship_bullets.update()
        self.alien_bullets.update()
        if self.boss_show:
            self.boss_2.bullets.update()

        # 如果子弹已经飞出了屏幕就将其删除
        for bullet in self.ship_bullets.sprites():
            if bullet.rect.bottom < 0: 
                self.ship_bullets.remove(bullet)

        for bullet in self.alien_bullets.sprites():
            if bullet.rect.top > self.screen.get_rect().bottom or \
                    bullet.rect.right > self.screen_rect.right or \
                    bullet.rect.left < 0 or \
                    bullet.rect.bottom < 0: 
                self.alien_bullets.remove(bullet)

        if self.boss_show:
            for bullet in self.boss_2.bullets.sprites():
                if bullet.rect.top > self.screen.get_rect().bottom or \
                        bullet.rect.right > self.screen_rect.right or \
                        bullet.rect.left < 0 or \
                        bullet.rect.bottom < 0: 
                    self.boss_2.bullets.remove(bullet)

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
        # 定时创建外星人Alien_1
        self.scheduler.add_job(self._create_alien_1, 'interval', seconds=2)
        # 定时创建外星人Alien_2
        self.scheduler.add_job(self._create_alien_2, 'interval', seconds=3)
        # # # 定时创建外星人Alien_3
        # if self.stats.difficulty == 2:
        #     self.scheduler.add_job(self._create_alien_3, 'interval', seconds=8)
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

    def _check_alien_gone(self):
        """检测已经飞出屏幕消失的外星人"""
        for alien in self.aliens.sprites():
            # 普通外星人会在屏幕下方消失
            if alien.rect.y > self.screen_rect.height:
                self.aliens.remove(alien)

            elif isinstance(alien, Alien_4):  # 如果是4号外星人，它会消失在屏幕上方
                if alien.reach_nadir and alien.rect.bottom < self.screen_rect.top:
                    self.aliens.remove(alien)

    def _alien_hit(self, alien):
        """创建一个外星人被击中的效果"""
        # 如果是Alien_3或者Alien_4被击毁，并且它正在执行开火任务，则需要将该任务删除
        if isinstance(alien, Alien_4) or isinstance(alien, Alien_3):
            if alien.blood_volume > 0:
                alien.blood_volume -= 1
                alien.hight_light = True
            else:
                # 移除开火的任务
                if self.scheduler.get_job(f"{id(alien)} open fire"):
                    self.scheduler.remove_job(f"{id(alien)} open fire")
                # 渲染爆炸效果
                self.player.play('explode', 0, 1)
                self.explosion.set_effect(alien.rect.x, alien.rect.y)
                # 删除该外星人
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

        # if self.stats.difficulty == 1:
        #     # 定时创建外星人Alien_1
        #     self.scheduler.add_job(self._create_alien_1, 'interval', seconds=2)
        #     # 定时创建外星人Alien_2
        #     self.scheduler.add_job(self._create_alien_2, 'interval', seconds=3)
        # 当水平提升到5时，Boss出现。同时创建一个补给包，强化飞船火力
        if self.stats.difficulty == 2:
            self.scheduler.add_job(self._create_alien_3, 'interval', seconds=8)
        if self.stats.difficulty == 5:
            self.scheduler.add_job(self._create_alien_4, 'interval', seconds=15)
        # if self.stats.difficulty == 7:

        #     # Boss登场
        #     self.boss_show = True
        #     pygame.mixer.fadeout(2000)
        #     self.player.play_multiple_sounds(
        #         ['boss_2_apear', 'great_war_boss_2'], [1, -1])
           
            # 创建补给包
            self.missile_package = MissilePackage(self)
            self.packages.add(self.missile_package)

    def _set_boss_explosions_range(self):
        """根据Boss所在位置，获得其连续爆炸的随机位置"""
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
        
        # 如果碰撞了就高亮显示Boss，并删除子弹
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
        
            # 如果Boss的血量已耗尽，则渲染其爆炸的效果
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
            self.scheduler.remove_all_jobs()
            sleep(5)
            # 用1.5秒时间渐停播放背景音乐
            self.player.fadeout(1500)
            # 设置玩家胜利
            self.victory = True
            sleep(3)
            # 播放游戏胜利的音效
            self.player.play('victory', -1, 1)
            # 显示鼠标
            pygame.mouse.set_visible(True)  
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
        self.boss_show = False

        # 设定在3.1秒后恢复默认的爆炸效果（3.1秒正好是10次连续爆炸持续时间的总和多一点点）
        threading.Timer(3.1, self.explosion.reset).start()

    def _check_ship_hit(self):
        """检查飞船是否被击中（与外星人发生碰撞或有外星人到达屏幕底部），并做出响应"""
        if not self.ship_destroy:
            # 获取与飞船发生碰撞的子弹
            collided_bullet = pygame.sprite.spritecollideany(
                self.ship, self.alien_bullets)
            
            # 获取与飞船发生碰撞的外星人
            collided_alien = pygame.sprite.spritecollideany(
                self.ship, self.aliens, pygame.sprite.collide_mask)
            
            # 检测飞船是否与Boss发生了碰撞
            if pygame.sprite.spritecollide(self.ship, self.boss_group, False,
                                            pygame.sprite.collide_mask):
                self._ship_destroyed()
            
            # 当飞船与子弹碰撞时，做出相应的操作
            if collided_bullet:
                self.alien_bullets.remove(collided_bullet)
                self._ship_destroyed() 

            # 当飞船与外星人碰撞时，做出相应的操作
            if collided_alien:
                self.aliens.remove(collided_alien)
                self._ship_destroyed()

            # 如果Boss已经出现，则检测飞船是否被Boss发射的子弹击中
            if self.boss_show:
                self._check_boss_bullet_hits_ship()

    def _check_boss_bullet_hits_ship(self):
        """检查Boss的子弹命中飞船"""
        # 检测与飞船发生碰撞的Boss子弹
        collided_bullets = pygame.sprite.spritecollideany(
            self.ship, self.boss_2.bullets, pygame.sprite.collide_mask)
        
        # 当飞船与子弹碰撞时，做出相应的操作
        if collided_bullets:
            # 如果击中飞船的是激光束，则激光束不会消失
            if not isinstance(collided_bullets, LaserBeam):
                self.boss_2.bullets.remove(collided_bullets)
            self._ship_destroyed()

    def _ship_destroyed(self):
        """响应飞船被击毁"""
        self.ship_destroy = True
        # 播放声音
        self.player.play('explode', 0, 1)
        # 设置爆炸图片显示的正确位置
        self.explosion.set_effect(self.ship.rect.x, self.ship.rect.y)
        # 设置多线程，倒计时三秒后将调用self._ship_hit()方法
        threading.Timer(3, self._ship_hit).start()
      
    def _ship_hit(self):
        """当飞船被击中时，做出相应的响应"""
        # 如果还有备用飞船，重新开始，否则结束游戏
        if self.stats.ship_left > 0:
            # 备用飞船减一，表示启用了一艘备用飞船
            self.stats.ship_left -= 1
            # 刷新屏幕上显示的剩余飞船
            self.sb.prep_ships()

            # 新飞船出现时，清空屏幕上所有的子弹和外星人
        #    self.aliens.empty()
            self.ship_bullets.empty()
            self.alien_bullets.empty()
            
            if self.boss_show:  
                self.boss_2.bullets.empty()

            # 因为已经创建了一个飞船实例，因此启动备用飞船并不是真的要在创建一个实例，
            # 我们只需将现有的飞船居中即可。   
            self.ship.ship_center()
            self.ship_destroy = False

        else:  # 如果备用飞船全部用完，则游戏结束
            # 删除所有的定时任务
            self.scheduler.remove_all_jobs()
            # 停顿3秒，效果更好
            sleep(3)
            # 设置状态
            self.game_over = True
            self.game_active = False
            # 播放游戏结束的音效
            self.player.stop()
            self.player.play('game_over', 0, 1)
            # 显示鼠标
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
        if self.boss_show:
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
      
        if self.boss_show:
            self.boss_2.update_screen()

        self.explosion.blitme()
        self.packages.draw(self.screen)
        self.sb.ships.draw(self.screen)
        self.sb.show_score()

        if self.victory:
            self.game_text.show_victory_text()
            self.continue_button.draw_button()
        if self.game_over:
            self.game_text.show_game_over_text()
            self.restart_button.draw_button()

        # 显示窗口
        pygame.display.flip()