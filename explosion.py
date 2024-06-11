import pygame
import os
from pygame.sprite import Sprite

class Explosion(pygame.sprite.Sprite):
    def __init__(self, ai_game,center):
        super().__init__()
        self.screen = ai_game.screen
        # 获取爆炸图片的路径
        explosion_image_path = os.path.join(os.path.dirname(__file__), "images/new_boom2.png")
        # 加载爆炸图片并处理透明度
        self.image = pygame.image.load(explosion_image_path).convert_alpha()
        self.rect = self.image.get_rect(center=center)
        self.start_time = pygame.time.get_ticks()


    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > 200:  # 爆炸效果持续200毫秒
            self.kill()  # 移除爆炸精灵
            print("移除成功")

