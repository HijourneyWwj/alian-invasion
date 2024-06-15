class settings:
    def __init__(self):
        """初始化游戏的静态设置"""
        # 屏幕设置
        self.screen_width = 1200 #设置屏幕宽度
        self.screen_height = 800 #设置屏幕高度
        self.bg_color = (230, 230, 230) # 设置背景色

        #飞船设置
        self.ship_limit = 3  # 限制飞船数量

        #子弹设置
        self.bullet_width = 3  #3
        self.bullet_height = 15  #15
        self.bullet_color = (255, 128, 0)   #原色(60, 60, 60)
        self.bullet_allowed = 5  #3

        #外星人设置
        self.fleet_drop_speed = 10  #原始10

        #游戏节奏
        self.speedup_scale = 1.1
        #外星人得分的提高速度
        self.score_scale = 1.5

        self.game_status = False  # 游戏是否暂停,true 进行，false 暂停

        self.initialize_dynamic_settings() #调用方法创建动态的变量


    def initialize_dynamic_settings(self):
        """初始化动态设置"""
        self.bullet_speed = 3.0  #原始2
        self.ship_speed = 1.5  #飞船左右运行速度
        self.alien_speed = 1.0
        self.fleet_direction = 1 #外星人队列的易懂方向， 1 向右，-1 向左
        self.alien_points = 50 #记分设置

    def increase_speed(self):
        """提高速度设置的值,乘以游戏节奏"""
        self.bullet_speed *= self.speedup_scale
        self.ship_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = round(int(self.alien_points * self.score_scale) / 10 ) * 10#取10的整数倍

