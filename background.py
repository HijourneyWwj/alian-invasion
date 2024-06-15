import pygame
import os

class Background():
    def __init__(self,ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # 游戏背景速度
        self.background_move_speed = 1

        # 加载背景图像并获取其外接矩形
        background_path = os.path.join(os.path.dirname(__file__), "images/bg_long.png")
        self.background = pygame.image.load(background_path).convert()
        # 调整背景图像大小以适应屏幕宽度
        self.background = pygame.transform.scale(self.background,
                                                 (self.screen_rect.width, self.background.get_height()))
        self.rect = self.background.get_rect()

        # 背景图放在屏幕底部的中央
        self.rect.midbottom = self.screen_rect.midbottom  # 让背景图midbottom的x y 值等于屏幕的midbottom xy值

        # 存储背景图的y浮点数
        self.y = float(self.rect.y)
        self.bg_direction = 1  # 背景图移动方向， 1 向上，-1 向下

    # 参考外星人的移动方式
    def check_background_edges(self):
        """判断背景图是否到达屏幕边缘，是返回 True"""
        screen_rect = self.screen.get_rect()
        if self.rect.top == 0 or self.rect.bottom == screen_rect.bottom:
            return True

    def update_background(self):
        """改变背景图的 Y 坐标，让背景图“运动”起来"""
        self.y += self.background_move_speed * self.bg_direction
        self.rect.y = self.y

    def blit_background(self):
        """在指定位置绘制背景图"""
        self.screen.blit(self.background, (self.rect.x, self.rect.y))
