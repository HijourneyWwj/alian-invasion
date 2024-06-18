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
        self.alien_shoot_sound.set_volume(0.1)
        self.boss_shoot_sound.set_volume(0.8)
        self.boss_explosion_sound.set_volume(1)

    def play_music(self,music):
        if music == "ship_shoot":
            self.shoot_sound.play()
        if music == "explosion":
            self.explosion_sound.play()
        if music == "click_button":
            self.click_button_sound.play()
        if music == "bgm":
            self.bgm_sound.play(-1)
        if music == "alien_shoot":
            self.alien_shoot_sound.play()
        if music == "boss_shoot":
            self.boss_shoot_sound.play()
        if music == "boss_explosion":
            self.boss_explosion_sound.play()


    def _creat_sound(self):
        self.shoot_sound = pygame.mixer.Sound('sound/shoot.mp3')
        self.explosion_sound = pygame.mixer.Sound('sound/explosion.mp3')
        self.bgm_sound = pygame.mixer.Sound('sound/bgm.mp3')
        self.click_button_sound = pygame.mixer.Sound('sound/click_button.mp3')
        self.alien_shoot_sound = pygame.mixer.Sound('sound/alien_shoot_voice.mp3')
        self.boss_shoot_sound = pygame.mixer.Sound('sound/boss_shoot_voice.mp3')
        self.boss_explosion_sound = pygame.mixer.Sound('sound/boss_explosion_sound.mp3')


