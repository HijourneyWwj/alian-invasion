class GameStats:
    """跟踪游戏的统计信息"""

    def __init__(self, ai_game):
        """初始化统计信息"""
        self.settings = ai_game.settings
        self.reset_stats()  # 将初始化部分单独独立为方法，便于除开始游戏时的其他情况调用
        # self.high_score = 0
        self._get_high_score()

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def _get_high_score(self):
        with open("./high_score.txt", "r") as f:
            self.high_score = int(f.read())
