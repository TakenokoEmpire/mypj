
import pygame
from pygame import Surface, mixer
from pygame.locals import *
from typing import List, Tuple
import time
import random
# from . import game_number_guess
import sys

from . import battle
from . import town


# mixer.Sound("--.mp3") #音の再生

"""TRUE"""

pygame.init()
mixer.init()
# numberguess = game_number_guess.NumberGuess()


class ShowGame(battle.Battle, town.Town):
    # stage_num　→　max_dungeon_num（変数名変更）：最大ダンジョン数
    # enemy_level　→　dungeon_num（変数名変更）：選択ダンジョン番号

    def __init__(self,
                 num: List[int] = [0, 1, 2, 3, 4],
                 turn: int = 1,
                 display_size: Tuple[int] = (360, 640),
                 dungeon_num: int = 0,
                 max_dungeon_num: int = 3,
                 gamescene: int = 0,
                 demand: int = 1,):
        print("showgame init")
        super().__init__()
        self.demand = demand
        self.num = num
        self.turn = turn
        self.boss_turn = turn
        self.screen = pygame.display.set_mode(display_size)
        self.dungeon_num = dungeon_num
        self.max_dungeon_num = max_dungeon_num
        self.gamescene = gamescene
        self.error_count = 0  # 同じ数字入れたときのエラーカウント
        self.history_count = 0  # 履歴画面関連
        self.guess_list = []  # 推測した数字
        self.boss_guess_list = []
        self.running = True
        self.hit = 0
        self.blow = 0
        self.boss_hit = 0
        self.boss_blow = 0
        self.ans_g = [0, 0, 0, 0, 0]
        self.flag = []
        self.lv_g = self.lv
        self.turn_switch = 0

    def second_init_showgame(self):
        # GUIに対応
        # 進入ダンジョンが決定する前(initで強制的に実行される内容)のself設定は最小限にしておき、
        # ダンジョンに依存するステータス等はここで決めていく

        self.max_hp = int(self.hp*3)
        self.damage = self.e_atk
        self.exp_g = self.exp
        self.hp_g = self.max_hp

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
            self.mark_buttonrect.append(Rect(10+n*70, 425, 60, 25))  # マークの位置

    def set_enemy(self):
        """敵の設定
        """
        # ダンジョン番号毎の敵画像
        # ダメージときに点滅させるために2種類用意
        # 【】敵画像の名称は、変数を用いたい
        # 【】点滅用敵画像を作るのがめんどくさいなら、他にいい方法ありそう
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
        Rect(ボタンの位置とサイズ)
        """
        self.normal_buttonrect = Rect(normal_button_place)
        self.boss_buttonrect = Rect(boss_button_place)
        self.how_to_play_buttonrect = Rect(how_to_play_button_place)
        self.return_buttonrect = Rect(return_button_place)
        self.prev_buttonrect = Rect(prev_button_place)
        self.next_buttonrect = Rect(next_button_place)
        self.history_buttonrect = Rect(history_button_place)
        self.stage_select_buttonrect = []
        for i in range(self.max_dungeon_num):
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
        hp→
        """
        self.turn = 1
        self.hit = 0
        self.blow = 0
        self.guess_list = []
        self.hit_list = []
        self.blow_list = []
        self.num = [0, 1, 2, 3, 4]
        self.dungeon_num = 0

    # ここまで初期設定

    def home_show(self):
        """ホーム画面の描画
        """
        self.screen.blit(self.img, self.player_place)  # imgの描画・updateされてるから
        self.font = pygame.font.SysFont(None, 40)  # フォントの指定
        lv_display = self.font.render("Lv {}".format(
            self.lv_g), True, (255, 255, 255))  # 文字・色の指定
        # screen.blit→指定された位置に画像を表示
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
                    self.make_1ans()    # 新しい答えの生成が必要
                    pygame.mixer.Channel(0).play(
                        pygame.mixer.Sound(self.se_dict["start"]))
                    time.sleep(2)
                if self.boss_buttonrect.collidepoint(event.pos):
                    self.gamescene = 2  # boss stageへ
                    self.make_1ans()  # 新しい答えの生成
                    pygame.mixer.Channel(0).play(
                        pygame.mixer.Sound(self.se_dict["start"]))
                    self.load_show()  # ロード画面
                    # bossが解く
                    time.sleep(2)

                    if self.how_to_play_buttonrect.collidepoint(event.pos):
                        self.gamescene = 5  # how to playへ

    # BOSS用ロード画面
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
        for i in range(self.max_dungeon_num):  # ステージの数だけ描画
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
                for i in range(self.max_dungeon_num):
                    if self.stage_select_buttonrect[i].collidepoint(event.pos):
                        self.dungeon_num = i+1
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

    def normal_stage(self, mode="normal"):
        """通常ステージの描画
        最大HP→self、残らない変数【残りHP＋累計ダメージで導出可】
        残りHP(「self.hp_g」)=毎ターン計算（ダメージを受けた値が保存される）
        累計ダメージ（「damage」）→敵攻撃力（リスト）＊ターン数
        【BEFORE】
        hitblow→self
        【AFTER】
        hitblow→引数

        """
        self.screen.blit(
            self.enemy_list[self.dungeon_num], self.enemyrect)  # 敵の描画
        font2 = pygame.font.SysFont(None, 30)  # turnの表示
        stage = font2.render("turn:{}".format(
            self.turn), True, (255, 255, 255))
        pygame.draw.line(self.screen, (0, 200, 0), (30, 40),
                         (30+self.hp_g, 40), 10)  # HPの表示
        font3 = pygame.font.SysFont(None, 20)
        hp_word = font3.render("HP", True, (255, 255, 255))
        hp_value = font3.render("{}".format(self.hp_g), True, (255, 255, 255))
        # if mode == "normal":
        #     damage_ratio = (self.turn-1)
        # elif mode == "boss":
        #     if self.boss_hit == 5:
        #         damage_ratio = 100
        #     else:
        #         damage_ratio = 0
        # damage = damage_ratio*self.damage

        damage = self.damage*(self.turn-1)
        if damage != 0:
            pygame.draw.line(self.screen, (200, 0, 0),
                             (30+self.hp_g, 40), (30+self.hp_g+damage, 40), 10)
        font4 = pygame.font.SysFont(None, 50)
        hit_blow = font4.render("Hit:{}   Blow:{}".format(
            self.hit, self.blow), True, (255, 255, 255))
        self.screen.blit(stage, (5, 5))
        self.screen.blit(hp_word, (5, 35))
        self.screen.blit(hp_value, (30+self.hp_g+damage+2, 35))
        self.screen.blit(hit_blow, (80, 360))
        self.screen.blit(self.enter_button_img, self.enter_buttonrect)
        self.screen.blit(self.history_button_img, self.history_buttonrect)
        self.mark_show()

    def boss_action(self, mode="normal"):
        if mode == "normal":
            return
        if self.jamming_judge("boss") == "stop":
            print("敵の調査を妨害した！")
            time.sleep(1)
        else:
            self.boss_guess_list = self.boss_history[self.boss_turn-1]["guess"]
            self.boss_hit = self.boss_history[self.boss_turn-1]["hit"]
            self.boss_blow = self.boss_history[self.boss_turn-1]["blow"]
            self.boss_turn += 1
            print([self.boss_guess_list, self.boss_hit, self.boss_blow])
            time.sleep(1)

    def normal_stage_judge(self, mode="normal"):
        """ノーマルステージでのボタンの判定
        【進数を16以外に設定できるようにしたい】
        同じ数字が含まれるとエラーカウント＋1
        【BEFORE】エラーカウント0で、Hitblow判定を行う
        【AFTER】エラーカウント0で、数字を戻り値として戻す
        Hit5でクリア画面
        Hit4以下ならダメージエフェクトとHP更新
        ターン数更新
        HP0で敗北画面
        Historyボタンが押されたらHistoryカウントを1に

        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 上の×ボタンで閉じる
                self.running = False
            # 上下ボタン関連
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
                    # 自分の攻撃プロセス
                    if self.error_count == 0:
                        guess_mark = [self.marks_s[self.num[0]], self.marks_s[self.num[1]],
                                      self.marks_s[self.num[2]], self.marks_s[self.num[3]], self.marks_s[self.num[4]]]
                        print(self.num)
                        self.guess_list.append(guess_mark)  # マークの履歴
                        # self.guess = self.convert() # マークから文字列へ変換
                        # self.hit = 1
                        # self.blow = 2 #正誤の判定
                        self.hit, self.blow = self.judge_guess(
                            guess=self.num)  # 判定
                        self.hit_list.append(self.hit)
                        self.blow_list.append(self.blow)
                        self.turn_switch += 1  # ボス用
                        self.boss_action(mode)  # ボス用
                        if self.hit == 5:
                            self.gamescene = 4  # clear画面への遷移
                            pygame.mixer.music.stop()
                            pygame.mixer.music.load(self.bgm_dict["clear"])
                            pygame.mixer.music.set_volume(0.1)
                            pygame.mixer.music.play(loops=-1)
                            pygame.mixer.Channel(0).play(
                                pygame.mixer.Sound(self.se_dict["clear"]))
                        elif mode == "normal":
                            self.hp_g -= self.damage
                            pygame.mixer.Channel(0).play(
                                pygame.mixer.Sound(self.se_dict["attack"]))
                            for i in range(2):
                                self.screen.blit(
                                    self.enemy_damage_list[self.dungeon_num], self.enemyrect)
                                pygame.display.update()
                                time.sleep(0.1)
                                self.screen.blit(
                                    self.enemy_list[self.dungeon_num], self.enemyrect)
                                pygame.display.update()
                                time.sleep(0.1)
                        elif mode == "boss":
                            if self.boss_hit == 3:
                                print("演出はここに入れる")
                            elif self.boss_hit == 5:
                                self.hp_g -= self.damage*100
                                self.hp_g -= self.damage
                                pygame.mixer.Channel(0).play(
                                    pygame.mixer.Sound(self.se_dict["attack"]))
                                for i in range(3):
                                    self.screen.blit(
                                        self.enemy_damage_list[self.dungeon_num], self.enemyrect)
                                    pygame.display.update()
                                    time.sleep(0.25)
                                    self.screen.blit(
                                        self.enemy_list[self.dungeon_num], self.enemyrect)
                                    pygame.display.update()
                                    time.sleep(0.25)
                        self.turn += 1
                        if self.hp_g <= 0:
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

    def clear(self, dungeon_num: int = 0):
        """クリア画面の描画
        """
        font = pygame.font.SysFont(None, 80)
        font2 = pygame.font.SysFont(None, 40)
        clear = font.render("Clear!", True, (230, 180, 34))
        self.screen.blit(clear, (98, 100))
        exp = font2.render("EXP:{}".format(
            self.e_exp), True, (255, 255, 255))
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

    def make_1ans(self):
        if self.demand == 1:
            self.ans_g = [0, 1, 2, 3, 5]
        else:
            nums = list(range(16))
            self.ans_g = random.sample(nums, 5)

    def judge_guess(self, guess: List[int]):
        h = 0
        b = 0
        for i in range(len(guess)):
            if guess[i] == self.ans_g[i]:
                h += 1  # hがヒットの数
            else:
                if guess[i] in self.ans_g:
                    b += 1  # bがブローの数
        print(self.ans_g)
        return h, b

    def choice_dict_initialize(self):
        self.choice_dict = {}
        for dict_name in self.dict_name_list:
            self.choice_dict.update(
                {dict_name: {"number": "False", "name": "False"}})

    def choice_screen(self, title, choice: List[str], message: List[str], dict_name, delete_dict_list_when_return: List[str] = []):
        """選択肢を表示させるためのモジュール
        タイトルは28文字まで、選択肢は7つまで、メッセージは5行まで対応。
        選択が行われた場合、選択肢の番号と名前を、self.choice_dictのdict_nameに登録する
        dict_name="装備"のとき、選択肢の番号はself.choice_dict["装備"]["number"]に、選択肢の名前をself.choice_dict["装備"]["name"]に登録する
        """
        self.choice_buttonrect = []
        choice_answer = False
        font = pygame.font.SysFont(
            "bizudminchomediumbizudpminchomediumtruetype", 24)
        font2 = pygame.font.SysFont(
            "bizudminchomediumbizudpminchomediumtruetype", 18)
        # titleを表示
        # titleが長すぎたら改行して2行にする
        title = str(title)
        if len(title) >= 14:
            title2 = title[14:len(title)]
            title = title[0:14]
        else:
            title2 = ""
        print_title = font.render(title, True, "WHITE")
        self.screen.blit(print_title, (11, 12))
        print_title2 = font.render(title2, True, "WHITE")
        self.screen.blit(print_title2, (11, 44))
        # 選択肢を表示
        for i in range(len(choice)):
            self.choice_buttonrect.append(Rect(30, 90+47*i, 260, 30))
        for i, name in enumerate(choice):  # 選択肢の数だけ描画
            print_choice = font.render(name, True, "WHITE")
            self.screen.blit(print_choice, (30, 93+47*i))
        self.screen.blit(self.return_button_img, self.return_buttonrect)
        # メッセージを表示
        for i, name in enumerate(message):
            print_message = font2.render(name, True, "WHITE")
            self.screen.blit(print_message, (11, 430+22*i))

        # 以下、本来は別関数（judge_～～～）となるはずだった部分
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
                for i in range(len(choice)):
                    if self.choice_buttonrect[i].collidepoint(event.pos):
                        pygame.mixer.Channel(0).play(
                            pygame.mixer.Sound(self.se_dict["start"]))
                        print("選択肢：{}".format(i))
                        self.choice_judge = 1
                        time.sleep(0.5)
                        self.choice_dict.update({dict_name: {"number": i,
                                                             "name": choice[i]}})
                        print(self.choice_dict)
                # Returnボタンが押されたときの動作
                if self.return_buttonrect.collidepoint(event.pos):
                    # 何も設定されてない場合はホーム画面まで戻る
                    if delete_dict_list_when_return == []:
                        delete_dict_list_when_return = self.dict_name_list
                    time.sleep(0.5)
                    for dicts in delete_dict_list_when_return:
                        self.choice_dict.update(
                            {dicts: {"number": "False", "name": "False"}})

    # def judge_choice_screen(self):
        """
        """

    # def run(self):
    #     pygame.display.set_caption("Hit, Blow and Dragons")
    #     self.set_player()
    #     self.set_mark()
    #     self.set_enemy()
    #     self.set_button()
    #     self.set_mark_entry()
    #     self.set_sound()

    #     pygame.mixer.music.load(self.bgm_dict["home"])
    #     pygame.mixer.music.set_volume(0.3)
    #     pygame.mixer.music.play(loops=-1)
    #     while self.running:
    #         self.screen.fill((0, 0, 0))
    #         if self.error_count == 1:
    #             self.error_show()
    #             for event in pygame.event.get():
    #                 if event.type == pygame.QUIT:
    #                     self.running = False
    #                 if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
    #                     if self.return_buttonrect.collidepoint(event.pos):
    #                         self.error_count = 0
    #         elif self.history_count == 1:
    #             self.history_show()
    #             self.history_judge()
    #         elif self.history_count == 2:
    #             self.history2_show()
    #             self.history2_judge()
    #         elif self.history_count == 3:
    #             self.history2_show()
    #             self.history2_judge()
    #         elif self.history_count == 4:
    #             self.historylast_show()
    #             self.historylast_judge()
    #         elif self.gamescene == 0:  # ホーム画面
    #             self.reset()
    #             self.home_show()
    #             self.home_judge()
    #         elif self.gamescene == 5:  # how to play
    #             self.how_to_play()
    #             self.how_to_play_judje()
    #         elif self.dungeon_num == 0:
    #             self.stage_select()
    #             self.judge_stage_select()

    #         elif self.gamescene == 1:  # Normal Stage
    #             self.normal_stage()
    #             self.normal_stage_judge()

    #         elif self.gamescene == 2:  # Boss Stage
    #             self.boss_stage()
    #             for event in pygame.event.get():
    #                 if event.type == pygame.QUIT:
    #                     self.running = False
    #                 if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
    #                     if self.return_buttonrect.collidepoint(event.pos):
    #                         self.gamescene = 0

    #         elif self.gamescene == 3:  # game over
    #             self.game_over()
    #             self.result_judge()

    #         elif self.gamescene == 4:
    #             self.clear()
    #             self.result_judge()

    #         pygame.display.update()  # スクリーン上のものを書き換えた時にはupdateが必要


# def main():
#     display = ShowGame()
#     display.run()


# main()
