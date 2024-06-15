import sys  # 提供与系统交互的能力，比如退出游戏
import os
from time import sleep
import pygame  # 游戏开发的库

import alien
from settings import settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
# from background import Background
# # from sound import Sound
# from explosion import Explosion
# this is a test



class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = settings()  # 创建一个settings的实例
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        self.stats = GameStats(self)  # 创建一个用于存储游戏统计信息的实例
        self.sb = Scoreboard(self)
        self.ship = Ship(self)  # 此处的self，指的是AlienInvasion这个类的一个对象实例
        self.bullets = pygame.sprite.Group()  # 创建一个Group类下的实例
        self.aliens = pygame.sprite.Group()  # 创建一个Group类下的实例
        # self.explosions = pygame.sprite.Group()  # 创建一个Group类下的实例，储存爆炸图片编组
        self._create_fleet()
        self.game_active = False  # 控制游戏启动状态
        self.play_button = Button(self, "Play", (0, 0, 255))  # 创建 play 按钮
        self.continue_button = Button(self, "Continue", (0, 0, 255))  # 创建 stop 按钮
        # self.sound = Sound()
        # self.background = Background(self)

    def run_game(self):
        """开始游戏的主循环"""
        # self.sound.play_music("bgm")
        # self.background.update_background()
        while True:
            # 通过辅助方法，简化方法，并将事件循环隔离
            self._check_events()
            if self.game_active:  # 游戏状态为True时才启动
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            # 每次启动都重新绘制屏幕
            self._update_screen()
            self.clock.tick(60)  # 设置游戏帧率为60，pygame会尽可能确保循环每秒运行60次

    def _check_events(self):  # 带下划线的方法约定俗成为私密方法，只在指定的类里被使用，其他类不用
        """响应按键和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:  # 按键按下
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:  # 按键松开
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()  # 使用变量临时存储位置数据
                self._check_click_button(mouse_pos)

    def _check_click_button(self, mouse_pos):  # 传入鼠标点击的位置以判断是否开启游戏
        """在玩家单击 Play 按钮时开始新游戏"""
        if not self.game_active and self.play_button.rect.collidepoint(
                mouse_pos):  # 检查鼠标点击的位置，是否在按钮的矩形内，mouse_pos是一个（x，y）元组，记录点击的位置
            self._start_game()  # 重置游戏信息
            # self.sound.play_music("click_button")
        """玩家点击 continue 按钮时恢复游戏"""
        if self.game_active and self.continue_button.rect.collidepoint(mouse_pos):
            self._stop_or_continue_game(False)
            # self.sound.play_music("click_button")

    def _start_game(self):
        self.stats.reset_stats()
        self.game_active = True
        self._reset_ai_game()  # 清空外星人和子弹，并重新绘制飞船和外星人位置
        pygame.mouse.set_visible(False)  # 游戏开始时隐藏鼠标，减少对游戏干扰
        self.settings.initialize_dynamic_settings()
        self.settings.game_status = True
        self.sb._prep_score()  # 重新绘制得分（背后的逻辑是：先更新/重置game_stats里的score，再用_prep_score（）方法把socre绘制成图像，再当主程序的screen_update方法运行时，调用show_score方法展示在屏幕上）
        self.sb._prep_level()  # 重新绘制等级
        self.sb._prep_score_ships()  # 绘制分数板块的剩余飞船编组

    def _stop_or_continue_game(self, status):
        """控制游戏是否暂停，传入true暂停游戏，传入false继续游戏，此时外星人和子弹停止移动，飞船和子弹不可操作，并展现继续按钮"""
        # 需要创建对应的方法，让类下面的对象可以执行对应的操作
        self.settings.game_status = not status
        pygame.mouse.set_visible(status)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            # 向右移动飞船
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            # 向右移动飞船
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p and not self.game_active:
            self._start_game()
        elif event.key == pygame.K_ESCAPE:  # 按下esc时暂停游戏
            self._stop_or_continue_game(True)
        elif event.key == pygame.K_c:  # 按下c按键时游戏继续
            self._stop_or_continue_game(False)

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_bullets(self):
        """更新子弹的位置，并删除已消失的子弹"""
        # 更新子弹的数量
        self.bullets.update()
        # 检查子弹是否已经离开屏幕上方，离开则删除子弹
        for bullet in self.bullets.copy():  # python 限制循环内的数组不能改变长度，所以需要使用副本做判断，再通过副本的信息匹配到原始数据做删除
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
            # print(len(self.bullets)) 检查是否删除了子弹
        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        # 检查是否有子弹击中了外星人
        # 如果是，就删除相应的子弹和外星人
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)  # 判断子弹和外星人是否有碰撞（删除元素后，字典会变成0）
        if collisions:
            for collided_sprites in collisions.values():
                # for sprite in collided_sprites:
                    # explosion = Explosion(self, sprite.rect.center,0)  # 在外星人的位置创建一个爆炸实例
                    # self.explosions.add(explosion)  # 实例添加到爆炸类里，自动执行爆炸动画
                self.stats.score += self.settings.alien_points * len(
                    collided_sprites)  # 更新分数，当子弹同时消除多个外星人时，需要乘以aliens的数，即第一个键值对的值的list长度
                # self.sound.play_music("explosion")
            self.sb._prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            # 如果所有的外星人队列都被消灭了，就删除现有的子弹并创建一个新的外星舰队
            self.start_new_level()

    def start_new_level(self):
        self.bullets.empty()
        self._create_fleet()
        self.settings.increase_speed()
        self.stats.level += 1  # 改变数值后，还需要调用方法更新图像
        self.sb._prep_level()

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        # 绘制背景图片
        # self.background.blit_background()  # 绘制背景图
        # self.background.update_background()  #更新背景图
        if not self.ship.hidden:
            self.ship.blitme()  # 注意顺序，要在下一行代码前完成，这样才能执行下一行代码统一刷新页面
        # if self.background.check_background_edges():
        #     self.background.bg_direction *= -1
        # self.background.update_background()
        for bullet in self.bullets.sprites():  # 遍历group中的子弹，并且绘制到屏幕上
            bullet.draw_bullet()
        self.aliens.draw(self.screen)  # 将aliens编组里的alien都绘制到屏幕上
        self.sb.show_score()  # 显示得分（创建得分实例）
        if not self.game_active:  # 如果游戏处于非活动状态，就绘制 Play 按钮
            self.play_button.draw_button()
        if not self.settings.game_status and self.game_active:  # 如果游戏启动，但是处于暂停状态，就绘制 continue 按钮
            self.continue_button.draw_button()
        # self.explosions.draw(self.screen)
        # self.explosions.update()
        pygame.display.flip()  # 让最近绘制的屏幕可见，确保每次用户操作完成后，游戏页面都跟随刷新

    def _fire_bullet(self):
        # 创建一颗子弹，并将其加入到group编组中
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            # self.sound.play_music("shoot")

    def _create_fleet(self):
        """创建一个外星舰队"""
        # 创建一个外星人
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - alien_width
        number_aliens_x = available_space_x // (2 * alien_width)
        available_space_y = self.settings.screen_height - 3 * alien_height
        number_rows = available_space_y // (2 * alien_height)
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """创建一个外星人并且放在当前行"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        # 更新外星人群中所有外星人的位置
        self._check_fleet_edges()
        self.aliens.update()  # 编组调用方法时，会让所有的外星人都执行
        # 检测外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):  #判断飞船和外星舰队是否有“碰撞”
            # self._ship_explosion()  # 添加爆炸效果
            self._ship_hit()  # 更新剩余飞船数
        # 检查是否有外星人到达了屏幕的下边缘
        self._check_aliens_bottom()

    # 测试爆炸
    # def _ship_explosion(self):
    #     explosion = Explosion(self, self.ship.rect.center,1)  # 创建一个爆炸实例
    #     self.explosions.add(explosion)  # 将爆炸实例添加到类中，在画面中自动显示
    #     # self.sound.play_music("explosion")  # 播放爆炸音效
    #     self.ship.hide()  # 隐藏飞船

    def _ship_hit(self):
        """响应飞船和外星人的碰撞"""
        if self.stats.ships_left >= 1:  # 判断飞船剩余数量
            self.stats.ships_left -= 1  # 剩余飞船数量 - 1
            self.sb._prep_score_ships()  # 更新剩余飞船
            if self.stats.ships_left > 0:  # 仅在飞船数量大于 0 时重置游戏
                self._reset_ai_game()  # 调用重置游戏的方法
        if self.stats.ships_left == 0:
            self.game_active = False
            pygame.mouse.set_visible(True)  # 游戏开始时隐藏鼠标，减少对游戏干扰
            self.ship.hide()


    def _check_fleet_edges(self):
        """在有外星人到达边缘时采取相应的措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break  # 任意一个触碰边缘即结束循环

    def _change_fleet_direction(self):
        """将整个外星舰队向下移动，并改变它们的方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_aliens_bottom(self):
        """检查是否有外星人到达了屏幕的下边缘,则与触碰飞船同等处理"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # self._ship_explosion()  # 添加爆炸效果
                self._ship_hit()
                break

    def _reset_ai_game(self):  # 重置游戏
        self.aliens.empty()  # 清空外星人列表
        self.bullets.empty()  # 清空子弹列表
        self._create_fleet()  # 创建一个新的外星舰队
        self.ship.center_ship()  # 将飞船放在屏幕底部的中央
        # self.ship.show()  # 显示新的飞船



if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()
