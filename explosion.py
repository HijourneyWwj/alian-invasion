import pygame
import os
from time import sleep
from pygame.sprite import Sprite

class Explosion(pygame.sprite.Sprite):
    def __init__(self, ai_game,center,explosion_type):
        super().__init__()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.ship = ai_game.ship
        self.stats = ai_game.stats
        self.center = center
        # self.file = file

        # # 获取爆炸图片的路径
        # explosion_image_path = os.path.join(os.path.dirname(__file__), "images/new_boom2.png")   #
        # # 加载爆炸图片并处理透明度
        # self.image = pygame.image.load(explosion_image_path).convert_alpha()
        # self.rect = self.image.get_rect(center=center)
        # self.start_time = pygame.time.get_ticks()

        self._initialize_explosion()
        self.rect = self.image.get_rect(center=self.center)
        self.start_time = pygame.time.get_ticks()
        self.explosion_type = explosion_type  # 1 为飞船爆炸，0 为 boss 爆炸

    def _initialize_explosion(self):
        # 是否为外星人 boss 关卡
        if self.ai_game.stats.level % self.ai_game.settings.boss_level == 0:
            # 获取爆炸图片的路径
            explosion_image_path = os.path.join(os.path.dirname(__file__), "images/boss_explosion.png")
            # 加载爆炸图片并处理透明度
            self.image = pygame.image.load(explosion_image_path).convert_alpha()
        else:
            explosion_image_path = os.path.join(os.path.dirname(__file__), "images/alien_explosion.png")
            # 加载爆炸图片并处理透明度
            self.image = pygame.image.load(explosion_image_path).convert_alpha()


    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > 200:  # 爆炸效果持续200毫秒
            self.kill()  # 移除爆炸精灵
            if self.explosion_type == "ship" :
                # self.ship.deactivate_shield()
                sleep(0.5)  # 画面暂停 0.5 秒
                if self.stats.ships_left > 0:
                    self.ship.show()
                    self.ship.activate_shield()  #激活护盾
            if self.explosion_type == "boss":
                sleep(0.5)  # 画面暂停 0.5 秒


