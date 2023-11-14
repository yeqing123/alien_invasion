import pygame

class SoundsPlayer:
    """负责播放音乐的类"""

    def __init__(self):
        """初始化相关的属性"""
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.set_num_channels(15)

        # 所有需要加载的游戏音效的文件路径都在这里
        self.files_path = {
            'bg_music_1': 'level_1/musics/bg_music(Level_1).mp3',
            'bg_music_2': 'level_1/musics/CONTINUE.ogg', 
            'fire_bullet': 'level_1/musics/fire_bullet.mp3',
            'explode': 'level_1/musics/alien_explode.wav',
            'boss_explode': 'level_1/musics/boss_explode.wav',
            'dot_fire': 'level_1/musics/qhzd.ogg',
            'drop_bomb': 'level_1/musics/drop_bomb.wav',
            'victory':'level_1/musics/zd_bgm.ogg',
            'enhance': 'level_1/musics/buff.mp3',
            'ship_bomb': 'level_1/musics/skill2.ogg',
            'game_over': 'level_1/musics/游戏结束(GameOver).wav',
            }
        
        # 用一个字典保存加载后生成的Sound对象（以文件名为键，以对应的Sound对象为值）
        self.sounds_dictionary = {}
        # 给每个Sound分配一个音频通道ID（默认最多8个）
        self.channels_id = {}
        # 音频通道的编号
        self.id = 0

        # 加载所有音效文件
        self._load_files()

    def _load_files(self):
        """加载属性字典files_path中保存的所有音频文件"""
        for name, path in self.files_path.items():
            try :
                sound = pygame.mixer.Sound(path)
            except FileNotFoundError:
                print(f"No file exists in the {path}!")
            else:
                self.sounds_dictionary[name] = sound
                self.channels_id[name] = self.id
                self.id += 1
        
    def play(self, name, loops, volume):
        """播放指定名称的音乐，并设置循环次数的音量"""
        sound = self.sounds_dictionary.get(name)
        if sound:
            # 创建一个声音播放频道
            id = self.channels_id.get(name)
            channel = pygame.mixer.Channel(id)
            # 设置音量
            channel.set_volume(volume)
            # 播放音乐
            channel.play(sound, loops)
          
    def stop(self):
        """停止播放音乐"""
        pygame.mixer.stop()

    def set_volume(self, name, volume):
        """调节指定音乐的音量"""
        music = self.sounds_dictionary.get(name)
        if music:
           music.set_volume(volume) 