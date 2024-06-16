import pygame
from pygame.sprite import Sprite #使用sprite可以将游戏中相关的元素编组，进而同时操作编组中的所有元素

class Bullet(Sprite): #bullet 是 Spritte（精灵）的子类
    # 管理飞船所发射的子弹的类
    def __init__(self, ai_game,shooter):
        #在飞船的当前位置创建一个子弹对象
        super().__init__() # 用super（）的方法快速调用父类的init函数构造父类 Sprite 的属性，同时支持bullet创建自己的下列属性
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        """测试alien和ship都可以发射子弹"""
        if shooter == 'ship':
            self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
            self.rect.midtop = ai_game.ship.rect.midtop
            self.y = float(self.rect.y)
            self.speed_factor = -self.settings.bullet_speed  # 飞船子弹向上移动
        elif shooter == 'alien':
            self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
            self.rect.midbottom = ai_game.alien.rect.midbottom
            self.y = float(self.rect.y)
            self.speed_factor = self.settings.alien_bullet_speed  # 外星人子弹向下移动


        # #在(0,0) 处创建一个表示子弹的矩形，在设置正确的位置
        # self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        # self.rect.midtop = ai_game.ship.rect.midtop
        #
        # #存储浮点数表示子弹的位置
        # self.y = float(self.rect.y)


        # 创建一个用于mask的表面
        self.image = pygame.Surface((self.settings.bullet_width, self.settings.bullet_height))
        self.image.fill(self.settings.bullet_color)

        # 创建mask
        self.mask = pygame.mask.from_surface(self.image)


    def update(self):
        if self.settings.game_status:  # 当 game_status 的状态是true 进行中时，子弹才能向上运动
            #向上移动子弹
            #更新子弹的准确位置
            self.y += self.speed_factor
            # self.y -= self.settings.bullet_speed
            #更新子弹的rect 位置
            self.rect.y = self.y

    def draw_bullet(self):
        # 在屏幕上绘制子弹
        pygame.draw.rect(self.screen, self.color, self.rect)
