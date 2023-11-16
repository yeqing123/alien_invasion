import pygame

class SoundsPlayer:
    """负责播放音乐的类"""

    def __init__(self):
        """初始化相关的属性"""
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.set_num_channels(20)

        # 所有需要加载的游戏音效的文件路径都在这里
        self.files_path = {
            'bg_music_1': 'level_1/musics/bg_music(Level_1).mp3',
            'bg_music_2': 'level_1/musics/CONTINUE.ogg', 
            'fire_bullet': 'level_1/musics/fire_bullet.mp3',
            'explode': 'level_1/musics/alien_explode.wav',
            'boss_explode': 'level_1/musics/boss_explode.wav',
            'small_bullet': 'level_1/musics/qhzd.ogg',
            'drop_bomb': 'level_1/musics/drop_bomb.wav',
            'victory':'level_1/musics/zd_bgm.ogg',
            'enhance': 'level_1/musics/buff.mp3',
            'ship_bomb': 'level_1/musics/skill2.ogg',
            'game_over': 'level_1/musics/游戏结束(GameOver).wav',
            'launch_shotgun': 'level_2/musics/发射炮弹的音效_爱给网_aigei_com.mp3',
            'laser_shot': 'level_2/musics/能量激光发射聚集形成等音效 (6)_爱给网_aigei_com.mp3',
            'great_war_boss_2': 'level_2/musics/雷霆战机boss背景音乐_爱给网_aigei_com.wav',
            'boss_2_apear': 'level_2/musics/Boss出场战斗氛围铺垫-短视频人物登场-紧张神秘氛围_爱给网_aigei_com.wav',
            'storage_force': 'level_2/musics/武器蓄能 蓄力_爱给网_aigei_com.mp3',
            'boss_2_laser_beam': 'level_2/musics/激光光束充电回路1 - 科幻武器- 激光光束充电回路_ 通电_爱给网_aigei_com.mp3',
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
            return channel
          
    def stop(self):
        """停止播放音乐"""
        pygame.mixer.stop()
        pygame.mixer.music.stop()

    def play_multiple_sounds(self, soundnames, loops):
        """加入要播放的下一个声音"""
        for name in soundnames:
            pygame.mixer.music.load(self.files_path[name])
            index = soundnames.index(name)
            loop = loops[index]
            print(loop)
            pygame.mixer.music.play(loop, 0.5, 1)
            while not loop == - 1 and pygame.mixer.music.get_busy():
                pass

    def set_volume(self, name, volume):
        """调节指定音乐的音量"""
        music = self.sounds_dictionary.get(name)
        if music:
           music.set_volume(volume) 