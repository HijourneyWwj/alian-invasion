import pygame
from pygame.sprite import Sprite
from shield import Shield
from health_bar import HealthBar


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
        self.image = pygame.image.load('images/new_ship3.png')  # 加载飞船图像并获取其外接矩形
        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.screen_rect.midbottom[0], self.screen_rect.midbottom[1] - 15)
        self.x = float(self.rect.x)  # 存储飞船的X浮点数
        self.y = float(self.rect.y)  # 存储飞船的X浮点数
        self.moving_right = False # 移动标志：判断飞船是否需要向右移动
        self.moving_left = False
        self.hidden = False  # 是否隐藏飞船的标志
        self.shield = None
        self.shield_color = (255,255,255,64)  # 护盾的颜色
        self.border_thickness = 20  # 护盾的厚度  20
        self.feather_radius = 12  # 护盾的羽化半径 12

        # 无敌时间，用于子弹碰撞时避免因为帧刷新的原因重复计算伤害
        self.invincibility_duration = 100  # 在500毫秒内，ship无敌。
        self.last_hit_time = 0  # 上一次受到伤害的时间
        # self.ship_use = ""

        # ship 血条
        self.ship_health_bar = HealthBar(self.screen, self.x, self.y,50, 5, self.settings.ship_blood, (255, 0, 0))
        self.ship_health_bar.draw()


    def blitme(self):
        """在指定位置绘制飞船"""
        if not self.hidden:
            self.screen.blit(self.image, (self.rect.x, self.rect.y))
            self.ship_health_bar.update_health(self.ship_blood)
            if self.shield and not self.hidden and self.is_fully_visible():
                self.shield.visible = True
                self.shield.update()
            else:
                if self.shield:
                    self.shield.visible = False

    def update(self):
        if self.settings.game_status and self.hidden == False:  # 当 game_status 的状态是true 进行中时，飞船才能左右移动
            if self.moving_right and self.rect.right < self.screen_rect.right:
                self.x += self.settings.ship_speed
            if self.moving_left and self.rect.left > 0:
                self.x -= self.settings.ship_speed
            # 使用self.x的值更新rect的值
            self.rect.x = self.x


    def activate_shield(self):
        """激活护盾"""
        # if self.ship_use == "shoot":
        self.shield = Shield(self,self.shield_color,self.ship_blood,self.border_thickness,self.feather_radius) #传入ship的护盾色，血量等.
        self.shield.shield_owner = "ship"
        self.shield.add(self.ai_game.shields)

    def deactivate_shield(self):
        """取消护盾"""
        if self.shield:
            self.shield.kill()
            self.shield = None

    def center_ship(self):
        """将飞船放在屏幕底部的中央，且向上15"""
        self.rect.midbottom = (self.screen_rect.midbottom[0], self.screen_rect.midbottom[1] - 15)
        self.x = float(self.rect.x)

    def hide(self):
        """隐藏飞船"""
        self.hidden = True

    def show(self):
        """显示飞船"""
        self.hidden = False


    def is_fully_visible(self):
        """检查飞船是否完全可见"""
        return self.rect.left >= 0 and self.rect.right <= self.screen_rect.right and \
               self.rect.top >= 0 and self.rect.bottom <= self.screen_rect.bottom