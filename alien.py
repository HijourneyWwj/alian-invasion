import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self, ai_game):
        #初始化外星人并设置起始位置
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        #加载外星人图像并设置其rect 属性
        self.image = pygame.image.load('images/new_alien.png')
        self.rect = self.image.get_rect()

        #每个外星人最初都在屏幕的左上角区域
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 加载外星人爆炸图片并获取rect属性
        self.boom_image = pygame.image.load('images/new_boom.png')
        self.boom_rect = self.boom_image.get_rect()

    def check_edges(self):
        """如果外星人位于屏幕边缘，就返回 True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        # 当游戏未暂停时，才向右移动外星人。否则不运动
        if self.settings.game_status: #当 game_status 的状态是true 进行中时，外星人才向右运动
            self.x += self.settings.alien_speed * self.settings.fleet_direction
            self.rect.x = self.x



