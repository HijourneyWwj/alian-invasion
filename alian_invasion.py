import sys  # 提供与系统交互的能力，比如退出游戏
import os
from time import sleep
import pygame  # 游戏开发的库
import random
import math
import numpy as np

import alien
from settings import settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
from background import Background
from explosion import Explosion
from sound import Sound
from shield import Shield


class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        pygame.surfarray.use_arraytype('numpy')  # 确保使用 numpy array
        self.clock = pygame.time.Clock()
        self.settings = settings()  # 创建一个settings的实例
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        self.stats = GameStats(self)  # 创建一个用于存储游戏统计信息的实例
        self.sb = Scoreboard(self)
        self.ship = Ship(self)  # 此处的self，指的是AlienInvasion这个类的一个对象实例
        # self.ship.ship_use = "shoot"
        self.bullets = pygame.sprite.Group()  # 创建一个Group类下的实例
        self.aliens = pygame.sprite.Group()  # 创建一个Group类下的实例
        self.explosions = pygame.sprite.Group()  # 创建一个Group类下的实例，储存爆炸图片编组
        self.shields = pygame.sprite.Group()
        self._create_fleet()
        self.game_active = False  # 控制游戏启动状态
        self.play_button = Button(self, "Play", (0, 0, 255))  # 创建 play 按钮
        self.continue_button = Button(self, "Continue", (0, 0, 255))  # 创建 stop 按钮
        self.background = Background(self)
        self.sound = Sound()
        self._alien_shoot_event()

    def run_game(self):
        """开始游戏的主循环"""
        self.sound.play_music("bgm")
        self.background.update_background()
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
            # alien shoot 事件触发后
            elif event.type == self.alien_bullet_timer and self.settings.game_status:  # 游戏暂停时外星人停止发射子弹
                if self.stats.level % self.settings.boss_level == 0:  # 如果时boss 关卡，发射boss的子弹
                    self._fire_bullet("boss")
                else:
                    self._fire_bullet("alien")

    def _check_click_button(self, mouse_pos):  # 传入鼠标点击的位置以判断是否开启游戏
        """在玩家单击 Play 按钮时开始新游戏"""
        if not self.game_active and self.play_button.rect.collidepoint(
                mouse_pos):  # 检查鼠标点击的位置，是否在按钮的矩形内，mouse_pos是一个（x，y）元组，记录点击的位置
            self._start_game()  # 开始游戏
            self.sound.play_music("click_button")
        """玩家点击 continue 按钮时恢复游戏"""
        if self.game_active and self.continue_button.rect.collidepoint(mouse_pos):
            self._stop_or_continue_game(False)
            self.sound.play_music("click_button")

    def _start_game(self):  # 开始游戏并创建一系列资源，仅在游戏确认界面，鼠标点击play或这按键按p时启动
        self.stats.reset_stats()  # 重置游戏数据
        self.game_active = True  # 游戏活跃状态为真
        self._reset_ai_game()  # 清空外星人和子弹，并重新绘制飞船和外星人位置
        pygame.mouse.set_visible(False)  # 隐藏鼠标，减少对游戏干扰
        self.settings.initialize_dynamic_settings()  # 初始化设置里的动态项
        self.settings.game_status = True  # 设置的游戏状态为真
        self.sb._prep_score()  # 重新绘制得分（背后的逻辑是：先更新/重置game_stats里的score，再用_prep_score（）方法把socre绘制成图像，再当主程序的screen_update方法运行时，调用show_score方法展示在屏幕上）
        self.sb._prep_level()  # 重新绘制等级
        self.sb._prep_score_ships()  # 绘制分数板块的剩余飞船编组
        self.ship.show()
        self.ship.activate_shield()

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
            self._fire_bullet("ship")
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

    """定义 alien 发射子弹的触发事件"""

    def _alien_shoot_event(self):
        """alien 自动触发发射子弹"""
        self.alien_bullet_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.alien_bullet_timer, self.settings.alien_bullet_time_break)  # 根据设置里的外星人射击时间，控制发射时长

    def _update_bullets(self):
        """更新子弹的位置，并删除已消失的子弹"""
        self.bullets.update()  # 更新子弹位置
        # 检查子弹是否已经离开屏幕，离开则删除子弹
        for bullet in self.bullets.copy():  # python 限制循环内的数组不能改变长度，所以需要使用副本做判断，再通过副本的信息匹配到原始数据做删除
            if bullet.rect.bottom <= 0 or bullet.rect.top >= self.settings.screen_height:  # 前者判断ship的子弹超过屏幕顶部，后者判断alien的子弹超过屏幕底部
                self.bullets.remove(bullet)
            # print(len(self.bullets)) #检查是否删除了子弹
        self._check_collision()

    def _check_collision(self):
        # 区分子弹来源
        ship_bullets = [bullet for bullet in self.bullets if bullet.shooter == 'ship']
        ship_bullets_group = pygame.sprite.Group(ship_bullets)
        alien_bullets = [bullet for bullet in self.bullets if bullet.shooter == 'alien' or bullet.shooter == 'boss']
        alien_bullets_group = pygame.sprite.Group(alien_bullets)
        self._check_shipbullet_alien_collision(ship_bullets_group)
        self._check_alien_or_alienbullet_to_ship_collision(alien_bullets_group)

    def _check_shipbullet_alien_collision(self, ship_bullets_group):
        """判断飞船子弹和外星人的碰撞"""
        #判断boss 关卡，boss关卡有护盾计算
        if self.stats.level % self.settings.boss_level == 0:  # boss 关卡
            self._check_boss_blood(ship_bullets_group)
        else:  # 非boss 关卡
            collisions = pygame.sprite.groupcollide(ship_bullets_group, self.aliens, True, True,
                                                    pygame.sprite.collide_mask)
            if collisions:
                for collided_aliens in collisions.values():
                    for alien in collided_aliens:
                        explosion = Explosion(self, alien.rect.center, "alien")  # 在外星人的位置创建一个爆炸实例
                        self.explosions.add(explosion)  # 实例添加到爆炸类里，自动执行爆炸动画
                    self.stats.score += self.settings.alien_points * len(
                        collided_aliens)  # 更新分数，当子弹同时消除多个外星人时，需要乘以aliens的数，即第一个键值对的值的list长度
                    self.sound.play_music("explosion")
                self.sb._prep_score()
                self.sb.check_high_score()
        if not self.aliens:
            # 如果所有的外星人队列都被消灭了，就删除现有的子弹并创建一个新的外星舰队
            self.start_new_level()


    def _check_boss_blood(self,ship_bullets_group):
        boss_aliens = [alien for alien in self.aliens if alien.alien_type == 'boss'] #boss关卡只有一只boss alien
        boss = boss_aliens[0] #获取到对应的boss对象,并用于后续的计算
        current_time = pygame.time.get_ticks()  # 获取当前时间
        if current_time - boss.last_hit_time > boss.invincibility_duration:
            boss_collisions = pygame.sprite.groupcollide(ship_bullets_group, self.aliens,True, False,
                                                          pygame.sprite.collide_mask)
            if boss_collisions:
                # 更新最后一次碰撞时间
                boss.last_hit_time = current_time
                # 判断飞船血量，用血量抵挡一次伤害，直到血量为0。血量只抵挡子弹和飞船的碰撞伤害，若外星人到达屏幕底部则直接爆炸
                if boss.boss_blood > 1:
                    boss.boss_blood -= 1
                    # print(boss.boss_blood)
                else:
                    boss.kill()
                    explosion = Explosion(self, boss.rect.center, "boss")  # 在外星人的位置创建一个爆炸实例
                    self.explosions.add(explosion)  # 实例添加到爆炸类里，自动执行爆炸动画
                    self.stats.score += self.settings.boss_points
                    self.sound.play_music("boss_explosion")
                    self.sb._prep_score()
                    self.sb.check_high_score()

    def _check_alien_or_alienbullet_to_ship_collision(self, alien_or_alien_bullets_group):
        """判断外星人子弹和飞船的碰撞"""
        current_time = pygame.time.get_ticks()  # 获取当前时间
        if current_time - self.ship.last_hit_time > self.ship.invincibility_duration:
            ship_collisions = pygame.sprite.spritecollide(self.ship, alien_or_alien_bullets_group, True,
                                                          pygame.sprite.collide_mask)
            if ship_collisions:
                # 更新最后一次碰撞时间
                self.ship.last_hit_time = current_time
                # 判断飞船血量，用血量抵挡一次伤害，直到血量为0。血量只抵挡子弹和飞船的碰撞伤害，若外星人到达屏幕底部则直接爆炸
                if self.ship.ship_blood > 1:
                    self.ship.ship_blood -= 1
                else:
                    self._ship_explosion()  # 添加爆炸效果
                    self.ship.deactivate_shield()  # 飞船护盾消失
                    self._ship_hit()  # 更新剩余飞船数

    def _check_aliens_bottom(self):
        """检查是否有外星人到达了屏幕的下边缘,是则飞船爆炸"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_explosion()  # 添加爆炸效果
                self._ship_hit()
                break

    def start_new_level(self):
        self.stats.level += 1  # 游戏关卡+1，改变数值后，还需要调用方法更新图像
        self.bullets.empty()  # 清空子弹
        for shield in self.shields.copy():
            if shield.shield_owner == "boss":  # 在boss 关卡，过关后，仅删除boss的护盾
                self.shields.remove(shield)
        self._create_fleet()  # 创建新的飞船队列
        self.ship.ship_blood = self.settings.ship_blood #重置ship血量
        self.settings.increase_speed()  # 游戏提速
        self.sb._prep_level()  # 渲染当前等级

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        # 绘制背景图片
        self.background.blit_background()  # 绘制背景图
        self.background.update_background()  # 更新背景图
        if not self.ship.hidden:
            self.ship.blitme()  # 注意顺序，要在下一行代码前完成，这样才能执行下一行代码统一刷新页面
        if self.background.check_background_edges():
            self.background.bg_direction *= -1
        for bullet in self.bullets.sprites():  # 遍历group中的子弹，并且绘制到屏幕上
            bullet.draw_bullet()
        self.aliens.draw(self.screen)  # 将aliens编组里的alien都绘制到屏幕上
        self.sb.show_score()  # 显示得分（创建得分实例）
        if not self.game_active:  # 如果游戏处于非活动状态，就绘制 Play 按钮
            self.play_button.draw_button()
        if not self.settings.game_status and self.game_active:  # 如果游戏启动，但是处于暂停状态，就绘制 continue 按钮
            self.continue_button.draw_button()
        self.explosions.draw(self.screen)
        self.explosions.update()
        self.shields.draw(self.screen)
        pygame.display.flip()  # 让最近绘制的屏幕可见，确保每次用户操作完成后，游戏页面都跟随刷新

    def _fire_bullet(self, shooter):
        # 创建一颗子弹，并将其加入到group编组中
        if self.game_active:  # 游戏启动时才可以发射子弹
            if shooter == "ship":  # ship 发射子弹需要校验可发射子弹的最大数量
                self._fire_ship_bullet()
            """测试：alien 生成子弹"""
            if shooter == "alien":  # alien 发射子弹无数量限制
                self._fire_alien_bullet()
            if shooter == "boss":  # alien 发射子弹无数量限制
                self._fire_boss_bullet()

    def _fire_ship_bullet(self):
        """ship 发射子弹"""
        ship_bullets = [bullet for bullet in self.bullets if bullet.shooter == 'ship']
        ship_bullets_group = pygame.sprite.Group(ship_bullets)
        direction_vector_for_ship = pygame.Vector2(0, 1)  # 子弹从飞船向外星人的向量是个默认值
        if len(ship_bullets_group) < self.settings.ship_bullet_allowed:
            new_bullet = Bullet(self, "ship", self.ship.rect, direction_vector_for_ship)
            self.bullets.add(new_bullet)
            self.sound.play_music("ship_shoot")

    def _fire_alien_bullet(self):
        """alien 发射子弹"""
        if self.aliens.sprites():
            #  每次选择随机数量的外星人发射子弹，随着游戏提升，设置的同时发射数量会提升
            num_aliens_to_shoot = min(self.settings.alien_shoot_count, len(self.aliens.sprites()))
            chosen_aliens = random.sample(self.aliens.sprites(), num_aliens_to_shoot)
            for alien in chosen_aliens:
                ship_center = pygame.Vector2(self.ship.rect.center)
                alien_center = pygame.Vector2(alien.rect.center)
                direction_vector = ship_center - alien_center
                direction_vector_for_alien = direction_vector.normalize()
                new_bullet = Bullet(self, "alien", alien.rect, direction_vector_for_alien)
                self.bullets.add(new_bullet)
                self.sound.play_music("alien_shoot")

    def _fire_boss_bullet(self):
        """发射boss的子弹"""
        """计算boss的子弹发射角度"""
        num_bullets = self.settings.boss_bullet_count
        angle_step = 180 / (num_bullets - 1)  # 半圆角度步长
        alien_list = self.aliens.sprites()
        boss_alien_rect = alien_list[0].rect
        for i in range(num_bullets):
            angle = i * angle_step  # 计算每个子弹的角度
            direction_vector = pygame.Vector2(math.cos(math.radians(angle)), math.sin(math.radians(angle)))
            new_bullet = Bullet(self, 'boss', boss_alien_rect, direction_vector)
            self.bullets.add(new_bullet)
        self.sound.play_music("boss_shoot")

    def _create_fleet(self):
        """创建一个外星舰队"""
        if self.stats.level % self.settings.boss_level == 0:  # 如果是boss关卡，创建boss
            self._create_boss()
        else:
            self._create_alien_fleet()  # 如果是普通关卡，创建alien队伍

    def _create_boss(self):
        """在boss关卡，创建boss"""
        boss = Alien(self, "boss")
        boss.x = self.settings.screen_width / 2
        boss.rect.x = boss.x
        boss.rect.y = 30
        self.aliens.add(boss)

    def _create_alien_fleet(self):
        """在非boss关卡，创建外星人舰队"""
        temp_alien = Alien(self, "alien")  # 创建一个外星人，用于计算位置
        alien_width, alien_height = temp_alien.rect.size
        temp_alien.kill()  # 删除临时的外星人实例
        available_space_x = self.settings.screen_width - alien_width
        number_aliens_x = available_space_x // (2 * alien_width)
        available_space_y = self.settings.screen_height - 3 * alien_height
        number_rows = available_space_y // (2 * alien_height)

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """创建一个外星人并且放在当前行"""
        alien = Alien(self, "alien")
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
        # if pygame.sprite.spritecollideany(self.ship, self.aliens):  # 判断飞船和外星舰队是否有“碰撞”
        self._check_alien_or_alienbullet_to_ship_collision(self.aliens) # 检验飞船和外星人是否有碰撞，有则更新飞船血量
        # 检查是否有外星人到达了屏幕的下边缘
        self._check_aliens_bottom()

    # 测试爆炸
    def _ship_explosion(self):
        explosion = Explosion(self, self.ship.rect.center, "ship")  # 创建一个爆炸实例
        self.explosions.add(explosion)  # 将爆炸实例添加到类中，在画面中自动显示
        self.sound.play_music("explosion")  # 播放爆炸音效
        self.ship.hide()  # 隐藏飞船

    def _ship_hit(self):  # 更新剩余飞船数量
        """只在飞船爆炸时，使用此方法，三种情况飞船爆炸：
        1. 飞船被外星人子弹击中
        2. 飞船和外星人碰撞
        3. 外星人触达屏幕下方"""
        if self.stats.ships_left >= 1:  # 判断飞船剩余数量
            self.stats.ships_left -= 1  # 剩余飞船数量 - 1
            self.sb._prep_score_ships()  # 更新剩余飞船
            if self.stats.ships_left > 0:  # 仅在飞船数量大于 0 时重置游戏
                self._reset_ai_game()  # 调用重置游戏的方法
                # self.ship.activate_shield()  #激活护盾
        if self.stats.ships_left == 0:
            self.game_active = False  # 游戏暂停
            pygame.mouse.set_visible(True)  # 显示鼠标，可点击是否重新开始游戏
            self.ship.hide()
            self.ship.deactivate_shield()

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

    """在首次开始游戏，或者飞船剩余寿命-1时，重置游戏重置游戏"""

    def _reset_ai_game(self):  # 重置游戏
        self.aliens.empty()  # 清空外星人列表
        self.bullets.empty()  # 清空子弹列表
        self.shields.empty()  # 需要清空护盾，否则飞船会重复绘制护盾，boss关卡也会在重复绘制。无论清空与否，左上角都会有护盾显示
        self._create_fleet()  # 创建一个新的外星舰队
        self.ship.center_ship()  # 将飞船放在屏幕底部的中央
        self.ship.ship_blood = self.settings.ship_blood

if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()
