import pygame
from pygame.sprite import Sprite

class SpecialMove(Sprite):
    def __init__(self, ai_game, move_type,game_level):
        """初始化特殊技能"""
        super().__init__()  # 确保调用 Sprite 的初始化方法
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.move_type = move_type
        self.game_level = game_level
        self._init_special_move()


    def _init_special_move(self):
        if self.move_type == "1":
            self.image = pygame.image.load('images/dragon2.png').convert_alpha()
        """待拓展其他"""
        # elif self.move_type == "2":
        #     self.image = pygame.image.load('images/new_alien2.png').convert_alpha()
        # elif self.move_type == "3":
        #     self.image = pygame.image.load('images/new_alien3.png').convert_alpha()

        if self.image:
            screen_height = self.screen.get_height()
            aspect_ratio = self.image.get_width() / self.image.get_height()
            new_width = int(screen_height * aspect_ratio)
            self.image = pygame.transform.scale(self.image, (new_width, screen_height))
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.midtop = self.screen.get_rect().midbottom  # 将图像置于屏幕底部中央
            self.y = float(self.rect.y)
            self.show = False

    def update(self):
        """更新特殊技能位置"""
        if self.y > -self.rect.height:
            self.y -= 20
            self.rect.y = self.y
        if self.rect.bottom <= self.screen.get_rect().top:  # 当完全离开屏幕顶部时，删除实例
            self.kill()