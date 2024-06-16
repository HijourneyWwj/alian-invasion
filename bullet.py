import pygame
from pygame.sprite import Sprite #使用sprite可以将游戏中相关的元素编组，进而同时操作编组中的所有元素

class Bullet(Sprite): #bullet 是 Spritte（精灵）的子类
    # 管理飞船所发射的子弹的类
    def __init__(self, ai_game,shooter,sprite_rect):
        #在飞船的当前位置创建一个子弹对象
        super().__init__() # 用super（）的方法快速调用父类的init函数构造父类 Sprite 的属性，同时支持bullet创建自己的下列属性
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.shooter = shooter
        self.sprite_rect = sprite_rect
        self.check_shooter()
        # 创建mask
        self.mask = pygame.mask.from_surface(self.image)



    def check_shooter(self):
        """区分发射子弹的主体"""
        if self.shooter == 'ship':
            self.rect = pygame.Rect(0, 0, self.settings.ship_bullet_width, self.settings.ship_bullet_height)
            self.rect.midtop = self.sprite_rect.midtop
            self.y = float(self.rect.y)
            self.color = self.settings.ship_bullet_color
            self.image = pygame.Surface((self.settings.ship_bullet_width, self.settings.ship_bullet_height), pygame.SRCALPHA)
            self.image.fill((0, 0, 0, 0))
            # 使用相对于 self.image 的矩形来绘制椭圆
            pygame.draw.ellipse(self.image, self.color,
                                (0, 0, self.settings.ship_bullet_width, self.settings.ship_bullet_height))
            self.speed_factor = -self.settings.ship_bullet_speed  # 飞船子弹向上移动
            self.direction_vector = pygame.Vector2(0, 1)  # 子弹从飞船向外星人的向量是个默认值

        if self.shooter == 'alien':
            self.rect = pygame.Rect(0, 0, self.settings.alien_bullet_width, self.settings.alien_bullet_height)
            self.rect.midbottom = self.sprite_rect.midbottom
            self.y = float(self.rect.y)
            self.color = self.settings.alien_bullet_color
            self.image = pygame.Surface((self.settings.alien_bullet_width, self.settings.alien_bullet_height), pygame.SRCALPHA)
            self.image.fill((0, 0, 0, 0))
            pygame.draw.circle(self.image, self.color,
                               (self.settings.alien_bullet_width / 2, self.settings.alien_bullet_height / 2),
                               self.settings.alien_bullet_height / 2)
            self._calculate_direction()    #计算子弹从外星人到飞船的方向向量
            self.speed_factor = self.settings.ship_bullet_speed  # 外星人子弹向下移动,移动速度和飞船的保持一致
        # if self.shooter = 'boss':

    def update(self):
        if self.settings.game_status:  # 当 game_status 的状态是true 进行中时，子弹才能向上运动
            """让外星人子弹朝向飞船发射"""
            self.rect.x += self.direction_vector.x * self.speed_factor
            self.rect.y += self.direction_vector.y * self.speed_factor

    def _calculate_direction(self):
        """计算从外星人到飞船的方向向量，让外星人的子弹超飞船发射"""
        ship_center = pygame.Vector2(self.ai_game.ship.rect.center)
        alien_center = pygame.Vector2(self.sprite_rect.center)
        direction_vector = ship_center - alien_center
        self.direction_vector = direction_vector.normalize()  # 归一化方向向量

    def draw_bullet(self):
        # 在屏幕上绘制子弹
        self.screen.blit(self.image, self.rect)