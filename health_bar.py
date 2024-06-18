import pygame

class HealthBar:
    """为游戏创建血条的类"""
    def __init__(self, screen, x, y, width, height, max_health, color):
        """初始化健康条"""
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_health = max_health
        self.health = max_health
        self.color = color

    def update_health(self, new_health):
        """更新健康值"""
        self.health = max(0, min(new_health, self.max_health))

    def draw(self):
        """绘制健康条"""
        # 计算当前健康条的宽度
        current_health_ratio = self.health / self.max_health
        current_health_width = int(self.width * current_health_ratio)

        # 绘制背景框
        pygame.draw.rect(self.screen, (255, 255, 255), (self.x, self.y, self.width, self.height), 2)

        # 绘制当前健康值
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, current_health_width, self.height))
