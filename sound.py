import pygame

class Sound:
    def __init__(self):
        # 初始化Pygame混音器
        pygame.mixer.init()

        # 加载音效文件
        self._creat_sound()

        # 设置默认音量
        self.shoot_sound.set_volume(0.8)
        self.explosion_sound.set_volume(0.8)
        self.bgm_sound.set_volume(0.8)

    def play_music(self,music):
        if music == "shoot":
            self.shoot_sound.play()
        if music == "explosion":
            self.explosion_sound.play()
        if music == "click_button":
            self.click_button_sound.play()
        if music == "bgm":
            self.bgm_sound.play(-1)


    def _creat_sound(self):
        self.shoot_sound = pygame.mixer.Sound('sound/shoot.mp3')
        self.explosion_sound = pygame.mixer.Sound('sound/explosion.mp3')
        self.bgm_sound = pygame.mixer.Sound('sound/bgm.mp3')
        self.click_button_sound = pygame.mixer.Sound('sound/click_button.mp3')

