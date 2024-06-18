import pygame
from pygame.sprite import Sprite
from shield import Shield


class Alien(Sprite):
    def __init__(self, ai_game, alien_type):
        # 初始化外星人并设置起始位置
        super().__init__()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.alien_type = alien_type

        # boss 初始化护盾
        self.boss_shield_color = (224,57,235,64)  # 红色半透明护盾 (255, 0, 0, 64)
        self.boss_blood = self.settings.boss_blood  # 每次初始化boss的血量
        self.shield = None
        self.border_thickness = 80  # boss 护盾的厚度
        self.feather_radius = 25   # boss 护盾的羽化半径
        # boss无敌时间，用于子弹碰撞时避免因为帧刷新的原因重复计算伤害
        self.invincibility_duration = 100  # 在500毫秒内，ship无敌。
        self.last_hit_time = 0  # 上一次受到伤害的时间

        #初始化alien
        self._initialize_alien()



    def _initialize_alien(self):
        # 是否为外星人 boss 关卡,默认为假
        if self.ai_game.stats.level % self.settings.boss_level == 0:
            self.image = pygame.image.load('images/new_boss.png').convert_alpha()  # Load image with transparency
            self.rect = self.image.get_rect()
            self.alien_boss = True

            # 初始化护盾
            self.activate_shield()
            self.shield.visible = True

        else:
            self.image = pygame.image.load('images/new_alien2.png').convert_alpha()
            self.alien_boss = False
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        # 每个外星人最初都在屏幕的左上角区域
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)


    def activate_shield(self):
        """激活护盾"""
        self.shield = Shield(self, self.boss_shield_color, self.boss_blood,self.border_thickness,self.feather_radius)  # 传入boss的护盾色，血量等
        self.shield.shield_owner = "boss"
        self.shield.add(self.ai_game.shields)


    def deactivate_shield(self):
        """取消护盾"""
        if self.shield:
            self.shield.kill()
            self.shield = None

    def check_edges(self):
        """如果外星人位于屏幕边缘，就返回 True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        # 当游戏未暂停时，才向右移动外星人。否则不运动
        if self.settings.game_status:  # 当 game_status 的状态是true 进行中时，外星人才向右运动
            self.x += self.settings.alien_speed * self.settings.fleet_direction
            self.rect.x = self.x
        # 随着 boss 的位置更新，更新护盾的位置
        if self.ai_game.stats.level % self.settings.boss_level == 0 and self.shield:
            self.shield.update()
