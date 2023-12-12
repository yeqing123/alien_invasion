import pygame

from threading import Thread

class SoundsPlayer:
    """负责播放音乐的类"""

    def __init__(self, sounds_path):
        """初始化相关的属性"""
        pygame.init()
        pygame.mixer.init()
        self.channels_number = 20
        self.id = 0
        pygame.mixer.set_num_channels(self.channels_number)

        # 获取每一关将要播放的声音文件的路径
        self.files_path = sounds_path
        
        # 以name为键，以Sound和Channel组成的元组为值，将加载文件后生成的对象保存在字典中
        self.sc_dictionary = {}
        

    def _load_file(self, name):
        """根据名称加载声音文件，将生成的Sound对象和Channel对象保存在字典中"""
        try :
            path = self.files_path[name]
            # 加载文件
            sound = pygame.mixer.Sound(path)
        except FileNotFoundError:
            print(f"No file exists in the {path}!")
        else:
            if self.id < self.channels_number:
                # 创建一个Channel对象，并为其分配一个id 
                channel = pygame.mixer.Channel(self.id)
                # 将生成的sound和channel对象保存在字典中
                self.sc_dictionary[name] = (sound, channel)
                # 更新id
                self.id += 1
            else:
                print("The id value of the channel exceeds the set maximum value!")
                return None
            
    def play(self, name, loops, volume):
        """播放name对应的声音文件，loop表示循环的次数-1为无限循环，volume为音量"""
        
        # 如果字典中没有保存该键值对，说明还文件没有加载
        if not self.sc_dictionary.get(name):
             self._load_file(name)
        
        # 从字典中取出Sound和Channel组成的元组
        sc_tuple = self.sc_dictionary[name]
        # 获得Sound对象
        sound = sc_tuple[0]
        # 获得Channel对象
        channel = sc_tuple[1]

        # 设置音量
        channel.set_volume(volume)
        # 播放音乐
        channel.play(sound, loops)
       
        return channel
                
    def stop(self):
        """停止播放音乐"""
        pygame.mixer.stop()
        pygame.mixer.music.stop()

    def _play_sounds(self, soundnames, loops):
        """连续播放多个声音文件，每个文件都会按照设定的循环次数播放，然后自动播放下一个"""
        for name in soundnames:
            # 加载文件
            pygame.mixer.music.load(self.files_path[name])
            # 取得文件在列表中对应的索引值
            index = soundnames.index(name)
            # 取得播放该文件的循环次数
            loop = loops[index]
            # 播放文件
            pygame.mixer.music.play(loop, 0.5, 1)
            # 一直等待文件播放完毕，然后播放下一个文件
            # （如果不使用多线程，这里会影响主进程的运行）
            while pygame.mixer.music.get_busy():
                pass

    def play_multiple_sounds(self, soundnames, loops):
        """在一个单独的线程中播放soundnames中保存的多个声音文件，
        这样可以避免对游戏主进程的干扰"""
        # 创建一个单独线程，负责连续播放多个文件
        t = Thread(target=self._play_sounds, args=(soundnames, loops))
        # 启动该线程
        t.start()

    def set_volume(self, name, volume):
        """调节指定音乐的音量"""
        music = self.sounds_dictionary.get(name)
        if music:
           music.set_volume(volume) 

    def fadeout(self, delay):
        """让正在播放的背景音乐逐渐延迟消失, delay以毫秒为单位"""
        pygame.mixer.music.fadeout(delay)