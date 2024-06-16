import pygame
from pygame.sprite import Sprite
from shield import Shield


class Ship(Sprite):  #继承 Sprite 以生成编组
    """管理飞船的类"""
    def __init__(self, ai_game):
        """初始化飞船并设置其初始位置"""
        super().__init__() #完成父类 sprite的初始化
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        self.ship_blood = self.settings.ship_blood # 初始化ship 的血量
        self.image = pygame.image.load('images/new_ship.png')  # 加载飞船图像并获取其外接矩形
        self.rect = self.image.get_rect()
        # print(self.rect)
        # self.rect.midbottom = self.screen_rect.midbottom   # 每艘飞船都放在屏幕底部的中央
        self.rect.midbottom = (self.screen_rect.midbottom[0], self.screen_rect.midbottom[1] - 10)
        print(self.rect.midbottom)
        self.x = float(self.rect.x)  # 存储飞船的X浮点数
        self.moving_right = False # 移动标志：判断飞船是否需要向右移动
        self.moving_left = False
        self.hidden = False  # 是否隐藏飞船的标志
        self.shield = None
        self.shield_color = (255,255,255,64)


    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image,(self.rect.x, self.rect.y))
        # print(self.rect.x, self.rect.y)
        # print("center",self.rect.center)

    def update(self):
        if self.settings.game_status:  # 当 game_status 的状态是true 进行中时，飞船才能左右移动
            if self.moving_right and self.rect.right < self.screen_rect.right:
                self.x += self.settings.ship_speed
            if self.moving_left and self.rect.left > 0:
                self.x -= self.settings.ship_speed
            # 使用self.x的值更新rect的值
            self.rect.x = self.x

        # 更新护盾的位置
        if self.shield:
            self.shield.update()

    def activate_shield(self):
        """激活护盾"""
        self.shield = Shield(self,self.shield_color,self.ship_blood) #传入ship的护盾色，血量等
        self.shield.add(self.ai_game.shields)

    def deactivate_shield(self):
        """取消护盾"""
        if self.shield:
            self.shield.kill()
            self.shield = None

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