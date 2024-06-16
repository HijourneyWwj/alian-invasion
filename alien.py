import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self, ai_game):
        #初始化外星人并设置起始位置
        super().__init__()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self._initialize_alien()


    def _initialize_alien(self):
        # 是否为外星人 boss 关卡,默认为假
        if self.ai_game.stats.level % 5 == 0:
            self.image = pygame.image.load('images/alienboss.png').convert_alpha()  # Load image with transparency
            self.alien_boss = True
        else:
            self.image = pygame.image.load('images/new_alien.png').convert_alpha()
            self.alien_boss = False
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        # 每个外星人最初都在屏幕的左上角区域
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)


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

    def fire_bullet(self):
        """外星人发射子弹"""
        new_bullet = Bullet(self.ai_game, shooter='alien')
        self.ai_game.alien_bullets.add(new_bullet)

