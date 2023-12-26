import pygame

from pygame.sprite import Group
from pygame.sprite import Sprite
from time import sleep
from functools import lru_cache

from level_2.bullets.alien.boss.fire_ball import FireBall
from level_2.bullets.alien.boss.laser_beam import LaserBeam
from level_2.bullets.alien.boss.rotating_bullet import RotatingBullet

class AlienBoss_2(Sprite):
    """管理第二关外星人boss的类"""

    def __init__(self, ai_game):
        """初始化各类属性"""
        super().__init__()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.scheduler = ai_game.scheduler
        self.screen_rect = self.screen.get_rect()
        
        self.image = pygame.image.load("images/aliens/bosses/boss_2.png")
        self.high_image = pygame.image.load(
            "images/aliens/bosses/high_light_boss_2.png")
        
         # 对图片进行优化处理
        self.image = self.image.convert_alpha()
        self.high_image = self.high_image.convert_alpha()

        self.rect = self.image.get_rect()
        self.high_rect = self.high_image.get_rect()

        # 存放Boss发射的旋转子弹和激光束的编组
        self.rotate_bullets = Group()
        # 存放Boss发射的散弹的编组
        self.shotguns = Group()

        # 存放Boss的闲置的旋转子弹对象
        self.idle_rotate_bullets = []
        # 存放Boss闲置的散弹(包括FireBall对象)
        self.idle_shotguns = []

        # 设置与运动有关的属性
        self.boss_speed = 1.0

        # 创建显示激光束效果实例
        self.laser_beam = LaserBeam(self.ai_game, self)

        self.initialize_state()

        # 设置要发射的旋转子弹的id
        self.id_list = [4, 3, 2, 1, 16, 15, 14]

    def initialize_state(self):
        """初始化Boss的有关状态"""
        # 重置初始位置
        self.rect.midbottom = self.screen_rect.midtop
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # 清空子弹编组和存放闲置子弹的列表
        self.rotate_bullets.empty()
        self.shotguns.empty()
        self.idle_rotate_bullets.clear()
        self.idle_shotguns.clear()
      
        # 定义Boss的血量
        self.blood_volume = 700
        # 定义分值
        self.boss_points = 20

        # 设置游戏运行过程中Boss的一些状态标识
        self.high_light = False
        self.allow_fire = False

        # 保存火球子弹的变量
        self.fire_ball = None

    def update(self):
        """更新boss的位置"""
        # Boss登场时先判断是否到达屏幕的指定位置
        if self.rect.bottom < self.screen_rect.height / 2.5:
            self._boss_appearing()
        elif not self.allow_fire: # 如果还没有允许射击，则设置为允许开火
            self.allow_fire = True

            # 向任务调度器中添加Boss的投弹任务，每三秒开火一次，每十秒俯冲投弹一次
            self.scheduler.add_job(
                self._launch_fire_ball, 'interval', seconds=5, max_instances=15)
        else:     # 如果以上情况都不是，则左右运动
            self._move_left_and_right()
        
        # 当Boss的血量减到一定程度时，增强Boss的火力
        if self.blood_volume <= 200 and not self.scheduler.get_job("laser"):
            print("添加激光束任务")
            self.scheduler.add_job(self._launch_laser_beam, 'interval', 
                                id="laser", seconds=15, max_instances=10)
        
        if self.blood_volume <= 100 and not self.scheduler.get_job("rotate_bullet"):
            print("添加旋转子弹任务")
            self.scheduler.add_job(self._launch_rotating_bullet, 
                        'interval', id="rotate_bullet", seconds=15, args=[0])
            

        # 检测火球是否需要炸裂
        if self.fire_ball:
            self.fire_ball.fire_ball_burst()

    def _boss_appearing(self):
        """Boss出现了"""
        self.y += 2.5
        self.rect.y = self.y
        
    def _move_left_and_right(self):
        """负责Boss常规的左右移动"""
        self._check_edges()
        self.x += self.boss_speed * self.settings.boss_direction
        self.rect.x = self.x

    def _check_edges(self):
        """如果boss移动到了设定的左右边缘，就改变其移动方向"""
        if (self.rect.left <= 100 or 
            self.rect.right >= self.screen_rect.right - 100):

            self.settings.boss_direction *= -1
    
    def _launch_rotating_bullet(self, index):
        """发射旋转子弹"""
        # 如果索引值到达列表末尾，就结束递归
        if index == len(self.id_list) - 1:
            return
        try:
            # 从列表末尾弹出一个闲置的RotatingBullet对象
            idle_bullet = self.idle_rotate_bullets.pop()
            # 重置该对象的位置
            idle_bullet.initialize_position()
            # 加入编组
            self.rotate_bullets.add(idle_bullet)
        except IndexError:  # 如果列表为空，就创建一个新的对象
            new_bullet = RotatingBullet(self.ai_game, self)
            id = self.id_list[index]
            new_bullet.set_id(id)
            new_bullet.initialize_flight_path()
            self.rotate_bullets.add(new_bullet)
        
        index += 1    
        sleep(1)
        # 每个一秒就递归一次
        self._launch_rotating_bullet(index)

    def _launch_laser_beam(self):
        """发射激光束"""
        # 播放激光器蓄力时的音效(时间为3秒钟) 
        self.ai_game.player.play('storage_force', 0, 1)
        sleep(3)

        # 播放激光束发射时的音效
        self.ai_game.player.play('boss_2_laser_beam', 0, 1)
        # 重置位置
        self.laser_beam.initialize_position()
        # 将激光束实例加入编组
        self.rotate_bullets.add(self.laser_beam)
        # 激光束持续3秒
        sleep(3)
        self.rotate_bullets.remove(self.laser_beam)

    def _launch_fire_ball(self):
        """发射火球子弹"""
        # 先从Boss口中发射一颗火球状子弹
        self.fire_ball = FireBall(self)
        self.shotguns.add(self.fire_ball)

    def boss_high_light(self):
        """让Boss图片高亮，以表示它被击中了一次"""
        # 将Rect对象更改为在初始化时已经加载好的另一张图片
        self.high_rect.x = self.rect.x
        self.high_rect.y = self.rect.y

    def blitme(self):
        """在屏幕上绘制boss"""
        # 根据是否高亮的标识，绘制不同的图片
        if self.high_light:
            self.screen.blit(self.high_image, self.high_rect)
            self.high_light = False
        else:
            self.screen.blit(self.image, self.rect)

    def update_screen(self):
        """绘制Boss2及其子弹的图像"""
        self.blitme()
        self.rotate_bullets.draw(self.screen)
        self.shotguns.draw(self.screen)
