
import pygame
from pygame import Surface, mixer
from pygame.locals import *
from typing import List, Tuple
import math
import time
import random
import unicodedata
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
                 #  turn: int = 1,
                 display_size: Tuple[int] = (360, 640),
                 dungeon_num: int = 0,
                 max_dungeon_num: int = 3,
                 gamescene: int = 0,
                 demand: List[int] = [1, 1, 1]):
        print("showgame init")
        super().__init__()
        self.demand = demand
        self.num = num
        if self.demand[1] != 1:
            self.screen = pygame.display.set_mode(
                display_size, HWSURFACE | FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((360, 640))
        self.dungeon_num = dungeon_num
        self.max_dungeon_num = max_dungeon_num
        self.gamescene = gamescene
        self.error_count = 0  # 同じ数字入れたときのエラーカウント
        self.history_count = 0  # 履歴画面関連
        self.item_screen_count = 0
        # self.guess_list = []  # 推測した数字
        # self.boss_guess_list = []
        self.running = True
        # self.hit = 0
        # self.blow = 0
        # self.boss_hit = 0
        # self.boss_blow = 0
        self.ans_g = [0, 0, 0, 0, 0]
        self.flag = []
        self.turn_switch = 0
        # self.lv = self.lv
        self.screen_size = 1
        self.screen_count = 0
        self.width = display_size[0]
        self.height = display_size[1]
        self.message = ""
        self.message_checker = 0
        self.clock = pygame.time.Clock()
        self.FPS = 72
        self.ball_img = pygame.image.load("./new_system/mypj3/img/ball.png")
        self.ball_img = pygame.transform.rotozoom(self.ball_img, 0, self.screen_size)
        self.enemy_stop = 0

    def second_init_showgame(self):
        # GUIに対応
        # 進入ダンジョンが決定する前(initで強制的に実行される内容)のself設定は最小限にしておき、
        # ダンジョンに依存するステータス等はここで決めていく

        # ステータス更新した？
        self.turn = 1
        self.boss_turn = 1
        self.hit = 0
        self.blow = 0
        self.boss_hit = 0
        self.boss_blow = 0
        self.guess_list = []  # 推測した数字
        self.boss_guess_list = []
        self.max_hp = self.hp
        self.damage = self.e_atk
        self.exp_g = self.exp
        self.hp_g = self.max_hp
        # hpバーを表示する大きさ
        # 100まではリニアに、1000までは緩やかに、長さが増加し、1000以上で固定（300ピクセル）
        if self.hp_g <= 100:
            self.hp_bar_ratio = 1.5
        elif self.hp_g <= 1000:
            self.hp_bar_ratio = 150/self.hp_g * \
                (self.hp_g/100)**(math.log(2)/math.log(1000/100))
        else:
            self.hp_bar_ratio = 300 / self.hp_g
        # print(self.hp_bar_ratio)
        self.attr_mark_qty = [4,4,4,4]
        self.mark_qty_all = 16
        self.attr_judge_battle()
        self.attr_mark_dict = {}
        self.make_attr_mark_dict()
        self.digit_16_to_less()

    def make_attr_mark_dict(self):
        # ax = [3,4,4,4]
        attr_mark_dict = {}
        key_count = 0
        for attr_index,qty in enumerate(self.attr_mark_qty):
            # print(qty)
            for shape_index in range(qty):
                self.attr_mark_dict[key_count] = attr_index*4+shape_index
                key_count += 1
        print(self.attr_mark_dict)

    def attr_judge_battle(self):
        """現状、各属性の数は3~4の間でしか動かないようになってる"""
        enemy_attr_resist = [self.e_lv*3,self.e_lv*3,self.e_lv*3,self.e_lv*3]
        for attr in range(4):
            attr_mergin = (self.attr_power[attr] - enemy_attr_resist[attr])/100 * (1+self.demand[4])
            attr_mergin_fraction = attr_mergin - int(attr_mergin)
            if self.rand_judge(attr_mergin_fraction) == True:
                self.attr_mark_qty[attr] = min(max(3 - int(attr_mergin),2),4)
            else:
                self.attr_mark_qty[attr] = min(max(4 - int(attr_mergin),2),4)
        if int(self.demand[3]) != 0:
            self.attr_mark_qty = [4,4,4-self.demand[3],4]
        self.mark_qty_all = sum(self.attr_mark_qty)


    def set_player(self, X: int = 118, Y: int = 50):
        """ホーム画面の立ち絵の設定
        """
        self.img = pygame.image.load("./new_system/mypj3/img/player.png")
        self.img = pygame.transform.rotozoom(self.img, 0, self.screen_size)
        self.player_place = (X*self.screen_size, Y*self.screen_size)

    def set_mark(self):
        """入力用マークの設定
        """
        self.b_moon_img = pygame.image.load("./new_system/mypj3/img/b_moon.png")
        self.b_moon_img = pygame.transform.rotozoom(
            self.b_moon_img, 0, self.screen_size)
        self.b_snow_img = pygame.image.load("./new_system/mypj3/img/b_snow.png")
        self.b_snow_img = pygame.transform.rotozoom(
            self.b_snow_img, 0, self.screen_size)
        self.b_star_img = pygame.image.load("./new_system/mypj3/img/b_star.png")
        self.b_star_img = pygame.transform.rotozoom(
            self.b_star_img, 0, self.screen_size)
        self.b_sun_img = pygame.image.load("./new_system/mypj3/img/b_sun.png")
        self.b_sun_img = pygame.transform.rotozoom(
            self.b_sun_img, 0, self.screen_size)
        self.g_moon_img = pygame.image.load("./new_system/mypj3/img/g_moon.png")
        self.g_moon_img = pygame.transform.rotozoom(
            self.g_moon_img, 0, self.screen_size)
        self.g_snow_img = pygame.image.load("./new_system/mypj3/img/g_snow.png")
        self.g_snow_img = pygame.transform.rotozoom(
            self.g_snow_img, 0, self.screen_size)
        self.g_star_img = pygame.image.load("./new_system/mypj3/img/g_star.png")
        self.g_star_img = pygame.transform.rotozoom(
            self.g_star_img, 0, self.screen_size)
        self.g_sun_img = pygame.image.load("./new_system/mypj3/img/g_sun.png")
        self.g_sun_img = pygame.transform.rotozoom(
            self.g_sun_img, 0, self.screen_size)
        self.p_moon_img = pygame.image.load("./new_system/mypj3/img/p_moon.png")
        self.p_moon_img = pygame.transform.rotozoom(
            self.p_moon_img, 0, self.screen_size)
        self.p_snow_img = pygame.image.load("./new_system/mypj3/img/p_snow.png")
        self.p_snow_img = pygame.transform.rotozoom(
            self.p_snow_img, 0, self.screen_size)
        self.p_star_img = pygame.image.load("./new_system/mypj3/img/p_star.png")
        self.p_star_img = pygame.transform.rotozoom(
            self.p_star_img, 0, self.screen_size)
        self.p_sun_img = pygame.image.load("./new_system/mypj3/img/p_sun.png")
        self.p_sun_img = pygame.transform.rotozoom(
            self.p_sun_img, 0, self.screen_size)
        self.y_moon_img = pygame.image.load("./new_system/mypj3/img/y_moon.png")
        self.y_moon_img = pygame.transform.rotozoom(
            self.y_moon_img, 0, self.screen_size)
        self.y_snow_img = pygame.image.load("./new_system/mypj3/img/y_snow.png")
        self.y_snow_img = pygame.transform.rotozoom(
            self.y_snow_img, 0, self.screen_size)
        self.y_star_img = pygame.image.load("./new_system/mypj3/img/y_star.png")
        self.y_star_img = pygame.transform.rotozoom(
            self.y_star_img, 0, self.screen_size)
        self.y_sun_img = pygame.image.load("./new_system/mypj3/img/y_sun.png")
        self.y_sun_img = pygame.transform.rotozoom(
            self.y_sun_img, 0, self.screen_size)

        self.b_moon_s_img = pygame.image.load("./new_system/mypj3/img/b_moon_s.png")
        self.b_moon_s_img = pygame.transform.rotozoom(
            self.b_moon_s_img, 0, self.screen_size)
        self.b_snow_s_img = pygame.image.load("./new_system/mypj3/img/b_snow_s.png")
        self.b_snow_s_img = pygame.transform.rotozoom(
            self.b_snow_s_img, 0, self.screen_size)
        self.b_star_s_img = pygame.image.load("./new_system/mypj3/img/b_star_s.png")
        self.b_star_s_img = pygame.transform.rotozoom(
            self.b_star_s_img, 0, self.screen_size)
        self.b_sun_s_img = pygame.image.load("./new_system/mypj3/img/b_sun_s.png")
        self.b_sun_s_img = pygame.transform.rotozoom(
            self.b_sun_s_img, 0, self.screen_size)
        self.g_moon_s_img = pygame.image.load("./new_system/mypj3/img/g_moon_s.png")
        self.g_moon_s_img = pygame.transform.rotozoom(
            self.g_moon_s_img, 0, self.screen_size)
        self.g_snow_s_img = pygame.image.load("./new_system/mypj3/img/g_snow_s.png")
        self.g_snow_s_img = pygame.transform.rotozoom(
            self.g_snow_s_img, 0, self.screen_size)
        self.g_star_s_img = pygame.image.load("./new_system/mypj3/img/g_star_s.png")
        self.g_star_s_img = pygame.transform.rotozoom(
            self.g_star_s_img, 0, self.screen_size)
        self.g_sun_s_img = pygame.image.load("./new_system/mypj3/img/g_sun_s.png")
        self.g_sun_s_img = pygame.transform.rotozoom(
            self.g_sun_s_img, 0, self.screen_size)
        self.p_moon_s_img = pygame.image.load("./new_system/mypj3/img/p_moon_s.png")
        self.p_moon_s_img = pygame.transform.rotozoom(
            self.p_moon_s_img, 0, self.screen_size)
        self.p_snow_s_img = pygame.image.load("./new_system/mypj3/img/p_snow_s.png")
        self.p_snow_s_img = pygame.transform.rotozoom(
            self.p_snow_s_img, 0, self.screen_size)
        self.p_star_s_img = pygame.image.load("./new_system/mypj3/img/p_star_s.png")
        self.p_star_s_img = pygame.transform.rotozoom(
            self.p_star_s_img, 0, self.screen_size)
        self.p_sun_s_img = pygame.image.load("./new_system/mypj3/img/p_sun_s.png")
        self.p_sun_s_img = pygame.transform.rotozoom(
            self.p_sun_s_img, 0, self.screen_size)
        self.y_moon_s_img = pygame.image.load("./new_system/mypj3/img/y_moon_s.png")
        self.y_moon_s_img = pygame.transform.rotozoom(
            self.y_moon_s_img, 0, self.screen_size)
        self.y_snow_s_img = pygame.image.load("./new_system/mypj3/img/y_snow_s.png")
        self.y_snow_s_img = pygame.transform.rotozoom(
            self.y_snow_s_img, 0, self.screen_size)
        self.y_star_s_img = pygame.image.load("./new_system/mypj3/img/y_star_s.png")
        self.y_star_s_img = pygame.transform.rotozoom(
            self.y_star_s_img, 0, self.screen_size)
        self.y_sun_s_img = pygame.image.load("./new_system/mypj3/img/y_sun_s.png")
        self.y_sun_s_img = pygame.transform.rotozoom(
            self.y_sun_s_img, 0, self.screen_size)

        self.marks_16 = {0: self.b_moon_img, 1: self.b_snow_img, 2: self.b_star_img, 3: self.b_sun_img,
                      4: self.g_moon_img, 5: self.g_snow_img, 6: self.g_star_img, 7: self.g_sun_img,
                      8: self.p_moon_img, 9: self.p_snow_img, 10: self.p_star_img, 11: self.p_sun_img,
                      12: self.y_moon_img, 13: self.y_snow_img, 14: self.y_star_img, 15: self.y_sun_img
                      }
        self.marks_s_16 = {0: self.b_moon_s_img, 1: self.b_snow_s_img, 2: self.b_star_s_img, 3: self.b_sun_s_img,
                        4: self.g_moon_s_img, 5: self.g_snow_s_img, 6: self.g_star_s_img, 7: self.g_sun_s_img,
                        8: self.p_moon_s_img, 9: self.p_snow_s_img, 10: self.p_star_s_img, 11: self.p_sun_s_img,
                        12: self.y_moon_s_img, 13: self.y_snow_s_img, 14: self.y_star_s_img, 15: self.y_sun_s_img
                        }

        self.mark_buttonrect = []
        for n in range(5):
            self.mark_buttonrect.append(Rect(
                (10+n*70)*self.screen_size, 425*self.screen_size, 60*self.screen_size, 25*self.screen_size))

    def digit_16_to_less(self):
        self.marks = {}
        self.marks_s = {}
        for i in range(self.mark_qty_all):
            self.marks[i] = self.marks_16[self.attr_mark_dict[i]]
            self.marks_s[i] = self.marks_s_16[self.attr_mark_dict[i]]

    def set_enemy(self):
        """敵の設定
        """
        # ダンジョン番号毎の敵画像
        # ダメージときに点滅させるために2種類用意
        # 【】敵画像の名称は、変数を用いたい
        # 【】点滅用敵画像を作るのがめんどくさいなら、他にいい方法ありそう
        self.enemy1_img = pygame.image.load("./new_system/mypj3/img/enemy1.png")
        self.enemy1_img = pygame.transform.rotozoom(
            self.enemy1_img, 0, self.screen_size)
        self.enemy1_damage_img = pygame.image.load(
            "./new_system/mypj3/img/enemy1_damage.png")
        self.enemy1_damage_img = pygame.transform.rotozoom(
            self.enemy1_damage_img, 0, self.screen_size)
        self.enemy2_img = pygame.image.load("./new_system/mypj3/img/enemy2.png")
        self.enemy2_img = pygame.transform.rotozoom(
            self.enemy2_img, 0, self.screen_size)
        self.enemy2_damage_img = pygame.image.load(
            "./new_system/mypj3/img/enemy2_damage.png")
        self.enemy2_damage_img = pygame.transform.rotozoom(
            self.enemy2_damage_img, 0, self.screen_size)
        self.enemy3_img = pygame.image.load("./new_system/mypj3/img/enemy3.png")
        self.enemy3_img = pygame.transform.rotozoom(
            self.enemy3_img, 0, self.screen_size)
        self.enemy3_damage_img = pygame.image.load(
            "./mypj3/img/enemy3_damage.png")
        self.enemy3_damage_img = pygame.transform.rotozoom(
            self.enemy3_damage_img, 0, self.screen_size)
        self.enemy_list = {1: self.enemy1_img,
                           2: self.enemy2_img, 3: self.enemy3_img}
        self.enemy_damage_list = {1: self.enemy1_damage_img,
                                  2: self.enemy2_damage_img, 3: self.enemy3_damage_img}
        self.enemyrect = Rect(93*self.screen_size, 60*self.screen_size,
                              187*self.screen_size, 250*self.screen_size)

    def set_button(self):
        """ボタンの設定
        Rect(ボタンの位置とサイズ)
        """
        self.normal_buttonrect = Rect(
            80*self.screen_size, 300*self.screen_size, 200*self.screen_size, 50*self.screen_size)
        self.boss_buttonrect = Rect(
            80*self.screen_size, 375*self.screen_size, 200*self.screen_size, 50*self.screen_size)
        self.how_to_play_buttonrect = Rect(
            80*self.screen_size, 500*self.screen_size, 200*self.screen_size, 50*self.screen_size)
        self.return_buttonrect = Rect(
            80*self.screen_size, 575*self.screen_size, 200*self.screen_size, 50*self.screen_size)
        self.left_buttonrect = Rect(
            10*self.screen_size, 570*self.screen_size, 60*self.screen_size, 60*self.screen_size)
        self.right_buttonrect = Rect(
            290*self.screen_size, 570*self.screen_size, 60*self.screen_size, 60*self.screen_size)
        self.prev_buttonrect = Rect(
            50*self.screen_size, 500*self.screen_size, 120*self.screen_size, 30*self.screen_size)
        self.next_buttonrect = Rect(
            190*self.screen_size, 500*self.screen_size, 120*self.screen_size, 30*self.screen_size)
        self.history_buttonrect = Rect(
            120*self.screen_size, 580*self.screen_size, 120*self.screen_size, 30*self.screen_size)
        self.stage_select_buttonrect = []
        for i in range(self.max_dungeon_num):
            self.stage_select_buttonrect.append(Rect(
                80*self.screen_size, (100+100*i)*self.screen_size, 200*self.screen_size, 50*self.screen_size))
        self.normal_button_img = pygame.image.load(
            "./new_system/mypj3/img/normal_button.png")
        self.normal_button_img = pygame.transform.rotozoom(
            self.normal_button_img, 0, self.screen_size)
        self.boss_button_img = pygame.image.load("./new_system/mypj3/img/boss_button.png")
        self.boss_button_img = pygame.transform.rotozoom(
            self.boss_button_img, 0, self.screen_size)
        self.how_to_play_button_img = pygame.image.load(
            "./new_system/mypj3/img/how_to_button.png")
        self.how_to_play_button_img = pygame.transform.rotozoom(
            self.how_to_play_button_img, 0, self.screen_size)
        self.return_button_img = pygame.image.load("./new_system/mypj3/img/return.png")
        self.return_button_img = pygame.transform.rotozoom(
            self.return_button_img, 0, self.screen_size)
        self.prev_button_img = pygame.image.load("./new_system/mypj3/img/prev.png")
        self.prev_button_img = pygame.transform.rotozoom(
            self.prev_button_img, 0, self.screen_size)
        self.next_button_img = pygame.image.load("./new_system/mypj3/img/next.png")
        self.next_button_img = pygame.transform.rotozoom(
            self.next_button_img, 0, self.screen_size)
        self.history_button_img = pygame.image.load(
            "./new_system/mypj3/img/history_button.png")
        self.history_button_img = pygame.transform.rotozoom(
            self.history_button_img, 0, self.screen_size)
        self.how_to_play_img = pygame.image.load("./new_system/mypj3/img/how_to_play.png")
        self.how_to_play_img = pygame.transform.rotozoom(
            self.how_to_play_img, 0, self.screen_size)
        self.left_img = pygame.image.load("./new_system/mypj3/img/left.png")
        self.left_img = pygame.transform.rotozoom(
            self.left_img, 0, self.screen_size)
        self.right_img = pygame.image.load("./new_system/mypj3/img/right.png")
        self.right_img = pygame.transform.rotozoom(
            self.right_img, 0, self.screen_size)

    def set_mark_entry(self):
        """マーク入力用の設定
        """
        self.up_button_img = pygame.image.load("./new_system/mypj3/img/up.png")
        self.up_button_img = pygame.transform.rotozoom(
            self.up_button_img, 0, self.screen_size)
        self.down_button_img = pygame.image.load("./new_system/mypj3/img/down.png")
        self.down_button_img = pygame.transform.rotozoom(
            self.down_button_img, 0, self.screen_size)
        self.up_buttonrect = []
        for n in range(5):
            self.up_buttonrect.append(Rect(
                (10+n*70)*self.screen_size, 400*self.screen_size, 60*self.screen_size, 25*self.screen_size))
        self.down_buttonrect = []
        for n in range(5):
            self.down_buttonrect.append(Rect(
                (10+n*70)*self.screen_size, 485*self.screen_size, 60*self.screen_size, 25*self.screen_size))
        self.enter_button_img = pygame.image.load("./new_system/mypj3/img/enter.png")
        self.enter_button_img = pygame.transform.rotozoom(
            self.enter_button_img, 0, self.screen_size)
        self.enter_buttonrect = Rect(
            120*self.screen_size, 520*self.screen_size, 120*self.screen_size, 32*self.screen_size)

    def set_sound(self):
        self.bgm_dict = {"normal": "./new_system/mypj3/sound/normal_BGM.mp3",
                         "boss": "./new_system/mypj3/sound/boss.mp3",
                         "home": "./new_system/mypj3/sound/home.mp3",
                         "clear": "./new_system/mypj3/sound/clear_bgm.mp3",
                         "failed": "./new_system/mypj3/sound/failed_bgm.mp3"}
        self.se_dict = {"attack": "./new_system/mypj3/sound/attacked.mp3",
                        "start": "./new_system/mypj3/sound/start.mp3",
                        "clear": "./new_system/mypj3/sound/clear_se.mp3",
                        "failed": "./new_system/mypj3/sound/failed_se.mp3"}

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
        self.font = pygame.font.SysFont(None, 40*self.screen_size)  # フォントの指定
        lv_display = self.font.render("Lv {}".format(
            self.lv), True, (255, 255, 255))  # 文字・色の指定
        self.screen.blit(lv_display, (150*self.screen_size,
                         220*self.screen_size))  # テキストの位置
        self.screen.blit(self.normal_button_img, self.normal_buttonrect)
        self.screen.blit(self.boss_button_img, self.boss_buttonrect)
        self.screen.blit(self.how_to_play_button_img,
                         self.how_to_play_buttonrect)
        self.screen.blit(self.return_button_img, self.return_buttonrect)

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
                    time.sleep(1)
                if self.boss_buttonrect.collidepoint(event.pos):
                    self.gamescene = 2  # boss stageへ
                    self.make_1ans()  # 新しい答えの生成
                    pygame.mixer.Channel(0).play(
                        pygame.mixer.Sound(self.se_dict["start"]))
                    self.load_show()  # ロード画面
                    # bossが解く
                    time.sleep(1)

                if self.how_to_play_buttonrect.collidepoint(event.pos):
                    self.gamescene = 5  # how to playへ
                if self.return_buttonrect.collidepoint(event.pos):
                    self.gamescene = 0
                    self.choice_dict["初期画面"] = {
                        "number": "False", "name": "False"}

    # BOSS用ロード画面
    def load_show(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 40*self.screen_size)
        load_message = font.render("Now Loading...", True, (255, 255, 255))
        self.screen.blit(
            load_message, (150*self.screen_size, 450*self.screen_size))
        pygame.display.update()

    def error_show(self):
        """エラー画面の描画
        """
        self.font4 = pygame.font.SysFont(None, 33*self.screen_size)
        error_message = self.font4.render(
            "! Cannot enter the same mark !", True, (255, 0, 0))
        self.screen.blit(
            error_message, (18*self.screen_size, 300*self.screen_size))
        self.screen.blit(self.return_button_img, self.return_buttonrect)

    def history_show(self):
        """履歴の描画1ページ目
        """
        font = pygame.font.SysFont(None, 30*self.screen_size)
        if self.turn > 10:
            for i in range(10):
                for j in range(5):
                    self.screen.blit(self.guess_list[i][j], ((
                        30+j*40)*self.screen_size, (55+i*40)*self.screen_size, 30*self.screen_size, 30*self.screen_size))
                turn = font.render("{}".format(i+1), True, (255, 255, 255))
                self.screen.blit(
                    turn, (3*self.screen_size, (60+i*40)*self.screen_size))
                pygame.draw.line(self.screen, (100, 100, 100), (25*self.screen_size, (50+i*40)
                                 * self.screen_size), (25*self.screen_size, (90+i*40)*self.screen_size), 1)
                pygame.draw.line(self.screen, (100, 100, 100), (0, (90+i*40)*self.screen_size),
                                 (360*self.screen_size, (90+i*40)*self.screen_size), 1)
                hit_blow = font.render("Hit:{} Blow:{}".format(
                    self.hit_list[i], self.blow_list[i]), True, (255, 255, 255))
                self.screen.blit(
                    hit_blow, (230*self.screen_size, (60+i*40)*self.screen_size))

        else:
            for i in range(self.turn-1):
                for j in range(5):
                    self.screen.blit(self.guess_list[i][j], ((
                        30+j*40)*self.screen_size, (55+i*40)*self.screen_size, 30*self.screen_size, 30*self.screen_size))
                turn = font.render("{}".format(i+1), True, (255, 255, 255))
                self.screen.blit(
                    turn, (3*self.screen_size, (60+i*40)*self.screen_size))
                pygame.draw.line(self.screen, (100, 100, 100), (25*self.screen_size, (50+i*40)
                                 * self.screen_size), (25*self.screen_size, (90+i*40)*self.screen_size), 1)
                pygame.draw.line(self.screen, (100, 100, 100), (0, (90+i*40)*self.screen_size),
                                 (360*self.screen_size, (90+i*40)*self.screen_size), 1)
                hit_blow = font.render("Hit:{} Blow:{}".format(
                    self.hit_list[i], self.blow_list[i]), True, (255, 255, 255))
                self.screen.blit(
                    hit_blow, (230*self.screen_size, (60+i*40)*self.screen_size))
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
        font = pygame.font.SysFont(None, 30*self.screen_size)
        if self.turn > self.history_count*10:
            for i in range((self.history_count-1)*10, self.history_count*10):
                for j in range(5):
                    self.screen.blit(self.guess_list[i][j], ((30+j*40)*self.screen_size, (55+(
                        i-(self.history_count-1)*10)*40)*self.screen_size, 30*self.screen_size, 30*self.screen_size))
                turn = font.render("{}".format(i+1), True, (255, 255, 255))
                self.screen.blit(
                    turn, (3*self.screen_size, (60+(i-(self.history_count-1)*10)*40)*self.screen_size))
                pygame.draw.line(self.screen, (100, 100, 100), (25*self.screen_size, (50+(i-(self.history_count-1)*10)*40)
                                 * self.screen_size), (25*self.screen_size, (90+(i-(self.history_count-1)*10)*40)*self.screen_size), 1)
                pygame.draw.line(self.screen, (100, 100, 100), (0, (90+(i-(self.history_count-1)*10)*40)*self.screen_size),
                                 (360*self.screen_size, (90+(i-(self.history_count-1)*10)*40)*self.screen_size), 1)
                hit_blow = font.render("Hit:{} Blow:{}".format(
                    self.hit_list[i], self.blow_list[i]), True, (255, 255, 255))
                self.screen.blit(hit_blow, (230*self.screen_size,
                                 (60+(i-(self.history_count-1)*10)*40)*self.screen_size))

        else:
            for i in range((self.history_count-1)*10, self.turn-1):
                for j in range(5):
                    self.screen.blit(self.guess_list[i][j], ((30+j*40)*self.screen_size, (55+(
                        i-(self.history_count-1)*10)*40)*self.screen_size, 30*self.screen_size, 30*self.screen_size))
                turn = font.render("{}".format(i+1), True, (255, 255, 255))
                self.screen.blit(
                    turn, (3*self.screen_size, (60+(i-(self.history_count-1)*10)*40)*self.screen_size))
                pygame.draw.line(self.screen, (100, 100, 100), (25*self.screen_size, (50+(i-(self.history_count-1)*10)*40)
                                 * self.screen_size), (25*self.screen_size, (90+(i-(self.history_count-1)*10)*40)*self.screen_size), 1)
                pygame.draw.line(self.screen, (100, 100, 100), (0, (90+(i-(self.history_count-1)*10)*40)*self.screen_size),
                                 (360*self.screen_size, (90+(i-(self.history_count-1)*10)*40)*self.screen_size), 1)
                hit_blow = font.render("Hit:{} Blow:{}".format(
                    self.hit_list[i], self.blow_list[i]), True, (255, 255, 255))
                self.screen.blit(hit_blow, (230*self.screen_size,
                                 (60+(i-(self.history_count-1)*10)*40)*self.screen_size))
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
        font = pygame.font.SysFont(None, 30*self.screen_size)
        for i in range((self.history_count-1)*10, self.turn-1):
            for j in range(5):
                self.screen.blit(self.guess_list[i][j], ((30+j*40)*self.screen_size, (55+(
                    i-(self.history_count-1)*10)*40)*self.screen_size, 30*self.screen_size, 30*self.screen_size))
            turn = font.render("{}".format(i+1), True, (255, 255, 255))
            self.screen.blit(
                turn, (3*self.screen_size, (60+(i-(self.history_count-1)*10)*40)*self.screen_size))
            pygame.draw.line(self.screen, (100, 100, 100), (25*self.screen_size, (50+(i-(self.history_count-1)*10)*40)
                             * self.screen_size), (25*self.screen_size, (90+(i-(self.history_count-1)*10)*40)*self.screen_size), 1)
            pygame.draw.line(self.screen, (100, 100, 100), (0, (90+(i-(self.history_count-1)*10)*40)*self.screen_size),
                             (360*self.screen_size, (90+(i-(self.history_count-1)*10)*40)*self.screen_size), 1)
            hit_blow = font.render("Hit:{} Blow:{}".format(
                self.hit_list[i], self.blow_list[i]), True, (255, 255, 255))
            self.screen.blit(hit_blow, (230*self.screen_size,
                             (60+(i-(self.history_count-1)*10)*40)*self.screen_size))
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
        font = pygame.font.Font("./new_system/Harenosora.otf", 30*self.screen_size)
        level = font.render("ステージを選んで下さい", True, "WHITE")
        self.screen.blit(level, (11*self.screen_size, 10*self.screen_size))
        font2 = pygame.font.Font("./new_system/ALGERIA.TTF", 40*self.screen_size)
        for i in range(self.max_dungeon_num):  # ステージの数だけ描画
            level = font2.render("LEVEL:{}".format(i+1), True, "WHITE")
            self.screen.blit(level, (100*self.screen_size,
                             (100+100*i)*self.screen_size))
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
                        time.sleep(1)
                        # 音楽関連
                        # loops:繰り返す回数　loops+1回流れる、-1で無限ループ
                        # load+playでセット
                        # mixerで音楽をミックスできる（主にSEのとき）
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
        font2 = pygame.font.SysFont(None, 30*self.screen_size)  # turnの表示
        stage = font2.render("turn:{}".format(
            self.turn), True, (255, 255, 255))
        pygame.draw.line(self.screen, (0, 200, 0), (30*self.screen_size, 40*self.screen_size),
                        (30*self.screen_size+self.hp_g*self.hp_bar_ratio*self.screen_size, 40*self.screen_size), 10*self.screen_size)  # HPの表示
        font3 = pygame.font.SysFont(None, 20*self.screen_size)
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

        damage = self.hp - self.hp_g
        if damage != 0:
            pygame.draw.line(self.screen, (200, 0, 0),
                             (30*self.screen_size+self.hp_g*self.hp_bar_ratio*self.screen_size, 40*self.screen_size), (30*self.screen_size+(self.hp_g+damage)*self.hp_bar_ratio*self.screen_size, 40*self.screen_size), 10*self.screen_size)
        font4 = pygame.font.SysFont(None, 50*self.screen_size)
        hit_blow = font4.render("Hit:{}   Blow:{}".format(
            self.hit, self.blow), True, (255, 255, 255))
        self.screen.blit(stage, (5*self.screen_size, 5*self.screen_size))
        self.screen.blit(hp_word, (5*self.screen_size, 35*self.screen_size))
        self.screen.blit(
            hp_value, (30*self.screen_size+(self.hp_g+damage)*self.hp_bar_ratio*self.screen_size+2*self.screen_size, 35*self.screen_size))
        self.screen.blit(hit_blow, (80*self.screen_size, 360*self.screen_size))
        self.screen.blit(self.enter_button_img, self.enter_buttonrect)
        self.screen.blit(self.history_button_img, self.history_buttonrect)
        font = pygame.font.Font("./new_system/ALGERIA.TTF", 40*self.screen_size)
        item_comand = font.render("ITEMS", True, (255,255,255))
        self.screen.blit(item_comand,(130*self.screen_size, 310*self.screen_size))
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
                    if self.num[0] == self.mark_qty_all:
                        self.num[0] = 0
                if self.down_buttonrect[0].collidepoint(event.pos):
                    self.num[0] -= 1
                    if self.num[0] == -1:
                        self.num[0] = self.mark_qty_all-1
                if self.up_buttonrect[1].collidepoint(event.pos):
                    self.num[1] += 1
                    if self.num[1] == self.mark_qty_all:
                        self.num[1] = 0
                if self.down_buttonrect[1].collidepoint(event.pos):
                    self.num[1] -= 1
                    if self.num[1] == -1:
                        self.num[1] = self.mark_qty_all-1
                if self.up_buttonrect[2].collidepoint(event.pos):
                    self.num[2] += 1
                    if self.num[2] == self.mark_qty_all:
                        self.num[2] = 0
                if self.down_buttonrect[2].collidepoint(event.pos):
                    self.num[2] -= 1
                    if self.num[2] == -1:
                        self.num[2] = self.mark_qty_all-1
                if self.up_buttonrect[3].collidepoint(event.pos):
                    self.num[3] += 1
                    if self.num[3] == self.mark_qty_all:
                        self.num[3] = 0
                if self.down_buttonrect[3].collidepoint(event.pos):
                    self.num[3] -= 1
                    if self.num[3] == -1:
                        self.num[3] = self.mark_qty_all-1
                if self.up_buttonrect[4].collidepoint(event.pos):
                    self.num[4] += 1
                    if self.num[4] == self.mark_qty_all:
                        self.num[4] = 0
                if self.down_buttonrect[4].collidepoint(event.pos):
                    self.num[4] -= 1
                    if self.num[4] == -1:
                        self.num[4] = self.mark_qty_all-1
                if self.enter_buttonrect.collidepoint(event.pos):
                    for i in self.num:
                        if self.num.count(i) > 1:
                            self.error_count = 1  # 同じ数字が１つ以上含まれるときにerror=1にする
                    # 自分の攻撃プロセス
                    if self.error_count == 0:
                        guess_mark = [self.marks_s[self.num[0]], self.marks_s[self.num[1]],
                                      self.marks_s[self.num[2]], self.marks_s[self.num[3]], self.marks_s[self.num[4]]]
                        # print(self.num)
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
                            font4 = pygame.font.SysFont(None, 50*self.screen_size)
                            hit_blow = font4.render("Hit:{}   Blow:{}".format(self.hit,self.blow), True, (230,180,34),(0,0,0))
                            self.screen.blit(hit_blow, (80*self.screen_size,360*self.screen_size))
                            pygame.display.update()
                            pygame.mixer.Channel(0).play(pygame.mixer.Sound(self.se_dict["clear"])) 
                            time.sleep(2)
                            self.gamescene = 4 #clear画面への遷移
                            pygame.mixer.music.stop()
                            pygame.mixer.music.load(self.bgm_dict["clear"])
                            pygame.mixer.music.set_volume(0.1)
                            pygame.mixer.music.play(loops=-1)
                        elif mode == "normal" and self.enemy_stop < 1:
                            # self.hp_g -= self.damage
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
                        elif mode == "boss" and self.enemy_stop < 1:
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
                if Rect(130*self.screen_size,310*self.screen_size,120*self.screen_size, 50*self.screen_size).collidepoint(event.pos):
                    self.item_screen_count = 1
                    # pass #アイテムコマンド押したときの処理を入れてほしい

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
        self.screen.blit(self.enemy_list[self.enemy_level],self.enemyrect) # 敵の描画
        font2 = pygame.font.SysFont(None, 30*self.screen_size) # turnの表示
        stage = font2.render("turn:{}".format(self.turn), True, (255,255,255))
        font4 = pygame.font.SysFont(None, 50*self.screen_size)
        hit_blow = font4.render("Hit:{}   Blow:{}".format(self.hit,self.blow), True, (255,255,255))
        font = pygame.font.Font("./new_system/ALGERIA.TTF", 40*self.screen_size)
        item_comand = font.render("ITEMS", True, (255,255,255))
        self.screen.blit(item_comand,(130*self.screen_size, 310*self.screen_size))
        self.screen.blit(stage, (5*self.screen_size,5*self.screen_size))
        self.screen.blit(hit_blow, (80*self.screen_size,360*self.screen_size))
        self.screen.blit(self.enter_button_img, self.enter_buttonrect)
        self.screen.blit(self.history_button_img, self.history_buttonrect)
        self.mark_show()
        # ボスのHit,Blow
        font4 = pygame.font.SysFont(None, 40*self.screen_size)
        if self.hit >= 3: #ここでボスのhitが3以上かどうか
            self.alert_count = 1
        if self.alert_count == 1:
            hit_blow = font4.render("Hit:{}   Blow:{}".format(self.hit,self.blow), True, (160,0,0))
        else:
            hit_blow = font4.render("Hit:{}   Blow:{}".format(self.hit,self.blow), True, (255,255,255))
        self.screen.blit(hit_blow, (105*self.screen_size,30*self.screen_size))

    def game_over(self):
        """ゲームオーバー画面の描画
        """
        font = pygame.font.SysFont(None, 80*self.screen_size)
        game = font.render("Game", True, (150, 0, 0))
        over = font.render("Over", True, (150, 0, 0))
        self.screen.blit(game, (105*self.screen_size, 200*self.screen_size))
        self.screen.blit(over, (120*self.screen_size, 250*self.screen_size))
        self.screen.blit(self.return_button_img, self.return_buttonrect)
        self.screen.blit(self.history_button_img, Rect(
            120*self.screen_size, 500*self.screen_size, 120*self.screen_size, 30*self.screen_size))

    def clear(self, dungeon_num: int = 0):
        """クリア画面の描画
        """
        font = pygame.font.SysFont(None, 80*self.screen_size)
        font2 = pygame.font.SysFont(None, 40*self.screen_size)
        clear = font.render("Clear!", True, (230, 180, 34))
        self.screen.blit(clear, (98*self.screen_size, 100*self.screen_size))
        exp = font2.render("EXP:{}".format(self.e_exp), True, (255, 255, 255))
        self.screen.blit(exp, (130*self.screen_size, 200*self.screen_size))
        self.screen.blit(self.return_button_img, self.return_buttonrect)
        self.screen.blit(self.history_button_img, Rect(
            120*self.screen_size, 500*self.screen_size, 120*self.screen_size, 30*self.screen_size))

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
                if Rect(120*self.screen_size, 500*self.screen_size, 120*self.screen_size, 30*self.screen_size).collidepoint(event.pos):
                    self.history_count = 1

    def how_to_play(self):  # how to play 画面の描画
        self.screen.blit(self.how_to_play_img, Rect(
            0, 0, 360*self.screen_size, 640*self.screen_size))
        self.screen.blit(self.return_button_img, self.return_buttonrect)

    def how_to_play_judje(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
                if self.return_buttonrect.collidepoint(event.pos):
                    self.gamescene = 0

    def screen_select(self):
        if self.demand[1] == 1:
            self.screen_count = 1
            self.set_player()
            self.set_mark()
            self.set_enemy()
            self.set_button()
            self.set_mark_entry()
            return
        w, h = pygame.display.get_surface().get_size()
        font = pygame.font.Font("./new_system/Harenosora.otf", 100)
        pc = font.render("PC", True, "WHITE")
        self.screen.blit(pc, (50, 10))
        pcrect = Rect(0, 10, w, h/2-50)
        smartphone = font.render("スマホ", True, "WHITE")
        self.screen.blit(smartphone, (10, h/2+10))
        smartphonerect = Rect(0, h/2+10, w, h/2-50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
                if pcrect.collidepoint(event.pos):
                    self.screen = pygame.display.set_mode((360, 640))
                    self.screen_count = 1
                    self.set_player()
                    self.set_mark()
                    self.set_enemy()
                    self.set_button()
                    self.set_mark_entry()
                if smartphonerect.collidepoint(event.pos):
                    self.screen = pygame.display.set_mode((1080, 1920))
                    self.screen_size = 3
                    self.screen_count = 1
                    self.set_player()
                    self.set_mark()
                    self.set_enemy()
                    self.set_button()
                    self.set_mark_entry()

    def gacha_show(self):
        """ガチャの演出画面の描画
        """
        for i in range(144):
            self.screen.fill((0,0,0))
            if i > 47 and i < 72:
                pygame.draw.circle(self.screen, (240,248,255) ,(180*self.screen_size,320*self.screen_size),(i-47)*self.screen_size,0) # 白い円が中心から徐々に広がる
            if i >= 72:
                self.screen.blit(self.ball_img,Rect(155*self.screen_size,295*self.screen_size,50*self.screen_size,50*self.screen_size))
            pygame.draw.circle(self.screen, (238,130,238),(180*self.screen_size,320*self.screen_size),(5+i)*self.screen_size,3*self.screen_size) # 円環が広がる
            if i > 10:
                pygame.draw.circle(self.screen, (238,130,238),(50*self.screen_size,240*self.screen_size),(i-10)*self.screen_size,3*self.screen_size)
            if i > 15:
                pygame.draw.circle(self.screen, (238,130,238),(300*self.screen_size,400*self.screen_size),(i-15)*self.screen_size,3*self.screen_size)
            if i > 20:
                pygame.draw.circle(self.screen, (238,130,238),(240*self.screen_size,300*self.screen_size),(i-20)*self.screen_size,3*self.screen_size)
            if i > 23:
                pygame.draw.circle(self.screen,(238,130,238),(120*self.screen_size,350*self.screen_size),(i-23)*self.screen_size,3*self.screen_size)
            if i > 25:
                pygame.draw.circle(self.screen, (238,130,238),(220*self.screen_size,150*self.screen_size),(i-25)*self.screen_size,3*self.screen_size)
                pygame.draw.circle(self.screen,(238,130,238),(130*self.screen_size,450*self.screen_size),(i-25)*self.screen_size,3*self.screen_size)
            if i >= 108:
                pygame.draw.circle(self.screen, (240,248,255) ,(180*self.screen_size,320*self.screen_size),(25+(i-108)*15)*self.screen_size,0) # 画面全体を白く塗りつぶす
            pygame.display.update()
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

    def show_prologue(self):
        """プロローグの表示
        """
        j = 0
        self.screen.fill((0,0,0))
        for i in range(108):
            font = pygame.font.SysFont("bizudminchomediumbizudpminchomediumtruetype",25*self.screen_size)
            line_1 = font.render("この世界ではみんな",True, (255*i/108,255*i/108,255*i/108))
            line_2 = font.render("秘密のマークを持っています",True,  (255*i/108,255*i/108,255*i/108))
            self.screen.blit(line_1, (10*self.screen_size,10*self.screen_size))
            self.screen.blit(line_2, (10*self.screen_size,40*self.screen_size))
            pygame.display.update()
            self.clock.tick(self.FPS) 
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
                    if Rect(0,0,360*self.screen_size,640*self.screen_size).collidepoint(event.pos):
                        j = 1 # 画面を押せば飛ばせるようにしたほうがいいかも
            if j == 1:
                line_1 = font.render("この世界ではみんな",True, (255,255,255))
                line_2 = font.render("秘密のマークを持っています",True,  (255,255,255))
                self.screen.blit(line_1, (10*self.screen_size,10*self.screen_size))
                self.screen.blit(line_2, (10*self.screen_size,40*self.screen_size))
                pygame.display.update()
                break
        if j == 0:
            time.sleep(1)

        for i in range(108):
            font = pygame.font.SysFont("bizudminchomediumbizudpminchomediumtruetype",25*self.screen_size)
            line_1 = font.render("この秘密のマークは",True, (255*i/108,255*i/108,255*i/108))
            line_2 = font.render("持ち主を守る",True,  (255*i/108,255*i/108,255*i/108))
            line_3 = font.render("不思議な力の鍵です",True,  (255*i/108,255*i/108,255*i/108))
            self.screen.blit(line_1, (10*self.screen_size,90*self.screen_size))
            self.screen.blit(line_2, (10*self.screen_size,120*self.screen_size))
            self.screen.blit(line_3, (10*self.screen_size,150*self.screen_size))
            pygame.display.update()
            self.clock.tick(self.FPS) 
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
                    if Rect(0,0,360*self.screen_size,640*self.screen_size).collidepoint(event.pos):
                        j = 1 # 画面を押せば飛ばせるようにしたほうがいいかも
            
            if j == 1:
                line_1 = font.render("この秘密のマークは",True, (255,255,255))
                line_2 = font.render("持ち主を守る",True,  (255,255,255))
                line_3 = font.render("不思議な力の鍵です",True,  (255,255,255))
                self.screen.blit(line_1, (10*self.screen_size,90*self.screen_size))
                self.screen.blit(line_2, (10*self.screen_size,120*self.screen_size))
                self.screen.blit(line_3, (10*self.screen_size,150*self.screen_size))
                pygame.display.update()
                break
        if j == 0:
            time.sleep(1)
        
        for i in range(108):
            font = pygame.font.SysFont("bizudminchomediumbizudpminchomediumtruetype",25*self.screen_size)
            line_1 = font.render("冒険者はモンスターの",True, (255*i/108,255*i/108,255*i/108))
            line_2 = font.render("秘密のマークを解いて倒します",True,  (255*i/108,255*i/108,255*i/108))
            self.screen.blit(line_1, (10*self.screen_size,200*self.screen_size))
            self.screen.blit(line_2, (10*self.screen_size,230*self.screen_size))
            pygame.display.update()
            self.clock.tick(self.FPS) 
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
                    if Rect(0,0,360*self.screen_size,640*self.screen_size).collidepoint(event.pos):
                        j = 1 # 画面を押せば飛ばせるようにしたほうがいいかも
            if j == 1:
                line_1 = font.render("冒険者はモンスターの",True, (255,255,255))
                line_2 = font.render("秘密のマークを解いて倒します",True,  (255,255,255))
                self.screen.blit(line_1, (10*self.screen_size,200*self.screen_size))
                self.screen.blit(line_2, (10*self.screen_size,230*self.screen_size))
                pygame.display.update()
                break
        if j == 0:
            time.sleep(1)

        for i in range(108):
            font = pygame.font.SysFont("bizudminchomediumbizudpminchomediumtruetype",25*self.screen_size)
            line_1 = font.render("しかし知能の高いボスには",True, (255*i/108,255*i/108,255*i/108))
            line_2 = font.render("気を付けなくてはいけません",True,  (255*i/108,255*i/108,255*i/108))
            self.screen.blit(line_1, (10*self.screen_size,280*self.screen_size))
            self.screen.blit(line_2, (10*self.screen_size,310*self.screen_size))
            pygame.display.update()
            self.clock.tick(self.FPS) 
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
                    if Rect(0,0,360*self.screen_size,640*self.screen_size).collidepoint(event.pos):
                        j = 1 # 画面を押せば飛ばせるようにしたほうがいいかも
            if j == 1:
                line_1 = font.render("しかし知能の高いボスには",True, (255,255,255))
                line_2 = font.render("気を付けなくてはいけません",True,  (255,255,255))
                self.screen.blit(line_1, (10*self.screen_size,280*self.screen_size))
                self.screen.blit(line_2, (10*self.screen_size,310*self.screen_size))
                pygame.display.update()
                break
        if j == 0:
            time.sleep(1)

        for i in range(108):
            font = pygame.font.SysFont("bizudminchomediumbizudpminchomediumtruetype",25)
            line_1 = font.render("ボスは冒険者の秘密のマークを",True, (255*i/108,255*i/108,255*i/108))
            line_2 = font.render("解いてしまうのです",True,  (255*i/108,255*i/108,255*i/108))
            self.screen.blit(line_1, (10*self.screen_size,360*self.screen_size))
            self.screen.blit(line_2, (10*self.screen_size,390*self.screen_size))
            pygame.display.update()
            self.clock.tick(self.FPS) 
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
                    if Rect(0,0,360*self.screen_size,640*self.screen_size).collidepoint(event.pos):
                        j = 1 # 画面を押せば飛ばせるようにしたほうがいいかも
            if j == 1:
                line_1 = font.render("ボスは冒険者の秘密のマークを",True, (255,255,255))
                line_2 = font.render("解いてしまうのです",True,  (255,255,255))
                self.screen.blit(line_1, (10*self.screen_size,360*self.screen_size))
                self.screen.blit(line_2, (10*self.screen_size,390*self.screen_size))
                pygame.display.update()
                break
        if j == 0:
            time.sleep(1)

        for i in range(108):
            font = pygame.font.SysFont("bizudminchomediumbizudpminchomediumtruetype",25*self.screen_size)
            line_1 = font.render("ボスよりも早く",True, (255*i/108,255*i/108,255*i/108))
            line_2 = font.render("秘密のマークを解きましょう",True,  (255*i/108,255*i/108,255*i/108))
            self.screen.blit(line_1, (10*self.screen_size,440*self.screen_size))
            self.screen.blit(line_2, (10*self.screen_size,470*self.screen_size))
            pygame.display.update()
            self.clock.tick(self.FPS) 
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
                    if Rect(0,0,360*self.screen_size,640*self.screen_size).collidepoint(event.pos):
                        j = 1 # 画面を押せば飛ばせるようにしたほうがいいかも
            if j == 1:
                line_1 = font.render("ボスよりも早く",True, (255,255,255))
                line_2 = font.render("秘密のマークを解きましょう",True,  (255,255,255))
                self.screen.blit(line_1, (10*self.screen_size,440*self.screen_size))
                self.screen.blit(line_2, (10*self.screen_size,470*self.screen_size))
                pygame.display.update()
                break
        if j == 0:
            time.sleep(1)

        for i in range(108):
            font = pygame.font.SysFont("bizudminchomediumbizudpminchomediumtruetype",25*self.screen_size)
            line_1 = font.render("あなたの冒険に祝福を",True, (255*i/108,255*i/108,255*i/108))
            self.screen.blit(line_1, (100*self.screen_size,550*self.screen_size))
            pygame.display.update()
            self.clock.tick(self.FPS) 
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
                    if Rect(0,0,360*self.screen_size,640*self.screen_size).collidepoint(event.pos):
                        j = 1 # 画面を押せば飛ばせるようにしたほうがいいかも
            if j == 1:
                line_1 = font.render("あなたの冒険に祝福を",True, (255,255,255))
                self.screen.blit(line_1, (100*self.screen_size,550*self.screen_size))
                pygame.display.update()
                break
        time.sleep(2)


    def make_1ans(self):
        
        if self.demand[0] == 1:
            self.ans_g = [0, 1, 2, 3, 5]
        else:
            nums = list(range(self.mark_qty_all))
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
        self.choice_current_page = 0

    def choice_screen(self, title, choice: List[str], message: List[str], dict_name, delete_dict_list_when_return: List[str] = [], multi_page_checker: str = "single",special_action_when_return:int = 0):
        """選択肢を表示させるためのモジュール。
        選択肢をそばにその選択肢の説明を表示することで、タップ部分の大きさと選択肢数・文字量の両立を図る。
        タイトルは全角14字*2行、選択肢は6つまで、選択肢説明は全角20行*2行、メッセージは3行まで対応。
        選択肢数がこれを超える場合は、multiを使うこと。
        choiceは2重のリストとし、外側のリストの番号は選択肢番号を、内側のリストは0が選択肢の名前、1が選択肢の説明となる。
        title,choiceの説明部分は、どちらも「str」「長さ1のリスト」「長さ2のリスト」の全てに対応。
        自動改行したいときはstrか長さ1のリスト、自分で改行したいときは長さ2のリストを使用する
        選択が行われた場合、選択肢の番号と名前を、self.choice_dictのdict_nameに登録する
        dict_name="装備"のとき、選択肢の番号はself.choice_dict["装備"]["number"]に、選択肢の名前をself.choice_dict["装備"]["name"]に登録する
        special_action_when_returnは、returnボタンを押したときに、choice_screen関数に予め記録された関数を実行させる。
        【使い方】
        まず、self.dict_name_listに【選択肢の名称】を追加
        次に、引っ掛ける条件を「if self.choice_dict["【選択肢の名称】"]["number"] == "False":」とする。
        さらに、self.choice_screenの最後の引数に【選択肢の名称】を入力する。
        「RETURN」ボタンを押した際に、削除するべき｛ 前 の 選択肢の名称｝を決定する(設定がなければ、ホーム画面に戻る)
        選択結果は、self.choice_dictに保存される。
        何かおかしいと思ったら、
        ・self.dict_name_listに【選択肢の名称】を追加したか
        ・3箇所の【選択肢の名称】が全て同じであるか
        ・dict検索時のnumberとnameを間違えてないか"""
        self.choice_buttonrect = []
        choice_answer = False
        font_title = pygame.font.SysFont(
            "bizudminchomediumbizudpminchomediumtruetype", 24*self.screen_size)
        font = pygame.font.SysFont(
            "bizudminchomediumbizudpminchomediumtruetype", 20*self.screen_size)
        font2 = pygame.font.SysFont(
            "bizudminchomediumbizudpminchomediumtruetype", 15*self.screen_size)
        # titleを表示
        title = self.auto_line_break(title,28)
        print_title1 = font_title.render(title[0], True, "WHITE")
        self.screen.blit(
            print_title1, (11*self.screen_size, 12*self.screen_size))
        if len(title) > 1:
            print_title2 = font_title.render(title[1], True, "WHITE")
            self.screen.blit(
                print_title2, (11*self.screen_size, 44*self.screen_size))
        # 選択肢を表示
        for i in range(len(choice)):
            self.choice_buttonrect.append(Rect(24*self.screen_size, (78+70*i)*self.screen_size, 300*self.screen_size, 60*self.screen_size))
        for i, name in enumerate(choice):
            print_choice_index = font.render(name[0], True, "WHITE")
            self.screen.blit(print_choice_index, (24*self.screen_size, (81+70*i)*self.screen_size))
            choice_detail = self.auto_line_break(name[1], 40)
            for j, detail in enumerate(choice_detail):
                print_choice_detail = font2.render(detail, True, "WHITE")
                self.screen.blit(print_choice_detail, (40*self.screen_size, (105+70*i+18*j)*self.screen_size))
        self.screen.blit(self.return_button_img, self.return_buttonrect)
        if multi_page_checker == "multi":
            self.screen.blit(self.right_img, self.right_buttonrect)
            self.screen.blit(self.left_img, self.left_buttonrect)
        # メッセージを表示
        for i, name in enumerate(message):
            print_message = font2.render(name, True, "WHITE")
            self.screen.blit(
                print_message, (11*self.screen_size, (503+21*i)*self.screen_size))

        # 以下、本来は別関数（judge_～～～）となるはずだった部分
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
                for i in range(len(choice)):
                    if self.choice_buttonrect[i].collidepoint(event.pos):
                        pygame.mixer.Channel(0).play(pygame.mixer.Sound(self.se_dict["start"]))
                        print("選択肢：{}".format(i))
                        self.choice_judge = 1
                        time.sleep(0.25)
                        self.choice_dict.update({dict_name: {"number": i,"name": choice[i][0]}})
                        print(self.choice_dict)
                # Returnボタンが押されたときの動作
                if self.return_buttonrect.collidepoint(event.pos):
                    # 特別動作が登録されたいた場合は関数を実行する
                    if special_action_when_return == 1:
                        self.escape_from_item_screen_when_battle()
                        return
                    # 何も設定されてない場合はホーム画面まで戻る
                    if delete_dict_list_when_return == []:
                        delete_dict_list_when_return = self.dict_name_list
                    time.sleep(0.5)
                    for dicts in delete_dict_list_when_return:
                        self.choice_dict.update({dicts: {"number": "False", "name": "False"}})
                if multi_page_checker == "multi":
                    if self.left_buttonrect.collidepoint(event.pos):
                        self.choice_current_page -= 1
                    if self.right_buttonrect.collidepoint(event.pos):
                        self.choice_current_page += 1

    def auto_line_break(self,text,line_length):
        """line_breakをchoice用に使いやすくしたもの
        textがlistならそれぞれの行を表示
        strの場合、自動改行
        いずれにしても2行まで（それ以降は無視される）"""
        if type(text) == list and len(text) >1:
            pass
        else:
            if type(text) == list and len(text) == 1:
                text = str(text[0])
            text = self.line_break(text, line_length)
        return text

    def escape_from_item_screen_when_battle(self):
        self.item_screen_count = 0

    def old_choice_screen(self, title, choice: List[str], message: List[str], dict_name, delete_dict_list_when_return: List[str] = [], multi_page_checker: str = "single"):
        """選択肢を表示させるためのモジュール
        タイトルは28文字まで、選択肢は6つまで、メッセージは8行まで対応（それを超える場合はchoice_screen_multiを使う）
        選択が行われた場合、選択肢の番号と名前を、self.choice_dictのdict_nameに登録する
        dict_name="装備"のとき、選択肢の番号はself.choice_dict["装備"]["number"]に、選択肢の名前をself.choice_dict["装備"]["name"]に登録する
        【使い方】
        まず、self.dict_name_listに【選択肢の名称】を追加
        次に、引っ掛ける条件を「if self.choice_dict["【選択肢の名称】"]["number"] == "False":」とする。
        さらに、self.choice_screenの最後の引数に【選択肢の名称】を入力する。
        【10/8-14:30追加】：「RETURN」ボタンを押した際に、削除するべき｛ 前 の 選択肢の名称｝を決定する(設定がなければ、ホーム画面に戻る)
        選択結果は、self.choice_dictに保存される。
        何かおかしいと思ったら、
        ・self.dict_name_listに【選択肢の名称】を追加したか
        ・3箇所の【選択肢の名称】が全て同じであるか
        ・dict検索時のnumberとnameを間違えてないか
        をチェック
        """
        self.choice_buttonrect = []
        choice_answer = False
        font_title = pygame.font.SysFont(
            "bizudminchomediumbizudpminchomediumtruetype", 24*self.screen_size)
        font = pygame.font.SysFont(
            "bizudminchomediumbizudpminchomediumtruetype", 21*self.screen_size)
        font2 = pygame.font.SysFont(
            "bizudminchomediumbizudpminchomediumtruetype", 16*self.screen_size)
        # titleを表示
        # titleが長すぎたら改行して2行にする
        title = str(title)
        # title_list = self.line_break(message, 32)
        if len(title) >= 14:
            title2 = title[14:len(title)]
            title = title[0:14]
        else:
            title2 = ""
        print_title = font_title.render(title, True, "WHITE")
        self.screen.blit(
            print_title, (11*self.screen_size, 12*self.screen_size))
        print_title2 = font_title.render(title2, True, "WHITE")
        self.screen.blit(
            print_title2, (11*self.screen_size, 44*self.screen_size))
        # 選択肢を表示
        for i in range(len(choice)):
            self.choice_buttonrect.append(Rect(
                24*self.screen_size, (77+46*i)*self.screen_size, 300*self.screen_size, 33*self.screen_size))
        for i, name in enumerate(choice):  # 選択肢の数だけ描画
            print_choice = font.render(name, True, "WHITE")
            self.screen.blit(
                print_choice, (24*self.screen_size, (83+46*i)*self.screen_size))
        self.screen.blit(self.return_button_img, self.return_buttonrect)
        if multi_page_checker == "multi":
            self.screen.blit(self.right_img, self.right_buttonrect)
            self.screen.blit(self.left_img, self.left_buttonrect)
        # メッセージを表示
        for i, name in enumerate(message):
            print_message = font2.render(name, True, "WHITE")
            self.screen.blit(
                print_message, (11*self.screen_size, (310+21*i)*self.screen_size))

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
                        time.sleep(0.25)
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
                if multi_page_checker == "multi":
                    if self.left_buttonrect.collidepoint(event.pos):
                        self.choice_current_page -= 1
                    if self.right_buttonrect.collidepoint(event.pos):
                        self.choice_current_page += 1

    def choice_screen_multi(self, title, choice: List[str], message: List[str], dict_name, delete_dict_list_when_return: List[str] = [],auto_page_grouping = "on" ,message_multi_page = "off",special_action_when_return:int = 0):
        """選択肢が複数ページに跨る場合はこちらを使用する。
        特に指定がない場合は、自動で複数ページ化する（自動の場合、選択肢が6以下なら複数ページとならない）。
        手動でやる場合、最後から2番目の引数を"off"とし、リストの重なり数を1つ増やし、ページ毎にまとめること。
        choice,message以外はchoice_screenと同様。最終引数を"on"にすると、choiceだけでなくmessageも複数ページ化できる。
        この場合、最も外側のリストのlengthは、choiceとmessageでそれぞれ等しくすること。
        自動化とメッセージ複数ページ化を同時にonにする場合の動作は未確認（ヤバそう）"""
        page_qty = len(choice)
        if auto_page_grouping == "on":
            if page_qty <= 6:
                self.choice_screen(title,choice, message, dict_name, delete_dict_list_when_return)
                return
            else:
                choice = self.arrange_choice_list(choice)
        # 一番右のページで右を押したら左に戻ってくるための仕掛け
        page_num = self.choice_current_page % page_qty
        if message_multi_page == "off":
            self.choice_screen(title, choice[page_num], message, dict_name,
                           delete_dict_list_when_return, "multi",special_action_when_return)
        else:
            self.choice_screen(title, choice[page_num], message[page_num], dict_name,
                           delete_dict_list_when_return, "multi",special_action_when_return)

    def arrange_choice_list(self,choice):
        arranged_choice = []
        temporal_box = []
        i_count = 0
        # if auto_page_grouping == "on":
        for i in range(len(choice)//6):
            for j in range(6):
                temporal_box.append(choice[i*6+j])
            arranged_choice.append(temporal_box)
            temporal_box = []
            i_count = i+1
        if len(choice)%6 != 0:
            for j in range(len(choice)%6):
                temporal_box.append(choice[j+6*i_count])
            arranged_choice.append(temporal_box)
            temporal_box = []
        return arranged_choice
        # print(arranged_choice)

    def yes_no_choice(self,title,message,dict_name, delete_dict_list_when_return: List[str] = []):
        """はいかいいえの選択画面
        タイトルを長めにとれる。
        タイトル4行、メッセージ6行まで。"""
        choice = [["はい",""],["いいえ",""]]
        self.choice_buttonrect = []
        choice_answer = False
        font_title = pygame.font.SysFont(
            "bizudminchomediumbizudpminchomediumtruetype", 24*self.screen_size)
        font = pygame.font.SysFont(
            "bizudminchomediumbizudpminchomediumtruetype", 20*self.screen_size)
        font2 = pygame.font.SysFont(
            "bizudminchomediumbizudpminchomediumtruetype", 15*self.screen_size)
        # titleを表示
        title = self.auto_line_break(title,28)
        print_title1 = font_title.render(title[0], True, "WHITE")
        self.screen.blit(
            print_title1, (11*self.screen_size, 12*self.screen_size))
        if len(title) > 1:
            print_title2 = font_title.render(title[1], True, "WHITE")
            self.screen.blit(
                print_title2, (11*self.screen_size, 44*self.screen_size))
        if len(title) > 2:
            print_title3 = font_title.render(title[2], True, "WHITE")
            self.screen.blit(
                print_title3, (11*self.screen_size, 76*self.screen_size))
        if len(title) > 3:
            print_title4 = font_title.render(title[2], True, "WHITE")
            self.screen.blit(
                print_title4, (11*self.screen_size, 108*self.screen_size))
        # 選択肢を表示
        for i in range(len(choice)):
            self.choice_buttonrect.append(Rect(24*self.screen_size, (148+70*i)*self.screen_size, 300*self.screen_size, 60*self.screen_size))
        for i, name in enumerate(choice):
            print_choice_index = font.render(name[0], True, "WHITE")
            self.screen.blit(print_choice_index, (24*self.screen_size, (151+70*i)*self.screen_size))
            choice_detail = self.auto_line_break(name[1], 40)
            for j, detail in enumerate(choice_detail):
                print_choice_detail = font2.render(detail, True, "WHITE")
                self.screen.blit(print_choice_detail, (40*self.screen_size, (175+70*i+18*j)*self.screen_size))
        self.screen.blit(self.return_button_img, self.return_buttonrect)
        # メッセージを表示
        for i, name in enumerate(message):
            print_message = font2.render(name, True, "WHITE")
            self.screen.blit(
                print_message, (11*self.screen_size, (440+21*i)*self.screen_size))

        # 以下、本来は別関数（judge_～～～）となるはずだった部分
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
                for i in range(len(choice)):
                    if self.choice_buttonrect[i].collidepoint(event.pos):
                        pygame.mixer.Channel(0).play(pygame.mixer.Sound(self.se_dict["start"]))
                        print("選択肢：{}".format(i))
                        self.choice_judge = 1
                        time.sleep(0.25)
                        self.choice_dict.update({dict_name: {"number": i,"name": choice[i][0]}})
                        print(self.choice_dict)
                # Returnボタンが押されたときの動作
                if self.return_buttonrect.collidepoint(event.pos):
                    # 何も設定されてない場合はホーム画面まで戻る
                    if delete_dict_list_when_return == []:
                        delete_dict_list_when_return = self.dict_name_list
                    time.sleep(0.5)
                    for dicts in delete_dict_list_when_return:
                        self.choice_dict.update({dicts: {"number": "False", "name": "False"}})

    def message_screen(self, message: str):
        """メッセーのみを表示したいときに使うモジュール
        メッセージは自動改行される
        """
        self.choice_buttonrect = []
        choice_answer = False
        font_title = pygame.font.SysFont(
            "bizudminchomediumbizudpminchomediumtruetype", 24*self.screen_size)
        font = pygame.font.SysFont(
            "bizudminchomediumbizudpminchomediumtruetype", 21*self.screen_size)
        font2 = pygame.font.SysFont(
            "bizudminchomediumbizudpminchomediumtruetype", 16*self.screen_size)
        # 自動改行
        message = str(message)
        text_list = self.line_break(message, 32)
        for i, name in enumerate(text_list):
            print_message = font.render(name, True, "WHITE")
            self.screen.blit(
                print_message, (11*self.screen_size, (100+27*i)*self.screen_size))
        self.screen.blit(self.return_button_img, self.return_buttonrect)

        # 以下、本来は別関数（judge_～～～）となるはずだった部分
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
                # Returnボタンが押されたときの動作
                if self.return_buttonrect.collidepoint(event.pos):
                    self.message = ""

    def item_use_battle(self,item_name):
        self.item_use_history = {}
        effect_type = self.item_info(item_name,"effect_type")
        effect_val_min = self.item_info(item_name,"effect_val")
        effect_val_max = self.item_info(item_name,"effect_val_max")
        if effect_val_max is None:
            effect_val = effect_val_min
        else:
            effect_val = self.randex(effect_val_min,effect_val_max)
        self.enemy_stop = 0

        if effect_type in ["hp_rec","hp_rec_act"]:
            self.hp_g = min(self.max_hp,self.hp_g+effect_val)
        elif effect_type == "hp_rec_act":
            self.enemy_stop = 1
        elif effect_type == "enemy_jam":
            self.enemy_stop = effect_val + 1
        else:
            pass

    def item_use_before_battle(self,item_name):
        """主に選択肢を減らす系のアイテム。使用するタイミングがつかめないため未実装。
        タイミングさえ決めれば、このまま使えるようにしてある"""
        self.item_use_history = {}
        effect_type = self.item_info(item_name,"effect_type")
        effect_val_min = self.item_info(item_name,"effect_val")
        effect_val_max = self.item_info(item_name,"effect_val_max")
        if effect_val_max is None:
            effect_val = effect_val_min
        else:
            effect_val = int(self.randex(effect_val_min,effect_val_max))
        self.enemy_stop = 0
        for num, attr in enumerate(self.attr_list4):
            if effect_type == "{}_temporal".format(attr):
                self.attr_power[num] += effect_val
        if effect_type == "all_attr_temporal":
            for i in range(4):
                self.attr[i] += effect_val

    def normal_action(self):
        self.hp_g -= self.damage
            

    def damage_effect(self,count=2,period=0.2):
        pygame.mixer.Channel(0).play(
            pygame.mixer.Sound(self.se_dict["attack"]))
        for i in range(count):
            self.screen.blit(
                self.enemy_damage_list[self.dungeon_num], self.enemyrect)
            pygame.display.update()
            time.sleep(period/2)
            self.screen.blit(
                self.enemy_list[self.dungeon_num], self.enemyrect)
            pygame.display.update()
            time.sleep(period/2)


    def historylast_show(self):

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












