import pygame

class GameMusic:
    """负责管理游戏的背景音乐的类"""

    def __init__(self):
        """初始化相关的属性"""
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load('musics/CONTINUE.ogg')


    def play_music(self):
        """播放游戏背景音乐"""
        # 参数0.5表示将音量设置为一半
        pygame.mixer.music.set_volume(0.5)
        # 如果传入的参数是一个正整数，就表示循环播放的次数，-1表示一直循环播放
        pygame.mixer.music.play(-1)

    def stop_music(self):
        """停止播放音乐"""
        pygame.mixer.music.stop()
        pygame.mixer.quit()