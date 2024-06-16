import pygame
from pygame.sprite import Sprite

class Shield(Sprite):
    def __init__(self, parent, shield_color, initial_health):
        """初始化护盾"""
        super().__init__()
        self.parent = parent
        self.screen = parent.screen
        self.settings = parent.settings
        self.health = initial_health
        self.shield_color = shield_color

        # 创建一个半透明的圆形护盾
        self.radius = max(parent.rect.width, parent.rect.height) // 2 + 10
        self.image = pygame.Surface((2*self.radius, 2*self.radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.shield_color, (self.radius, self.radius), self.radius)

        self.rect = self.image.get_rect()
        self.update()

    def update(self):
        """更新护盾位置"""
        self.rect.center = self.parent.rect.center

    def draw(self):
        """绘制护盾"""
        self.screen.blit(self.image, self.rect)

    def take_damage(self, damage):
        """护盾受到伤害"""
        self.health -= damage
        if self.health <= 0:
            self.kill()
