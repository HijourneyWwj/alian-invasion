class Settings:
    def __init__(self):
        """初始化游戏的静态设置"""
        # 屏幕设置
        self.screen_width = 1200  # 设置屏幕宽度
        self.screen_height = 800  # 设置屏幕高度
        self.bg_color = (230, 230, 230)  # 设置背景色

        # 飞船设置
        self.ship_limit = 3  # 限制飞船数量


        # ship 子弹设置
        self.ship_bullet_width = 1500  # 3
        self.ship_bullet_height = 12  # 15
        self.ship_bullet_color = (255, 165, 0)  # 原色(60, 60, 60)
        self.ship_bullet_allowed = 5  # 3
        self.ship_blood = 5  # ship 的初始血量，可以抵挡5次子弹的攻击

        # 外星人设置
        self.fleet_drop_speed = 70  # 原始10
        # alien 子弹设置
        self.alien_bullet_width = 10  # 3
        self.alien_bullet_height = 10  # 15
        self.alien_bullet_color = (70, 239, 232)
        self.boss_level = 2  # 能被此整出的关卡，为boss关卡

        # boss 设置
        self.boss_bullet_width = 20
        self.boss_bullet_height = 20
        self.boss_bullet_color = (224, 57, 235)  # 紫色


        # 游戏节奏
        self.speedup_level = 1
        self.speedup_scale = 1.1
        # 外星人得分的提高速度
        self.score_scale = 1.5

        self.game_status = False  # 游戏是否暂停,true 进行，false 暂停

        self.initialize_dynamic_settings()  # 调用方法创建动态的变量

    def initialize_dynamic_settings(self):
        """初始化动态设置"""
        self.ship_bullet_speed = 3.0  # 原始2
        self.ship_speed = 1.5  # 飞船左右运行速度
        self.alien_speed = 1.0
        self.fleet_direction = 1  # 外星人队列的易懂方向， 1 向右，-1 向左
        self.alien_points = 50  # 记分设置
        self.alien_bullet_time_break = 1200  # 外星人发射子弹的频率，初始1.2秒，随着游戏节奏逐渐加快，每次提升20毫秒
        self.boss_bullet_count = 7  # boss 每次同时发射5个子弹，随着游戏节奏的提高，数量变大
        self.alien_shoot_count = 2  # 外星人同时发射子弹的数量，随着游戏节奏的提高，数量变大
        self.boss_blood = 10  # boss 的初始血量，随着游戏等级的提高而提高，可以抵挡100次子弹的攻击
        self.boss_points = 2000


    def increase_speed(self):
        """提高速度设置的值,乘以游戏节奏"""
        self.speedup_level += 1
        self.ship_bullet_speed *= self.speedup_scale
        self.ship_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = round(int(self.alien_points * self.score_scale) / 10) * 10  # 取10的整数倍
        self.boss_points = round(int(self.boss_points * self.score_scale) / 10) * 10  # 取10的整数倍
        self.alien_bullet_time_break -= 20 * self.speedup_scale
        self.alien_shoot_count = round(self.alien_shoot_count * self.speedup_scale)
        self.boss_blood = int(self.boss_blood * self.speedup_scale)  # boss 血量跟随等级提高
        if self.speedup_level % self.boss_level == 0:  # 仅在每个boss 关卡后提升难度
            self.boss_bullet_count = round(self.boss_bullet_count * self.speedup_scale)