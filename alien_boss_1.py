import pygame

from pygame.sprite import Group
from bullets.bomb import Bomb
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

        self.dot_bullets = Group()
        self.bombs = Group()

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.boss_speed = 1.5
        self.boss_drop_speed = 20
        self.nose_down_distance = 200
        self.nose_down_speed = 2.5

        # 自定义事件
        self.FIRE_BULLET_EVENT = pygame.USEREVENT + 2
        self.FIREFULL_EVENT = pygame.USEREVENT + 3

        self.allow_fire = False
        self.nose_down = False
        self.start_drop_bomb = False

    def _set_timer(self):
        """设置定时器"""
        pygame.time.set_timer(self.FIRE_BULLET_EVENT, 2000)
        pygame.time.set_timer(self.FIREFULL_EVENT, 10000)
        self.allow_fire = True


    def update(self):
        """更新boss的位置"""
        if self.rect.bottom < self.screen_rect.height / 2.5:
            self._boss_appearing()
        elif not self.allow_fire:
            self._set_timer()
        elif self.nose_down:
            self._nose_down()
            self.bombs.update()
        else:
            self._move_left_and_right()

    def _boss_appearing(self):
        """Boss出现了"""
        self.y += 2.5
        self.rect.y = self.y

    def _nose_down(self):
        """使Boss定时做俯冲动作"""
        if not self.start_drop_bomb:
            if self.nose_down_distance > 0:
                print("俯冲开始！")
                self.y += self.nose_down_speed
                self.rect.y = self.y
                self.nose_down_distance -= self.nose_down_speed
            elif self.nose_down_distance <= 0:
                print("投弹！")
                self._drop_bomb()
                self.start_drop_bomb = True
        else:
            print("回撤！")
            if self.nose_down_distance < 200:
                self.y -= self.nose_down_speed
                self.rect.y = self.y
                self.nose_down_distance += self.nose_down_speed
            else:
                self.nose_down = False
                self.start_drop_bomb = False
        
    def _move_left_and_right(self):
        """负责Boss常规的左右移动"""
        self._check_edegs()
        self.x += self.boss_speed * self.settings.boss_direction
        self.rect.x = self.x

    def _check_edegs(self):
        """检查boss是否移动到了屏幕左右边缘，然后改变其移动方向"""
        if (self.rect.left <= 100 or 
            self.rect.right >= self.screen_rect.right - 100):

            self.settings.boss_direction *= -1

    def _drop_bomb(self):
        """发射子弹"""
        position = self.rect.midbottom
        new_bomb = Bomb(self.ai_game, position)
        self.bombs.add(new_bomb)

    def fire_dot_bullet(self):
        """发射小圆点子弹"""
        x_position_1 = self.rect.x + 23
        x_position_2 = self.rect.x + 302
        y_position = self.rect.y + 193
        dot_bullet_1 = DotBullet(self.ai_game, (x_position_1, y_position))
        dot_bullet_2 = DotBullet(self.ai_game, (x_position_2, y_position))
        
        self.dot_bullets.add(dot_bullet_1)
        self.dot_bullets.add(dot_bullet_2)

    def blitme(self):
        """在屏幕上绘制boss"""
        self.screen.blit(self.image, self.rect)
