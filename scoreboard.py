import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard():
    """显示得分信息的类"""
    def __init__(self,ai_game):
        """初始化显示得分涉及的属性"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # 显示得分信息时使用的字体设置
        self.text_color =(255, 255, 255)  # 黑色(0, 0, 0)
        self.font = pygame.font.SysFont(None, 48)  # 调用pygame的方法，生成按钮中文字的样式属性

        # 初始化得分图像
        self._prep_score()
        self._prep_high_score()
        self._prep_level()
        self._prep_score_ships()

    # 背后的逻辑是：先更新 / 重置game_stats里的score信息，用_prep_score（）方法把socre绘制成图像，再当主程序的screen_update方法运行时，调用show_score方法展示在屏幕上

    """绘制当前得分"""
    def _prep_score(self):
        """将 文本 渲染为图像，并使其在按钮上居中""" # Pygame 处理文本的方式font.render，将要显示的字符串渲染为图像。
        score_str = str(f"Score {self.stats.score:,}").encode('utf-8').decode('utf-8') # 将数字转为文本
        self.score_image = self.font.render(score_str,True,self.text_color,None) # 用font方法将文本转为图像
        self.score_rect = self.score_image.get_rect() #获取图像的矩形
        self.score_rect.right  = self.screen_rect.right - 20 #让图片位置设置在屏幕右上
        self.score_rect.top = 20 #让图片位置设置在屏幕右上

    """绘制历史最高分"""
    def _prep_high_score(self):
        high_score_str = str(f"Highest Score {self.stats.high_score:,}")  # 将数字转为文本
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, None)  # 用font方法将文本转为图像
        self.high_score_rect = self.high_score_image.get_rect()  # 获取图像的矩形
        self.high_score_rect.centerx = self.screen_rect.centerx  # 让图片位置设置在屏幕中间
        self.high_score_rect.top = self.screen_rect.top + 20  # 让图片位置设置在屏幕中间

    """检验历史最高分，并做更新"""
    def check_high_score(self):
        if self.stats.score > self.stats.high_score: #新的积分大于历史最高分时（每次当有外星人被击落都需要判断，所以在外星人主程序也要调用此方法）
            self.stats.high_score = self.stats.score # 让最高分等于最新的积分
            self._prep_high_score()
            with open("./high_score.txt", "w") as f:
                f.write(str(self.stats.high_score))

    """绘制当前关卡等级"""
    def _prep_level(self):
        level_str = str(f"Level {self.stats.level:,}")  # 将数字转为文本
        self.level_image = self.font.render(level_str, True, self.text_color, None)  # 用font方法将文本转为图像
        self.level_rect = self.level_image.get_rect()  # 获取图像的矩形
        self.level_rect.right = self.score_rect.right  # 让图片位置设置在屏幕右上角
        self.level_rect.top = self.score_rect.bottom + 10  # 让图片位置设置在得分下方


    """在屏幕上显示得分、等级和余下的飞船"""
    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.score_ships.draw(self.screen) #让score_ships编组调用draw方法绘制剩余的飞船

    """绘制剩余飞船数"""
    def _prep_score_ships(self):
        self.score_ships = Group() # 给飞船创建一个编组
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.score_ships.add(ship)
