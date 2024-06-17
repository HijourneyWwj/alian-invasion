import pygame
import numpy as np
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
        self.border_thickness = 5
        self.feather_radius = 10

        self.visible = False  # 新增属性来控制护盾的显示
        self.shield_owner = ""

        # 创建一个半透明的圆形护盾
        # self.radius = max(parent.rect.width, parent.rect.height) // 2 + 10
        # self.image = pygame.Surface((2*self.radius, 2*self.radius), pygame.SRCALPHA)
        # pygame.draw.circle(self.image, self.shield_color, (self.radius, self.radius), self.radius)

        #创建一个全透明的圆
        self.radius = max(parent.rect.width, parent.rect.height) // 2 + 10
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        # self.rect.center = parent.rect.center

        pygame.draw.circle(self.image, self.shield_color, (self.radius, self.radius), self.radius, self.border_thickness)  #
        # 羽化护盾的。让效果更明显
        # self.feather(self.image, self.radius, self.shield_color, self.border_thickness, self.feather_radius)

        self.update()

    """
    -->初始化创建护盾（init）
    -->在屏幕上绘制护盾（draw）（实测不需要这个方法也能绘制）
    -->随着游戏帧/主体运动更新护盾位置（upadte）
    -->在遇到上伤害时扣减护盾值（take_damage）
    -->护盾值为0时删除护盾（self.kill）
    """
    def draw(self):
        """绘制护盾"""
        if self.visible:
            self.screen.blit(self.image, self.rect)

    def update(self):
        """更新护盾位置"""
        if self.visible:
            self.rect.center = self.parent.rect.center

    def take_damage(self, damage):
        """护盾受到伤害"""
        self.health -= damage
        if self.health <= 0:
            self.kill()

    # def feather(self, surface, radius, color, border_thickness, feather_radius):
    #     """应用羽化效果"""
    #     width, height = surface.get_size()
    #     center_x, center_y = width // 2, height // 2
    #
    #     for y in range(height):
    #         for x in range(width):
    #             dist = np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
    #             if radius - border_thickness <= dist <= radius:
    #                 alpha = max(0, 255 - int((dist - (radius - border_thickness)) / feather_radius * 255))
    #                 surface.set_at((x, y), (*color[:3], alpha))
    #             elif dist > radius:
    #                 surface.set_at((x, y), (0, 0, 0, 0))
