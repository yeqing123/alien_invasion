import pygame

from pygame.sprite import Group

from level_1.bullets.alien.boss.boss_bomb import BossBomb
from level_1.bullets.alien.boss.boss_ordinary_bullet import OrdinaryBullet

class AlienBoss_1():
    """管理一号外星人boss的类，其实例也将加入到外星人编组(aliens)中统一管理"""

    def __init__(self, ai_game):
        """初始化各类属性"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.scheduler = ai_game.scheduler
        self.screen_rect = self.screen.get_rect()
        
        # 加载两个Boss的图片，一个是普通图片另一个是高亮图片
        self.image = pygame.image.load("images/aliens/bosses/boss_1.png")
        self.high_image = pygame.image.load("images/aliens/bosses/high_light_boss_1.png")
        self.rect = self.image.get_rect()
        self.high_rect = self.high_image.get_rect()

        self.rect.midbottom = self.screen_rect.midtop

        self.ordinary_bullets = Group()
        self.bombs = Group()

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # 设置与运动有关的属性
        self.boss_speed = 1.5
        self.boss_drop_speed = 20
        self.dive_distance = 200
        self.dive_speed = 2.5

        # 定义Boss的血量
        self.blood_volume = 100

        # 设置游戏运行过程中Boss的一些状态标识
        self.high_light = False
        self.allow_fire = False
        self.begin_dive = False
        self.drop_bomb_done = False

    def update(self):
        """更新boss的位置"""
        # Boss登场时先判断是否到达屏幕的指定位置
        if self.rect.bottom < self.screen_rect.height / 2.5:
            self._boss_appearing()
        elif not self.allow_fire: # 如果还没有允许射击，则允许开火
            self.allow_fire = True
            # 向任务调度器中添加Boss的投弹任务，每三秒开火一次，每十秒俯冲投弹一次
            self.scheduler.add_job(self.fire_ordinary_bullet, 'interval', seconds=3)
            self.scheduler.add_job(self._begin_dive, 'interval', seconds=10)
        elif self.begin_dive: # 如果允许俯冲，则开始俯冲并投弹
            self._dive_drop_bomb()
            self.bombs.update() # 更新炸弹的位置
        else:     # 如果以上情况都不是，则左右运动
            self._move_left_and_right()

    def _boss_appearing(self):
        """Boss出现了"""
        self.y += 2.5
        self.rect.y = self.y

    def _begin_dive(self):
        """开始俯冲投弹"""
        self.begin_dive = True

    def _dive_drop_bomb(self):
        """让Boss做俯冲投弹后回撤的动作"""
        # 如果还没有投弹，就向前俯冲指定距离后投弹。如果已经投弹完成，就回撤到起始位置
        if not self.drop_bomb_done:
            # 继续向前俯冲
            if self.dive_distance > 0:
                self.y += self.dive_speed
                self.rect.y = self.y
                self.dive_distance -= self.dive_speed
            # 到达指定位置后投弹
            elif self.dive_distance <= 0:
                self._drop_bomb()
                self.drop_bomb_done = True
        else: # 回撤
            if self.dive_distance < 200:
                self.y -= self.dive_speed
                self.rect.y = self.y
                self.dive_distance += self.dive_speed
            # 当回撤到起始位置后，重置两个标记，等待下次俯冲
            elif self.dive_distance >= 200:
                self.begin_dive = False
                self.drop_bomb_done = False
        
    def _move_left_and_right(self):
        """负责Boss常规的左右移动"""
        self._check_edges()
        self.x += self.boss_speed * self.settings.boss_direction
        self.rect.x = self.x

    def _check_edges(self):
        """检查boss是否移动到了屏幕左右边缘，然后改变其移动方向"""
        if (self.rect.left <= 100 or 
            self.rect.right >= self.screen_rect.right - 100):

            self.settings.boss_direction *= -1

    def _drop_bomb(self):
        """发射子弹"""
        self.ai_game.player.play('drop_bomb', 0, 1)
        position = self.rect.midbottom
        new_bomb = BossBomb(self.ai_game, position)
        self.bombs.add(new_bomb)

    def fire_ordinary_bullet(self):
        """发射Boss的普通子弹，一次所有两侧同时发射"""
        # 设置两发子弹各自的初始坐标位置
        x_position_1 = self.rect.x + 23
        x_position_2 = self.rect.x + 302
        y_position = self.rect.y + 193
        # 根据指定位置创建两发子弹
        dot_bullet_1 = OrdinaryBullet(self.ai_game, (x_position_1, y_position))
        dot_bullet_2 = OrdinaryBullet(self.ai_game, (x_position_2, y_position))
        # 加入子弹编组
        self.ordinary_bullets.add(dot_bullet_1)
        self.ordinary_bullets.add(dot_bullet_2)

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
