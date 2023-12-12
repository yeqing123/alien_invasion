import pygame
import math

from pygame.sprite import Sprite
from random import randint
from time import sleep
from threading import Timer

from level_2.bullets.alien.alien_bomb import AlienBomb
from level_2.bullets.alien.small_bullet import SmallBullet

class Alien_4(Sprite):
    """
    创建一个4号外星人，该外星人在屏幕上边缘出现后，沿着y轴垂直向下飞行，
    飞过一段距离后开始向右转，当到达预设的最低点后开始返航，直到飞出上屏幕为止
    """
    
    def __init__(self, ai_game):
        """初始化一个从屏幕上边缘随机位置出现的外星人"""
        super().__init__()
        self.settings = ai_game.settings
        self.ai_game = ai_game
        self.screen_rect = ai_game.screen_rect

        # 加载外星人飞机图像
        self.image = pygame.image.load('images/aliens/JpPlane.bmp')
        # 对图片进行优化处理
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()

        # 设置外星人的初始位置
        self.rect.centerx = self.screen_rect.width / 4
        self.rect.y = -2 * self.rect.height

        # 设置该外星人在y轴上飞行的最低点
        self.y_nadir = self.screen_rect.height / 2
        
        # 设置外星人向下移动的速度
        self.down_moving_speed = 2.0
        # 设置外星人向右移动的速度，因为右移的速度是不断变化的，所以初始值为0
        self.right_moving_speed = 2.0
        # 设置y轴上移动速度的递减幅度
        self.reduce_scale = 0.05
        # 计算down_moving_speed从2递减到0所需的次数
        self.step_number= self.down_moving_speed / self.reduce_scale
        # 设置一个保存次数的备用变量
        self.spare_number = self.step_number

        # 为了便于精确计算，将其rect的中心点坐标设置为浮点数类型
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

         # 设置该外星人的分值
        self.alien_points = 3

        # 设置是否已到达指定的最低点
        self.reach_nadir = False

        # 记录扫射次数
        self.strafe_number = 0

        # 设置外星人左右扫射时的移动方向(1标识向右，-1标识向左)
        self.strafe_direction = 1

        # 设置血量
        self.blood_volume = 10

        # 设置是否高亮显示
        self.hight_light = False

        # 是否已经投弹
        self.drop_bomb = False

    def _start_strafe(self):
        """将APScheduler任务调度器中添加开火的任务"""
        # 使用id()函数获得当前外星人对象的id，作为开火任务的唯一id
        job_id = f"{id(self)} open fire"

        if self.ai_game.scheduler.get_job(job_id) == None:
            # 添加开火的任务，并设置子弹发射的频率为0.5秒
            self.ai_game.scheduler.add_job(
                self._open_fire, 'interval', id=job_id, seconds=0.5)

    def _open_fire(self):
        """在飞机的左右两边同时发射子弹"""
        # 设置左右两颗子弹的x坐标位置
        left_x = self.rect.x + self.rect.width / 4
        right_x = self.rect.x + (self.rect.width / 4) * 3
        
        # 创建子弹，并设置其初始化位置
        left_small_bullet = SmallBullet(self.ai_game, left_x, self.rect.bottom)
        right_small_bullet = SmallBullet(self.ai_game, right_x, self.rect.bottom)
        
        # 加入子弹编组中
        self.ai_game.alien_bullets.add(left_small_bullet)
        self.ai_game.alien_bullets.add(right_small_bullet)
        
        self.ai_game.player.play("small_bullet", 0, 0.5)
        
    def _drop_bomb(self):
        """外星人发射子弹"""
        # 设置炸弹的初始位置
        position = self.rect.midbottom
        # 创建炸弹对象，并加入编组
        new_bomb = AlienBomb(self.ai_game, position)
        self.ai_game.alien_bullets.add(new_bomb)
        self.ai_game.player.play("drop_bomb", 0, 0.5)
        
        # 投弹完成后，停止射击
        if self.ai_game.scheduler.get_job(job_id=f"{id(self)} open fire"):
                self.ai_game.scheduler.remove_job(job_id=f"{id(self)} open fire")

    def _rotate_alien(self):
        """计算外星人将要旋转的角度, 并旋转其图像"""
        # 根据外星人当前位置与设置的最低点形成的直角三角形的a,b,c三条边的长度

        # 只有到达指定位置时才开始转弯
        if self.rect.bottom >= self.y_nadir:
            # 首先计算飞机在x轴上移动的长度
            a = self.step_number * self.right_moving_speed
        else:
            a = 0.0
        
        # 然后计算以飞机当前的速度，计算在y轴上移动的长度
        b = self.step_number * self.down_moving_speed
            
        # 最后根据勾股定律得出三角形斜边c的长度
        c = math.sqrt(math.pow(a, 2) + math.pow(b, 2))

        # 计算将要旋转的夹角度数
        try:
            angle = math.degrees(math.acos((a*a-b*b-c*c)/(-2*b*c)))
        except ZeroDivisionError:
            pass
        else:
            # 如果已经到达了最低点，则转换角度
            # if self.down_moving_speed < 0:
            #     angle = 180 - angle

            if self.hight_light:
                self.image = pygame.image.load('images/aliens/HL_JpPlane.bmp')
                self.hight_light = False
            else:
                self.image = pygame.image.load('images/aliens/JpPlane.bmp')
            
            self.image = self.image.convert_alpha()
            # 旋转图像
            self.image = pygame.transform.rotate(self.image, angle)
            # 以图像中心点为轴心旋转
            self.rect = self.image.get_rect(center=self.rect.center)

    def _change_strafe_direction(self):
        """在扫射中改变左右移动方向"""
        # 设置所有移动的终点
        left_terminal_point = self.screen_rect.width / 4
        right_terminal_point = self.screen_rect.width / 4 * 3

        if self.strafe_direction == 1 and \
                self.rect.right >= right_terminal_point:
            self.strafe_direction = -1
            self.strafe_number += 1
        elif self.strafe_direction == -1 and \
                self.rect.left <= left_terminal_point:
            self.strafe_direction = 1
            self.strafe_number += 1
    
    def update(self):
        """更新外星人的位置"""
        if self.rect.bottom < self.y_nadir / 3:
            self.y += self.down_moving_speed
        elif self.rect.bottom < self.y_nadir:
            # 在投弹之前开始机枪扫射
            if not self.drop_bomb:
                self._start_strafe()

            # 当游戏难度提升至3时左右移动水平
            if self.ai_game.stats.difficulty >= 3 and self.strafe_number < 4: 
                self._change_strafe_direction()
                self.x += 1.5 * self.strafe_direction
            else:
                self.y += self.down_moving_speed
        elif self.rect.bottom >= self.y_nadir:
            # 当到达指定地点后，执行投弹操作
            if not self.drop_bomb:
                self._drop_bomb()
                self.drop_bomb = True

            # 标记已到达指定位置
            self.reach_nadir = True
            # 执行右转回撤操作
            if self.down_moving_speed > -2.0:
                self.x += self.right_moving_speed
                # 不断递减为负数后就开始回撤
                self.down_moving_speed -= self.reduce_scale
                
                if self.step_number > 0:
                    self.step_number -= 1
                else:
                    # 重置为初始值
                    self.step_number = self.spare_number
                
            self.y += self.down_moving_speed
        
        self.rect.centerx = self.x
        self.rect.centery = self.y
        
        # 更新并旋转飞机图像
        self._rotate_alien()
        
