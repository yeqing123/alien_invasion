import pygame
import threading

from pygame.sprite import Group
from bullets.boss_bullet import BossBullet
from bullets.dot_bullet import DotBullet

class AlienBoss_1:
    """管理一号外星人boss的类"""

    def __init__(self, ai_game):
        """初始化各类属性"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = self.screen.get_rect()
        self.image = pygame.image.load("images/processed_img_plane_boss.png")
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midtop

        self.bullets = Group()
        self.dot_bullets = Group()

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.boss_speed = 1.5
        self.boss_drop_speed = 20

        # 自定义事件
        self.FIRE_BULLET_EVENT = pygame.USEREVENT + 2

    def _set_fire_bullet_event(self):
        """设置boss的开火事件，并使之事件每次触发的延迟时间"""

    def update(self):
        """更新boss的位置"""
        if self.rect.bottom < self.screen_rect.height / 2.5:
            self.y += 2.5
            self.rect.y = self.y
        else:
            # 定义一个定时器，每隔1000毫秒就触发一次事件
            pygame.time.set_timer(self.FIRE_BULLET_EVENT, 1000)

            self._check_edegs()
            self.x += self.boss_speed * self.settings.boss_direction
            self.rect.x = self.x

    def _check_edegs(self):
        """检查boss是否移动到了屏幕左右边缘，然后改变其移动方向"""
        if (self.rect.left <= 100 or 
            self.rect.right >= self.screen_rect.right - 100):

            self.settings.boss_direction *= -1

    def fire_bullets(self):
        """发射子弹"""
        bullet_1 = BossBullet(self.ai_game, 'left')
        bullet_2 = BossBullet(self.ai_game, 'right')
        
        self.bullets.add(bullet_1)
        self.bullets.add(bullet_2)

    def fire_dot_bullet(self):
        """发射小圆点子弹"""
        x_position_1 = self.rect.x + 117
        x_position_2 = self.rect.x + 207
        y_position = self.rect.y + 185
        dot_bullet_1 = DotBullet(self.ai_game, x_position_1, y_position)
        dot_bullet_2 = DotBullet(self.ai_game, x_position_2, y_position)
        
        self.dot_bullets.add(dot_bullet_1)
        self.dot_bullets.add(dot_bullet_2)

    def blitme(self):
        """在屏幕上绘制boss"""
        self.screen.blit(self.image, self.rect)
