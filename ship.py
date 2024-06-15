import pygame
from pygame.sprite import Sprite


class Ship(Sprite):  #继承 Sprite 以生成编组
    """管理飞船的类"""
    def __init__(self, ai_game):
        """初始化飞船并设置其初始位置"""
        super().__init__() #完成父类 sprite的初始化
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/new_ship.png')
        self.rect = self.image.get_rect()

        # 每艘飞船都放在屏幕底部的中央
        self.rect.midbottom = self.screen_rect.midbottom

        # 存储飞船的X浮点数
        self.x = float(self.rect.x)

        # 移动标志：判断飞船是否需要向右移动
        self.moving_right = False
        self.moving_left = False

        # 是否隐藏飞船的标志
        self.hidden = False

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image,(self.rect.x, self.rect.y - 20))

    def update(self):
        if self.settings.game_status:  # 当 game_status 的状态是true 进行中时，飞船才能左右移动
            if self.moving_right and self.rect.right < self.screen_rect.right:
                self.x += self.settings.ship_speed
            if self.moving_left and self.rect.left > 0:
                self.x -= self.settings.ship_speed
            # 使用self.x的值更新rect的值
            self.rect.x = self.x

    def center_ship(self):
        """将飞船放在屏幕底部的中央"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def hide(self):
        """隐藏飞船"""
        self.hidden = True

    def show(self):
        """显示飞船"""
        self.hidden = False