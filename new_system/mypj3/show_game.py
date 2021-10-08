import pygame
from pygame import Surface, mixer
from pygame.locals import *
from typing import List, Tuple
import time
from game_number_guess import NumberGuess
import sys
# mixer.Sound("--.mp3") #音の再生


pygame.init()
mixer.init()
numberguess = NumberGuess()


class ShowGame:

    def __init__(self,
                 lv: int = 1,
                 num: List[int] = [0, 1, 2, 3, 4],
                 turn: int = 1,
                 max_hp: int = 100,
                 display_size: Tuple[int] = (360, 640),
                 stage1_damage: int = 4,
                 stage1_exp: int = 10,
                 enemy_level: int = 0,
                 stage_num: int = 3
                 ):
        self.lv = lv
        self.num = num
        self.turn = turn
        self.max_hp = max_hp
        self.screen = pygame.display.set_mode(display_size)
        self.damage_list = [stage1_damage, 20, 30]
        self.exp_list = [stage1_exp, 20, 30]
        self.enemy_level = enemy_level
        self.stage_num = stage_num
        self.gamescene = 0
        self.error_count = 0
        self.history_count = 0
        self.guess_list = []
        self.running = True
        self.hit = 0
        self.blow = 0
        self.ans = [0, 0, 0, 0, 0]

    def set_player(self, X: int = 118, Y: int = 50):
        """ホーム画面の立ち絵の設定
        """
        self.img = pygame.image.load("./mypj3/img/player.png")
        self.player_place = (X, Y)

    def set_mark(self):
        """入力用マークの設定
        """
        self.b_moon_img = pygame.image.load("./mypj3/img/b_moon.png")
        self.b_snow_img = pygame.image.load("./mypj3/img/b_snow.png")
        self.b_star_img = pygame.image.load("./mypj3/img/b_star.png")
        self.b_sun_img = pygame.image.load("./mypj3/img/b_sun.png")
        self.g_moon_img = pygame.image.load("./mypj3/img/g_moon.png")
        self.g_snow_img = pygame.image.load("./mypj3/img/g_snow.png")
        self.g_star_img = pygame.image.load("./mypj3/img/g_star.png")
        self.g_sun_img = pygame.image.load("./mypj3/img/g_sun.png")
        self.p_moon_img = pygame.image.load("./mypj3/img/p_moon.png")
        self.p_snow_img = pygame.image.load("./mypj3/img/p_snow.png")
        self.p_star_img = pygame.image.load("./mypj3/img/p_star.png")
        self.p_sun_img = pygame.image.load("./mypj3/img/p_sun.png")
        self.y_moon_img = pygame.image.load("./mypj3/img/y_moon.png")
        self.y_snow_img = pygame.image.load("./mypj3/img/y_snow.png")
        self.y_star_img = pygame.image.load("./mypj3/img/y_star.png")
        self.y_sun_img = pygame.image.load("./mypj3/img/y_sun.png")

        self.b_moon_s_img = pygame.image.load("./mypj3/img/b_moon_s.png")
        self.b_snow_s_img = pygame.image.load("./mypj3/img/b_snow_s.png")
        self.b_star_s_img = pygame.image.load("./mypj3/img/b_star_s.png")
        self.b_sun_s_img = pygame.image.load("./mypj3/img/b_sun_s.png")
        self.g_moon_s_img = pygame.image.load("./mypj3/img/g_moon_s.png")
        self.g_snow_s_img = pygame.image.load("./mypj3/img/g_snow_s.png")
        self.g_star_s_img = pygame.image.load("./mypj3/img/g_star_s.png")
        self.g_sun_s_img = pygame.image.load("./mypj3/img/g_sun_s.png")
        self.p_moon_s_img = pygame.image.load("./mypj3/img/p_moon_s.png")
        self.p_snow_s_img = pygame.image.load("./mypj3/img/p_snow_s.png")
        self.p_star_s_img = pygame.image.load("./mypj3/img/p_star_s.png")
        self.p_sun_s_img = pygame.image.load("./mypj3/img/p_sun_s.png")
        self.y_moon_s_img = pygame.image.load("./mypj3/img/y_moon_s.png")
        self.y_snow_s_img = pygame.image.load("./mypj3/img/y_snow_s.png")
        self.y_star_s_img = pygame.image.load("./mypj3/img/y_star_s.png")
        self.y_sun_s_img = pygame.image.load("./mypj3/img/y_sun_s.png")
        self.marks = {0: self.b_moon_img, 1: self.b_snow_img, 2: self.b_star_img, 3: self.b_sun_img,
                      4: self.g_moon_img, 5: self.g_snow_img, 6: self.g_star_img, 7: self.g_sun_img,
                      8: self.p_moon_img, 9: self.p_snow_img, 10: self.p_star_img, 11: self.p_sun_img,
                      12: self.y_moon_img, 13: self.y_snow_img, 14: self.y_star_img, 15: self.y_sun_img
                      }
        self.marks_s = {0: self.b_moon_s_img, 1: self.b_snow_s_img, 2: self.b_star_s_img, 3: self.b_sun_s_img,
                        4: self.g_moon_s_img, 5: self.g_snow_s_img, 6: self.g_star_s_img, 7: self.g_sun_s_img,
                        8: self.p_moon_s_img, 9: self.p_snow_s_img, 10: self.p_star_s_img, 11: self.p_sun_s_img,
                        12: self.y_moon_s_img, 13: self.y_snow_s_img, 14: self.y_star_s_img, 15: self.y_sun_s_img
                        }
        self.mark_buttonrect = []
        for n in range(5):
            self.mark_buttonrect.append(Rect(10+n*70, 425, 60, 25))

    def set_enemy(self):
        """敵の設定
        """
        self.enemy1_img = pygame.image.load("./mypj3/img/enemy1.png")
        self.enemy1_damage_img = pygame.image.load(
            "./mypj3/img/enemy1_damage.png")
        self.enemy2_img = pygame.image.load("./mypj3/img/enemy2.png")
        self.enemy2_damage_img = pygame.image.load(
            "./mypj3/img/enemy2_damage.png")
        self.enemy3_img = pygame.image.load("./mypj3/img/enemy3.png")
        self.enemy3_damage_img = pygame.image.load(
            "./mypj3/img/enemy3_damage.png")
        self.enemy_list = {1: self.enemy1_img,
                           2: self.enemy2_img, 3: self.enemy3_img}
        self.enemy_damage_list = {1: self.enemy1_damage_img,
                                  2: self.enemy2_damage_img, 3: self.enemy3_damage_img}
        self.enemyrect = Rect(93, 60, 187, 250)

    def set_button(self,
                   normal_button_place: Tuple[int] = (80, 300, 200, 50),
                   boss_button_place: Tuple[int] = (80, 375, 200, 50),
                   how_to_play_button_place: Tuple[int] = (80, 550, 200, 50),
                   return_button_place: Tuple[int] = (80, 550, 200, 50),
                   prev_button_place: Tuple[int] = (50, 500, 120, 30),
                   next_button_place: Tuple[int] = (190, 500, 120, 30),
                   history_button_place: Tuple[int] = (120, 570, 120, 30)):
        """ボタンの設定
        """
        self.normal_buttonrect = Rect(normal_button_place)
        self.boss_buttonrect = Rect(boss_button_place)
        self.how_to_play_buttonrect = Rect(how_to_play_button_place)
        self.return_buttonrect = Rect(return_button_place)
        self.prev_buttonrect = Rect(prev_button_place)
        self.next_buttonrect = Rect(next_button_place)
        self.history_buttonrect = Rect(history_button_place)
        self.stage_select_buttonrect = []
        for i in range(self.stage_num):
            self.stage_select_buttonrect.append(Rect(80, 100+100*i, 200, 50))
        self.normal_button_img = pygame.image.load(
            "./mypj3/img/normal_button.png")
        self.boss_button_img = pygame.image.load("./mypj3/img/boss_button.png")
        self.how_to_play_button_img = pygame.image.load(
            "./mypj3/img/how_to_button.png")
        self.return_button_img = pygame.image.load("./mypj3/img/return.png")
        self.prev_button_img = pygame.image.load("./mypj3/img/prev.png")
        self.next_button_img = pygame.image.load("./mypj3/img/next.png")
        self.history_button_img = pygame.image.load(
            "./mypj3/img/history_button.png")
        self.how_to_play_img = pygame.image.load("./mypj3/img/how_to_play.png")

    def set_mark_entry(self):
        """マーク入力用の設定
        """
        self.up_button_img = pygame.image.load("./mypj3/img/up.png")
        self.down_button_img = pygame.image.load("./mypj3/img/down.png")
        self.up_buttonrect = []
        for n in range(5):
            self.up_buttonrect.append(Rect(10+n*70, 400, 60, 25))
        self.down_buttonrect = []
        for n in range(5):
            self.down_buttonrect.append(Rect(10+n*70, 485, 60, 25))
        self.enter_button_img = pygame.image.load("./mypj3/img/enter.png")
        self.enter_buttonrect = Rect(120, 520, 120, 32)

    def set_sound(self):
        self.bgm_dict = {"normal": "./mypj3/sound/normal_BGM.mp3",
                         "boss": "./mypj3/sound/boss.mp3",
                         "home": "./mypj3/sound/home.mp3",
                         "clear": "./mypj3/sound/clear_bgm.mp3",
                         "failed": "./mypj3/sound/failed_bgm.mp3"}
        self.se_dict = {"attack": "./mypj3/sound/attacked.mp3",
                        "start": "./mypj3/sound/start.mp3",
                        "clear": "./mypj3/sound/clear_se.mp3",
                        "failed": "./mypj3/sound/failed_se.mp3"}

    def reset(self):
        """ゲーム関係の数値のリセット
        """
        self.hp = self.max_hp
        self.turn = 1
        self.hit = 0
        self.blow = 0
        self.guess_list = []
        self.hit_list = []
        self.blow_list = []
        self.num = [0, 1, 2, 3, 4]
        self.enemy_level = 0

    def home_show(self):
        """ホーム画面の描画
        """
        self.screen.blit(self.img, self.player_place)  # imgの描画・updateされてるから
        self.font = pygame.font.SysFont(None, 40)  # フォントの指定
        lv_display = self.font.render("Lv {}".format(
            self.lv), True, (255, 255, 255))  # 文字・色の指定
        self.screen.blit(lv_display, (150, 220))  # テキストの位置
        self.screen.blit(self.normal_button_img, self.normal_buttonrect)
        self.screen.blit(self.boss_button_img, self.boss_buttonrect)
        self.screen.blit(self.how_to_play_button_img,
                         self.how_to_play_buttonrect)

    def home_judge(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 上の×ボタンで閉じる
                self.running = False
            if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
                if self.normal_buttonrect.collidepoint(event.pos):
                    self.gamescene = 1  # normal stageへ
                    numberguess.make_1ans()    # 新しい答えの生成が必要
                    pygame.mixer.Channel(0).play(
                        pygame.mixer.Sound(self.se_dict["start"]))
                    time.sleep(2)
                if self.boss_buttonrect.collidepoint(event.pos):
                    self.gamescene = 2  # boss stageへ
                    numberguess.make_1ans()  # 新しい答えの生成
                    pygame.mixer.Channel(0).play(
                        pygame.mixer.Sound(self.se_dict["start"]))
                    self.load_show()  # ロード画面
                    # bossが解く
                    time.sleep(2)

                if self.how_to_play_buttonrect.collidepoint(event.pos):
                    self.gamescene = 5  # how to playへ

    def load_show(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 40)
        load_message = font.render("Now Loading...", True, (255, 255, 255))
        self.screen.blit(load_message, (150, 450))
        pygame.display.update()

    def error_show(self):
        """エラー画面の描画
        """
        self.font4 = pygame.font.SysFont(None, 33)
        error_message = self.font4.render(
            "! Cannot enter the same mark !", True, (255, 0, 0))
        self.screen.blit(error_message, (18, 300))
        self.screen.blit(self.return_button_img, self.return_buttonrect)

    def history_show(self):
        """履歴の描画1ページ目
        """
        font = pygame.font.SysFont(None, 30)
        if self.turn > 10:
            for i in range(10):
                for j in range(5):
                    self.screen.blit(
                        self.guess_list[i][j], (30+j*40, 55+i*40, 30, 30))
                turn = font.render("{}".format(i+1), True, (255, 255, 255))
                self.screen.blit(turn, (3, 60+i*40))
                pygame.draw.line(self.screen, (100, 100, 100),
                                 (25, 50+i*40), (25, 90+i*40), 1)
                pygame.draw.line(self.screen, (100, 100, 100),
                                 (0, 90+i*40), (360, 90+i*40), 1)
                hit_blow = font.render("Hit:{} Blow:{}".format(
                    self.hit_list[i], self.blow_list[i]), True, (255, 255, 255))
                self.screen.blit(hit_blow, (230, 60+i*40))

        else:
            for i in range(self.turn-1):
                for j in range(5):
                    self.screen.blit(
                        self.guess_list[i][j], (30+j*40, 55+i*40, 30, 30))
                turn = font.render("{}".format(i+1), True, (255, 255, 255))
                self.screen.blit(turn, (3, 60+i*40))
                pygame.draw.line(self.screen, (100, 100, 100),
                                 (25, 50+i*40), (25, 90+i*40), 1)
                pygame.draw.line(self.screen, (100, 100, 100),
                                 (0, 90+i*40), (360, 90+i*40), 1)
                hit_blow = font.render("Hit:{} Blow:{}".format(
                    self.hit_list[i], self.blow_list[i]), True, (255, 255, 255))
                self.screen.blit(hit_blow, (230, 60+i*40))
        if self.turn > 11:
            self.screen.blit(self.next_button_img, self.next_buttonrect)
        self.screen.blit(self.return_button_img, self.return_buttonrect)

    def history_judge(self):
        """履歴のボタンの判別1ページ目
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
                if self.return_buttonrect.collidepoint(event.pos):
                    self.history_count = 0
                if self.turn > 11:
                    if self.next_buttonrect.collidepoint(event.pos):
                        self.history_count = 2

    def history2_show(self):
        """履歴の描画2,3ページ目
        """
        font = pygame.font.SysFont(None, 30)
        if self.turn > self.history_count*10:
            for i in range((self.history_count-1)*10, self.history_count*10):
                for j in range(5):
                    self.screen.blit(
                        self.guess_list[i][j], (30+j*40, 55+(i-(self.history_count-1)*10)*40, 30, 30))
                turn = font.render("{}".format(i+1), True, (255, 255, 255))
                self.screen.blit(
                    turn, (3, 60+(i-(self.history_count-1)*10)*40))
                pygame.draw.line(self.screen, (100, 100, 100), (25, 50+(
                    i-(self.history_count-1)*10)*40), (25, 90+(i-(self.history_count-1)*10)*40), 1)
                pygame.draw.line(self.screen, (100, 100, 100), (0, 90+(
                    i-(self.history_count-1)*10)*40), (360, 90+(i-(self.history_count-1)*10)*40), 1)
                hit_blow = font.render("Hit:{} Blow:{}".format(
                    self.hit_list[i], self.blow_list[i]), True, (255, 255, 255))
                self.screen.blit(
                    hit_blow, (230, 60+(i-(self.history_count-1)*10)*40))

        else:
            for i in range((self.history_count-1)*10, self.turn-1):
                for j in range(5):
                    self.screen.blit(
                        self.guess_list[i][j], (30+j*40, 55+(i-(self.history_count-1)*10)*40, 30, 30))
                turn = font.render("{}".format(i+1), True, (255, 255, 255))
                self.screen.blit(
                    turn, (3, 60+(i-(self.history_count-1)*10)*40))
                pygame.draw.line(self.screen, (100, 100, 100), (25, 50+(
                    i-(self.history_count-1)*10)*40), (25, 90+(i-(self.history_count-1)*10)*40), 1)
                pygame.draw.line(self.screen, (100, 100, 100), (0, 90+(
                    i-(self.history_count-1)*10)*40), (360, 90+(i-(self.history_count-1)*10)*40), 1)
                hit_blow = font.render("Hit:{} Blow:{}".format(
                    self.hit_list[i], self.blow_list[i]), True, (255, 255, 255))
                self.screen.blit(
                    hit_blow, (230, 60+(i-(self.history_count-1)*10)*40))
        if self.turn > self.history_count*10+1:
            self.screen.blit(self.next_button_img, self.next_buttonrect)
        self.screen.blit(self.prev_button_img, self.prev_buttonrect)
        self.screen.blit(self.return_button_img, self.return_buttonrect)

    def history2_judge(self):
        """履歴のボタンの判別2,3ページ目
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
                if self.return_buttonrect.collidepoint(event.pos):
                    self.history_count = 0
                if self.turn > self.history_count*10+1:
                    if self.next_buttonrect.collidepoint(event.pos):
                        self.history_count += 1
                if self.prev_buttonrect.collidepoint(event.pos):
                    self.history_count -= 1

    def historylast_show(self):
        """履歴の描画最終ページ
        """
        font = pygame.font.SysFont(None, 30)
        for i in range((self.history_count-1)*10, self.turn-1):
            for j in range(5):
                self.screen.blit(
                    self.guess_list[i][j], (30+j*40, 55+(i-(self.history_count-1)*10)*40, 30, 30))
            turn = font.render("{}".format(i+1), True, (255, 255, 255))
            self.screen.blit(turn, (3, 60+(i-(self.history_count-1)*10)*40))
            pygame.draw.line(self.screen, (100, 100, 100), (25, 50+(
                i-(self.history_count-1)*10)*40), (25, 90+(i-(self.history_count-1)*10)*40), 1)
            pygame.draw.line(self.screen, (100, 100, 100), (0, 90+(
                i-(self.history_count-1)*10)*40), (360, 90+(i-(self.history_count-1)*10)*40), 1)
            hit_blow = font.render("Hit:{} Blow:{}".format(
                self.hit_list[i], self.blow_list[i]), True, (255, 255, 255))
            self.screen.blit(
                hit_blow, (230, 60+(i-(self.history_count-1)*10)*40))
        self.screen.blit(self.prev_button_img, self.prev_buttonrect)
        self.screen.blit(self.return_button_img, self.return_buttonrect)

    def historylast_judge(self):
        """履歴のボタンの判別最終ページ
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
                if self.return_buttonrect.collidepoint(event.pos):
                    self.history_count = 0
                if self.prev_buttonrect.collidepoint(event.pos):
                    self.history_count -= 1

    def stage_select(self):
        """ステージセレクト画面
        """
        font = pygame.font.SysFont(
            "bizudminchomediumbizudpminchomediumtruetype", 30)
        level = font.render("ステージを選んで下さい", True, "WHITE")
        self.screen.blit(level, (11, 10))
        font2 = pygame.font.SysFont("algerian", 40)
        for i in range(self.stage_num):  # ステージの数だけ描画
            level = font2.render("LEVEL:{}".format(i+1), True, "WHITE")
            self.screen.blit(level, (100, 100+100*i))
        self.screen.blit(self.return_button_img, self.return_buttonrect)

    def judge_stage_select(self):
        """ステージセレクト画面のボタンの判定
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
                for i in range(self.stage_num):
                    if self.stage_select_buttonrect[i].collidepoint(event.pos):
                        self.enemy_level = i+1
                        pygame.mixer.Channel(0).play(
                            pygame.mixer.Sound(self.se_dict["start"]))
                        time.sleep(2)
                        if self.gamescene == 1:
                            pygame.mixer.music.load(self.bgm_dict["normal"])
                            pygame.mixer.music.set_volume(0.3)
                            pygame.mixer.music.play(loops=-1)
                        elif self.gamescene == 2:
                            pygame.mixer.music.load(self.bgm_dict["boss"])
                            pygame.mixer.music.set_volume(0.3)
                            pygame.mixer.music.play(loops=-1)
                if self.return_buttonrect.collidepoint(event.pos):
                    self.gamescene = 0

    def normal_stage(self):
        """通常ステージの描画
        """
        self.screen.blit(
            self.enemy_list[self.enemy_level], self.enemyrect)  # 敵の描画
        font2 = pygame.font.SysFont(None, 30)  # turnの表示
        stage = font2.render("turn:{}".format(
            self.turn), True, (255, 255, 255))
        pygame.draw.line(self.screen, (0, 200, 0), (30, 40),
                         (30+self.hp, 40), 10)  # HPの表示
        font3 = pygame.font.SysFont(None, 20)
        hp_word = font3.render("HP", True, (255, 255, 255))
        hp_value = font3.render("{}".format(self.hp), True, (255, 255, 255))
        damage = (self.turn-1)*self.damage_list[self.enemy_level-1]
        if damage != 0:
            pygame.draw.line(self.screen, (200, 0, 0),
                             (30+self.hp, 40), (30+self.hp+damage, 40), 10)
        font4 = pygame.font.SysFont(None, 50)
        hit_blow = font4.render("Hit:{}   Blow:{}".format(
            self.hit, self.blow), True, (255, 255, 255))
        self.screen.blit(stage, (5, 5))
        self.screen.blit(hp_word, (5, 35))
        self.screen.blit(hp_value, (30+self.hp+damage+2, 35))
        self.screen.blit(hit_blow, (80, 360))
        self.screen.blit(self.enter_button_img, self.enter_buttonrect)
        self.screen.blit(self.history_button_img, self.history_buttonrect)
        self.mark_show()

    def normal_stage_judge(self):
        """ノーマルステージでのボタンの判定
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 上の×ボタンで閉じる
                self.running = False
            if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
                if self.up_buttonrect[0].collidepoint(event.pos):
                    self.num[0] += 1
                    if self.num[0] == 16:
                        self.num[0] = 0
                if self.down_buttonrect[0].collidepoint(event.pos):
                    self.num[0] -= 1
                    if self.num[0] == -1:
                        self.num[0] = 15
                if self.up_buttonrect[1].collidepoint(event.pos):
                    self.num[1] += 1
                    if self.num[1] == 16:
                        self.num[1] = 0
                if self.down_buttonrect[1].collidepoint(event.pos):
                    self.num[1] -= 1
                    if self.num[1] == -1:
                        self.num[1] = 15
                if self.up_buttonrect[2].collidepoint(event.pos):
                    self.num[2] += 1
                    if self.num[2] == 16:
                        self.num[2] = 0
                if self.down_buttonrect[2].collidepoint(event.pos):
                    self.num[2] -= 1
                    if self.num[2] == -1:
                        self.num[2] = 15
                if self.up_buttonrect[3].collidepoint(event.pos):
                    self.num[3] += 1
                    if self.num[3] == 16:
                        self.num[3] = 0
                if self.down_buttonrect[3].collidepoint(event.pos):
                    self.num[3] -= 1
                    if self.num[3] == -1:
                        self.num[3] = 15
                if self.up_buttonrect[4].collidepoint(event.pos):
                    self.num[4] += 1
                    if self.num[4] == 16:
                        self.num[4] = 0
                if self.down_buttonrect[4].collidepoint(event.pos):
                    self.num[4] -= 1
                    if self.num[4] == -1:
                        self.num[4] = 15
                if self.enter_buttonrect.collidepoint(event.pos):
                    for i in self.num:
                        if self.num.count(i) > 1:
                            self.error_count = 1  # 同じ数字が１つ以上含まれるときにerror=1にする
                    if self.error_count == 0:
                        guess_mark = [self.marks_s[self.num[0]], self.marks_s[self.num[1]],
                                      self.marks_s[self.num[2]], self.marks_s[self.num[3]], self.marks_s[self.num[4]]]
                        self.guess_list.append(guess_mark)  # マークの履歴
                        # self.guess = self.convert() # マークから文字列へ変換
                        #self.hit = 1
                        # self.blow = 2 #正誤の判定
                        self.hit, self.blow = numberguess.judge_guess(
                            guess=self.num)  # 判定
                        self.hit_list.append(self.hit)
                        self.blow_list.append(self.blow)
                        if self.hit == 5:
                            self.gamescene = 4  # clear画面への遷移
                            pygame.mixer.music.stop()
                            pygame.mixer.music.load(self.bgm_dict["clear"])
                            pygame.mixer.music.set_volume(0.1)
                            pygame.mixer.music.play(loops=-1)
                            pygame.mixer.Channel(0).play(
                                pygame.mixer.Sound(self.se_dict["clear"]))
                        else:
                            self.hp -= self.damage_list[self.enemy_level-1]
                            pygame.mixer.Channel(0).play(
                                pygame.mixer.Sound(self.se_dict["attack"]))
                            for i in range(2):
                                self.screen.blit(
                                    self.enemy_damage_list[self.enemy_level], self.enemyrect)
                                pygame.display.update()
                                time.sleep(0.1)
                                self.screen.blit(
                                    self.enemy_list[self.enemy_level], self.enemyrect)
                                pygame.display.update()
                                time.sleep(0.1)
                        self.turn += 1
                        if self.hp <= 0:
                            self.gamescene = 3
                            pygame.mixer.music.stop()
                            pygame.mixer.music.load(self.bgm_dict["failed"])
                            pygame.mixer.music.set_volume(0.5)
                            pygame.mixer.music.play(loops=-1)
                            pygame.mixer.Channel(0).play(
                                pygame.mixer.Sound(self.se_dict["failed"]))
                if self.history_buttonrect.collidepoint(event.pos):
                    self.history_count = 1

    def mark_show(self):
        """入力画面の描画
        """
        for n in range(5):
            self.screen.blit(self.up_button_img, self.up_buttonrect[n])
            self.screen.blit(self.down_button_img, self.down_buttonrect[n])
            self.screen.blit(self.marks[self.num[n]], self.mark_buttonrect[n])

    def convert(self):
        """入力された予測をhit&blowの判定用の文字列に変換
        """
        num_convert = []
        for n in range(5):
            num_convert.append(str(self.num[n]))
            if num_convert[n] == "10":
                num_convert[n] = "a"
            if num_convert[n] == "11":
                num_convert[n] = "b"
            if num_convert[n] == "12":
                num_convert[n] = "c"
            if num_convert[n] == "13":
                num_convert[n] = "d"
            if num_convert[n] == "14":
                num_convert[n] = "e"
            if num_convert[n] == "15":
                num_convert[n] = "f"
        self.guess = num_convert[0]+num_convert[1] + \
            num_convert[2]+num_convert[3]+num_convert[4]

    def boss_stage(self):
        """ボスステージの描画
        """
        font2 = pygame.font.SysFont(None, 80)
        stage = font2.render("Boss Stage", True, (255, 255, 255))
        self.screen.blit(stage, (25, 30))
        self.screen.blit(self.return_button_img, self.return_buttonrect)

    def game_over(self):
        """ゲームオーバー画面の描画
        """
        font = pygame.font.SysFont(None, 80)
        game = font.render("Game", True, (150, 0, 0))
        over = font.render("Over", True, (150, 0, 0))
        self.screen.blit(game, (105, 200))
        self.screen.blit(over, (120, 250))
        self.screen.blit(self.return_button_img, self.return_buttonrect)
        self.screen.blit(self.history_button_img, Rect(120, 500, 120, 30))

    def clear(self, enemy_level: int = 0):
        """クリア画面の描画
        """
        font = pygame.font.SysFont(None, 80)
        font2 = pygame.font.SysFont(None, 40)
        clear = font.render("Clear!", True, (230, 180, 34))
        self.screen.blit(clear, (98, 100))
        exp = font2.render("EXP:{}".format(
            self.exp_list[enemy_level]), True, (255, 255, 255))
        self.screen.blit(exp, (130, 200))
        self.screen.blit(self.return_button_img, self.return_buttonrect)
        self.screen.blit(self.history_button_img, Rect(120, 500, 120, 30))

    def result_judge(self):
        """結果画面でのボタンの判定
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
                if self.return_buttonrect.collidepoint(event.pos):
                    self.gamescene = 0
                    pygame.mixer.music.stop()
                    time.sleep(0.5)
                    pygame.mixer.music.load(self.bgm_dict["home"])
                    pygame.mixer.music.set_volume(0.3)
                    pygame.mixer.music.play(loops=-1)
                if Rect(120, 500, 120, 30).collidepoint(event.pos):
                    self.history_count = 1

    def how_to_play(self):  # how to play 画面の描画
        self.screen.blit(self.how_to_play_img, Rect(0, 0, 360, 640))
        self.screen.blit(self.return_button_img, self.return_buttonrect)

    def how_to_play_judje(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
                if self.return_buttonrect.collidepoint(event.pos):
                    self.gamescene = 0

    def run(self):
        pygame.display.set_caption("Hit, Blow and Dragons")
        self.set_player()
        self.set_mark()
        self.set_enemy()
        self.set_button()
        self.set_mark_entry()
        self.set_sound()

        pygame.mixer.music.load(self.bgm_dict["home"])
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(loops=-1)
        while self.running:
            self.screen.fill((0, 0, 0))
            if self.error_count == 1:
                self.error_show()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
                        if self.return_buttonrect.collidepoint(event.pos):
                            self.error_count = 0
            elif self.history_count == 1:
                self.history_show()
                self.history_judge()
            elif self.history_count == 2:
                self.history2_show()
                self.history2_judge()
            elif self.history_count == 3:
                self.history2_show()
                self.history2_judge()
            elif self.history_count == 4:
                self.historylast_show()
                self.historylast_judge()
            elif self.gamescene == 0:  # ホーム画面
                self.reset()
                self.home_show()
                self.home_judge()
            elif self.gamescene == 5:  # how to play
                self.how_to_play()
                self.how_to_play_judje()
            elif self.enemy_level == 0:
                self.stage_select()
                self.judge_stage_select()

            elif self.gamescene == 1:  # Normal Stage
                self.normal_stage()
                self.normal_stage_judge()

            elif self.gamescene == 2:  # Boss Stage
                self.boss_stage()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
                        if self.return_buttonrect.collidepoint(event.pos):
                            self.gamescene = 0

            elif self.gamescene == 3:  # game over
                self.game_over()
                self.result_judge()

            elif self.gamescene == 4:
                self.clear()
                self.result_judge()

            pygame.display.update()  # スクリーン上のものを書き換えた時にはupdateが必要


def main():
    display = ShowGame()
    display.run()


main()
