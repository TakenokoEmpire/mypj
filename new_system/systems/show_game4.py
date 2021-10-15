
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
import cursor, tools
import os

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
                #  max_dungeon_num: int = 3,
                 gamescene: int = 0,
                 demand: List[int] = [0,0,0,0,0,0]):
        print("showgame init")
        super().__init__()
        self.demand = demand
        self.num = num
        if self.demand[1] != 1:
            self.screen = pygame.display.set_mode(
                display_size, HWSURFACE | FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((360, 640))
        # self.max_dungeon_num = max_dungeon_num
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
        # self.dungeon_type = ""

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
        self.level_up_box = []
        self.alert_count = 0
        self.attr_mark_qty = [4,4,4,4]
        self.mark_qty_all = 16
        self.attr_judge_battle()
        self.attr_mark_dict = {}
        self.make_attr_mark_dict()
        self.make_1ans()
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

    def set_town(self):
        self.town_back_list = {}
        for stage_minus1 in range(5):
            stage = stage_minus1 + 1
            self.town_back_list[stage] = pygame.image.load("./new_system/mypj3/img/scenery/town{}.png".format(stage))
            self.town_back_list[stage] = pygame.transform.rotozoom(self.town_back_list[stage], 0, self.screen_size)

        self.townbackrect=Rect(0, 70*self.screen_size,
                              187*self.screen_size, 250*self.screen_size)



    def set_enemy(self):
        """敵の設定
        """
        # ダンジョン番号毎の敵画像
        # ダメージときに点滅させるために2種類用意

        self.enemy_list = {}
        self.enemy_back_list = {}
        self.enemyrect = {}
        for stage_minus1 in range(15):
            stage = stage_minus1 + 1
            self.enemy_list[stage] = pygame.image.load("./new_system/mypj3/img/monster/enemy_{}.png".format(stage)).convert_alpha()
            self.enemy_list[stage] = pygame.transform.rotozoom(self.enemy_list[stage], 0, self.screen_size)
            self.enemy_back_list[stage] = pygame.image.load("./new_system/mypj3/img/scenery/sc{}.png".format(stage))
            self.enemy_back_list[stage] = pygame.transform.rotozoom(self.enemy_back_list[stage], 0, self.screen_size)
            self.enemyrect[stage] = Rect(180*self.screen_size-int(self.enemy_list[stage].get_width()/2), 85*self.screen_size,187*self.screen_size, 250*self.screen_size)
        self.scenerect= Rect(0, 70*self.screen_size,
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
            25*self.screen_size, 580*self.screen_size, 120*self.screen_size, 30*self.screen_size)
        self.stage_select_buttonrect = []
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
            25*self.screen_size, 520*self.screen_size, 120*self.screen_size, 32*self.screen_size)

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
        self.dungeon_num = -1

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


    def stage_select_effect(self):
        pygame.mixer.Channel(0).play(
            pygame.mixer.Sound(self.se_dict["start"]))
        time.sleep(1)
        if self.gamescene == 1:
            pygame.mixer.music.load(self.bgm_dict["normal"])
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(loops=-1)
        elif self.gamescene == 2:
            pygame.mixer.music.load(self.bgm_dict["boss"])
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(loops=-1)

    def normal_stage(self, mode="normal"):
        """通常ステージの描画
        """

        self.screen.blit(self.enemy_back_list[self.dungeon_num],self.scenerect) # 背景の描画
        self.screen.blit(self.enemy_list[self.dungeon_num],self.enemyrect[self.dungeon_num]) # 敵の描画
        font2 = pygame.font.SysFont(None, 30*self.screen_size) # turnの表示
        # stage = font2.render("turn:{}".format(self.turn), True, (255,255,255))
        font4 = pygame.font.SysFont(None, 45*self.screen_size)
        #ターン数が2桁になったときに位置がずれないように
        if self.turn < 10:
            hit_blow = font4.render("Turn:{}    Hit:{}    Blow:{}".format(self.turn,self.hit,self.blow), True, (255,255,255))
        else:
            hit_blow = font4.render("Turn:{}  Hit:{}    Blow:{}".format(self.turn,self.hit,self.blow), True, (255,255,255))
        font = pygame.font.Font("./new_system/ALGERIA.TTF", 40*self.screen_size)
        item_comand = font.render("ITEMS", True, (255,255,255))
        self.screen.blit(item_comand,(210*self.screen_size, 555*self.screen_size))
        # self.screen.blit(stage, (5*self.screen_size,5*self.screen_size))
        self.screen.blit(hit_blow, (22*self.screen_size,360*self.screen_size))
        self.screen.blit(self.enter_button_img, self.enter_buttonrect)
        self.screen.blit(self.history_button_img, self.history_buttonrect)
        self.mark_show()

        # self.screen.blit(self.enemy_list[self.dungeon_num], self.enemyrect[self.dungeon_num])  # 敵の描画
        font2 = pygame.font.SysFont(None, 30*self.screen_size)  # turnの表示
        # stage = font2.render("turn:{}".format(self.turn), True, (255, 255, 255))
        pygame.draw.line(self.screen, (0, 200, 0), (30*self.screen_size, 40*self.screen_size),(30*self.screen_size+self.hp_g*self.hp_bar_ratio*self.screen_size, 40*self.screen_size), 10*self.screen_size)  # HPの表示
        font3 = pygame.font.SysFont(None, 20*self.screen_size)
        hp_word = font3.render("HP", True, (255, 255, 255))
        hp_value = font3.render("{}".format(self.hp_g), True, (255, 255, 255))

        damage = self.hp - self.hp_g
        if damage != 0:
            pygame.draw.line(self.screen, (200, 0, 0),
                             (30*self.screen_size+self.hp_g*self.hp_bar_ratio*self.screen_size, 40*self.screen_size), (30*self.screen_size+(self.hp_g+damage)*self.hp_bar_ratio*self.screen_size, 40*self.screen_size), 10*self.screen_size)
        self.screen.blit(hp_word, (5*self.screen_size, 35*self.screen_size))
        self.screen.blit(hp_value, (30*self.screen_size+(self.hp_g+damage)*self.hp_bar_ratio*self.screen_size+2*self.screen_size, 35*self.screen_size))
        self.mark_show()
        if self.hp_g <= 0:
            self.game_over_1()

    def boss_action(self, mode="normal"):
        if mode == "normal":
            return
        if self.jamming_judge("boss") == "stop":
            print("敵の調査を妨害した！")
            time.sleep(1)
        else:
            try:
                self.boss_guess_list = self.boss_history[self.boss_turn-1]["guess"]
                self.boss_hit = self.boss_history[self.boss_turn-1]["hit"]
                self.boss_blow = self.boss_history[self.boss_turn-1]["blow"]
                self.damage_effect(mode)
                if self.boss_hit == 3:
                    self.damage_effect(mode)
                self.boss_turn += 1
            except IndexError:
                pass
            # print([self.boss_guess_list, self.boss_hit, self.boss_blow])
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
                        self.guess_list.append(guess_mark)  # マークの履歴
                        self.hit, self.blow = self.judge_guess(
                            guess=self.num)  # 判定
                        self.hit_list.append(self.hit)
                        self.blow_list.append(self.blow)
                        self.turn_switch += 1  # ボス用
                        self.boss_action(mode)  # ボス用
                        if self.hit == 5:
                            font4 = pygame.font.SysFont(None, 45*self.screen_size)
                            if self.turn < 10:
                                hit_blow = font4.render("Turn:{}    Hit:{}    Blow:{}".format(self.turn,self.hit,self.blow), True, (230,180,34),(0,0,0))
                            else:
                                hit_blow = font4.render("Turn:{}  Hit:{}    Blow:{}".format(self.turn,self.hit,self.blow), True, (230,180,34),(0,0,0))
                            self.screen.blit(hit_blow, (22*self.screen_size,360*self.screen_size))
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
                            self.damage_effect(mode)
                        elif mode == "boss" and self.enemy_stop < 1:
                            if self.boss_hit == 5:
                                self.hp_g -= self.damage*100
                                self.hp_g -= self.damage
                                pygame.mixer.Channel(0).play(
                                    pygame.mixer.Sound(self.se_dict["attack"]))
                        self.turn += 1
                        if self.hp_g <= 0:
                            self.game_over_1()
                if self.history_buttonrect.collidepoint(event.pos):
                    self.history_count = 1
                if Rect(210*self.screen_size,550*self.screen_size,120*self.screen_size, 50*self.screen_size).collidepoint(event.pos):
                    self.item_screen_count = 1
                    # pass #アイテムコマンド押したときの処理を入れてほしい

    def game_over_1(self):
        self.gamescene = 3
        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.bgm_dict["failed"])
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.Channel(0).play(
            pygame.mixer.Sound(self.se_dict["failed"]))

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
        self.screen.blit(self.enemy_back_list[self.dungeon_num],self.scenerect) # 背景の描画
        self.screen.blit(self.enemy_list[self.dungeon_num],self.enemyrect[self.dungeon_num]) # 敵の描画
        font2 = pygame.font.SysFont(None, 30*self.screen_size) # turnの表示
        # stage = font2.render("turn:{}".format(self.turn), True, (255,255,255))
        font4 = pygame.font.SysFont(None, 45*self.screen_size)
        #ターン数が2桁になったときに位置がずれないように
        if self.turn < 10:
            hit_blow = font4.render("Turn:{}    Hit:{}    Blow:{}".format(self.turn,self.hit,self.blow), True, (255,255,255))
        else:
            hit_blow = font4.render("Turn:{}  Hit:{}   Blow:{}".format(self.turn,self.hit,self.blow), True, (255,255,255))
        font = pygame.font.Font("./new_system/ALGERIA.TTF", 40*self.screen_size)
        item_comand = font.render("ITEMS", True, (255,255,255))
        self.screen.blit(item_comand,(210*self.screen_size, 555*self.screen_size))
        self.screen.blit(hit_blow, (22*self.screen_size,360*self.screen_size))
        self.screen.blit(self.enter_button_img, self.enter_buttonrect)
        self.screen.blit(self.history_button_img, self.history_buttonrect)
        self.mark_show()
        # ボスのHit,Blow
        font4 = pygame.font.SysFont(None, 36*self.screen_size)
        if self.boss_hit >= 3: #ここでボスのhitが3以上かどうか
            self.alert_count = 1
        if self.alert_count == 1:
            hit_blow = font4.render("Turn:{} Hit:{}  Blow:{}".format(self.boss_turn,self.boss_hit,self.boss_blow), True, (190,20,20))
        else:
            if self.boss_turn < 10:
                hit_blow = font4.render("Turn:{}   Hit:{}  Blow:{}".format(self.boss_turn,self.boss_hit,self.boss_blow), True, (255,255,255))
            else:
                hit_blow = font4.render("Turn:{} Hit:{} Blow:{}".format(self.boss_turn,self.boss_hit,self.boss_blow), True, (255,255,255))
        self.screen.blit(hit_blow, (111*self.screen_size,6*self.screen_size))
        # try:
        font5 = pygame.font.SysFont(None, 49*self.screen_size)
        boss_show = font5.render("BOSS", True, (190,20,20))
        self.screen.blit(boss_show, (7*self.screen_size,15*self.screen_size))
        font6 = pygame.font.SysFont(None, 28*self.screen_size)
        enemy_guess_str = font6.render("Guess:", True, (255,255,255))
        self.screen.blit(enemy_guess_str, (111*self.screen_size,35*self.screen_size))
        try:
            for j in range(5):
                self.screen.blit(self.marks_s_16[int(self.boss_guess_list[j],base=16)], ((180+j*30)*self.screen_size, 32*self.screen_size, 30*self.screen_size, 30*self.screen_size))
        except IndexError:
            pass

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
        # 入場可能ダンジョンを更新
        if self.dungeon_num == self.frontier_stage_id:
            self.mysheet[self.vhindex(self.mysheet,"frontier",1,"total",1,"excel")] = self.dungeon_num + 1

        font = pygame.font.SysFont(None, 80*self.screen_size)
        font2 = pygame.font.SysFont(None, 40*self.screen_size)
        font3 = pygame.font.SysFont(None, 28*self.screen_size)
        font_j = pygame.font.Font("./new_system/Harenosora.otf", 26*self.screen_size)
        if self.dungeon_type == "normal":
            clear = font.render("CLEAR!!", True, (230, 180, 34))
            self.screen.blit(clear, (58*self.screen_size, 100*self.screen_size))
        elif self.dungeon_type == "boss":
            clear = font.render("VICTORY!!!", True, (255, 32, 32))
            self.screen.blit(clear, (29*self.screen_size, 100*self.screen_size))
        exp = font2.render("EXP:+{}".format(self.e_exp), True, (255, 255, 255))
        exp_left = font3.render("To next: {}/{}".format(self.vhlookup(self.book["level_table"],str(self.lv+1),1,"exp",1)-self.exp,self.vhlookup(self.book["level_table"],str(self.lv+1),1,"exp",1)-self.vhlookup(self.book["level_table"],str(self.lv),1,"exp",1)), True, (255, 255, 255))
        money = font2.render("Gold:+{}".format(self.e_money), True, (255, 255, 255))
        drop1 = font2.render("Drop", True, (255, 255, 255))
        drop2 = font_j.render(self.droplist[0], True, (255, 255, 255))
        self.screen.blit(exp, (50*self.screen_size, 200*self.screen_size))
        self.screen.blit(exp_left, (65*self.screen_size, 240*self.screen_size))
        self.screen.blit(money, (50*self.screen_size, 300*self.screen_size))
        self.screen.blit(drop1, (50*self.screen_size, 360*self.screen_size))
        self.screen.blit(drop2, (75*self.screen_size, 400*self.screen_size))
        self.screen.blit(self.return_button_img, self.return_buttonrect)
        self.screen.blit(self.history_button_img, Rect(
            120*self.screen_size, 500*self.screen_size, 120*self.screen_size, 30*self.screen_size))

    def level_up_screen(self):
        """レベルアップ描写
        レベルアップがない場合は何も起きない
        while len(self.level_up_box) == 0:の形にして、表示するごとにboxを減らしていけば
        「2レベル上がったら2回画面表示」が可能になるはず"""
        while len(self.level_up_box) > 0:
            font = pygame.font.SysFont(None, 80*self.screen_size)
            font2 = pygame.font.SysFont(None, 40*self.screen_size)
            levelup = font.render("LEVEL UP!!", True, (230, 180, 34))
            self.screen.blit(levelup, (98*self.screen_size, 100*self.screen_size))
            lvup = font2.render("Lv:{} -> {}".format(self.level_up_box[0][0],self.level_up_box[0][1]), True, (255, 255, 255))
            hpup = font2.render("HP:{} -> {}".format(self.level_up_box[0][2],self.level_up_box[0][3]), True, (255, 255, 255))
            self.screen.blit(lvup, (130*self.screen_size, 200*self.screen_size))
            self.screen.blit(hpup, (130*self.screen_size, 260*self.screen_size))
            self.screen.blit(self.return_button_img, self.return_buttonrect)
            self.screen.blit(self.history_button_img, Rect(
                120*self.screen_size, 500*self.screen_size, 120*self.screen_size, 30*self.screen_size))
            if len(self.level_up_box) > 1:
                self.level_up_box = self.level_up_box[1:]
            else:
                self.level_up_box = []
            return


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
            self.set_town()
            self.set_button()
            self.set_mark_entry()
            return
        w, h = pygame.display.get_surface().get_size()
        font = pygame.font.Font("./new_system/Harenosora.otf", 100)
        pc = font.render("PC", True, "WHITE")
        self.screen.blit(pc, (50, 10))
        pcrect = Rect(0, 10, w, h/2-50)

        smartphone = font.render("スマホ", True, "WHITE")
        self.screen.blit(smartphone, (10, h/3+10))
        smartphonerect = Rect(0, h/3+10, w, h/2-50)

        smartphone_hires = font.render("スマホ(大)", True, "WHITE")
        self.screen.blit(smartphone_hires, (10, h/1.5+10))
        smartphone_hiresrect = Rect(0, h/1.5+10, w, h/2-50)

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
                if smartphone_hiresrect.collidepoint(event.pos):
                    self.screen = pygame.display.set_mode((1440, 2560))
                    self.screen_size = 4
                    self.screen_count = 1
                    self.set_player()
                    self.set_mark()
                    self.set_enemy()
                    self.set_button()
                    self.set_mark_entry()

    def gacha_show(self,rarity,rand_value_judge = "off"):
        """ガチャの演出画面の描画
        レアリティを引数にとり演出が変わる
        rand_value_judgeをonにすると、0~1の間で乱数がどれだけいい値が出たかによって演出を変更する。
        """
        if rand_value_judge == "on":
            if rarity < 0.25:
                rarity = int(1)
            elif rarity < 0.75:
                rarity = int(2)
            elif rarity < 0.95: 
                rarity = int(3)
            elif rarity < 0.99:
                rarity = int(4)
            elif rarity <=1:
                rarity = int(5)

        color_dict = {1:(96,96,96),2:(72,72,216),3:(238,130,238),4:(238,130,238),5:(238,130,238)}
        length_dict = {1:108,2:108,3:136,4:144,5:224}
        central_ball_dict = {1:0,2:0,3:1,4:1,5:1}
        last_speed_dict = {1:100,2:100,3:100,4:15,5:2}
        for i in range(length_dict[rarity]):
            self.screen.fill((0,0,0))
            if i > 47 and i < 72 and rarity >= 3:
                pygame.draw.circle(self.screen, (240,248,255) ,(180*self.screen_size,320*self.screen_size),(i-47)*self.screen_size,0) # 白い円が中心から徐々に広がる
            if i >= 72 and i<108 and rarity >= 3:
                self.screen.blit(self.ball_img,Rect(180*self.screen_size,320*self.screen_size,50*self.screen_size,50*self.screen_size))
            if i >= 108 and i<120 and rarity == 3:
                pygame.draw.circle(self.screen, (240,248,255) ,(180*self.screen_size,320*self.screen_size),(25-(i-108))*self.screen_size,0)
            pygame.draw.circle(self.screen, color_dict[rarity],(180*self.screen_size,320*self.screen_size),(5+i)*self.screen_size,3*self.screen_size) # 円環が広がる
            if i > 10:
                pygame.draw.circle(self.screen, color_dict[rarity],(50*self.screen_size,240*self.screen_size),(i-10)*self.screen_size,3*self.screen_size)
            if i > 15:
                pygame.draw.circle(self.screen, color_dict[rarity],(300*self.screen_size,400*self.screen_size),(i-15)*self.screen_size,3*self.screen_size)
            if i > 20:
                pygame.draw.circle(self.screen, color_dict[rarity],(240*self.screen_size,300*self.screen_size),(i-20)*self.screen_size,3*self.screen_size)
            if i > 23:
                pygame.draw.circle(self.screen,color_dict[rarity],(120*self.screen_size,350*self.screen_size),(i-23)*self.screen_size,3*self.screen_size)
            if i > 25:
                pygame.draw.circle(self.screen, color_dict[rarity],(220*self.screen_size,150*self.screen_size),(i-25)*self.screen_size,3*self.screen_size)
                pygame.draw.circle(self.screen,color_dict[rarity],(130*self.screen_size,450*self.screen_size),(i-25)*self.screen_size,3*self.screen_size)
            if rarity >= 4:
                if i >= 108:
                    pygame.draw.circle(self.screen, (240,248,255) ,(180*self.screen_size,320*self.screen_size),(25+(i-108)*last_speed_dict[rarity])*self.screen_size,0) # 画面全体を白く塗りつぶす
            if rarity == 5:
                if i >= 144:
                    pygame.draw.circle(self.screen, (240,248,255) ,(45*self.screen_size,130*self.screen_size),(25+(i-144)*last_speed_dict[rarity])*self.screen_size,0) # 画面全体を白く塗りつぶす
                    pygame.draw.circle(self.screen, (240,248,255) ,(210*self.screen_size,60*self.screen_size),(25+(i-144)*last_speed_dict[rarity])*self.screen_size,0) # 画面全体を白く塗りつぶす
                    pygame.draw.circle(self.screen, (240,248,255) ,(300*self.screen_size,220*self.screen_size),(25+(i-144)*last_speed_dict[rarity])*self.screen_size,0) # 画面全体を白く塗りつぶす
                    pygame.draw.circle(self.screen, (240,248,255) ,(315*self.screen_size,510*self.screen_size),(25+(i-144)*last_speed_dict[rarity])*self.screen_size,0) # 画面全体を白く塗りつぶす
                    pygame.draw.circle(self.screen, (240,248,255) ,(150*self.screen_size,580*self.screen_size),(25+(i-144)*last_speed_dict[rarity])*self.screen_size,0) # 画面全体を白く塗りつぶす
                    pygame.draw.circle(self.screen, (240,248,255) ,(60*self.screen_size,420*self.screen_size),(25+(i-144)*last_speed_dict[rarity])*self.screen_size,0) # 画面全体を白く塗りつぶす
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
        self.paper_img = pygame.image.load("./new_system/mypj3/img/paper.png")
        self.paper_img = pygame.transform.rotozoom(self.paper_img, 0, self.screen_size)
        self.screen.blit(self.paper_img,Rect(0,0,360*self.screen_size,640*self.screen_size))
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
            self.ans_g = [0, 2, 4, 7, 9]
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
        # 「ダンジョンへ行く」状態でワールドマップなので、これで初期化する。
        # 街いに行きたいときも、「ダンジョンへ行く」よりも「街へ行く」のほうが優先度が高いので、
        # 街へ行く条件を満たすように設定すれば「ダンジョンへ行く」よりも優先されるため問題はない。
        self.choice_dict["街へ行く"] = {"number":1,"name":"ダンジョンへ行く"}
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
        if auto_page_grouping == "on":
            choice_qty = len(choice)
            page_qty = math.ceil(choice_qty/6)
            if choice_qty <= 6:
                self.choice_screen(title,choice, message, dict_name, delete_dict_list_when_return)
                return
            else:
                choice = self.arrange_choice_list(choice)
        else:
            page_qty = len(choice)
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

    def message_screen(self,message,fontsize:str = "large"):
        """メッセーのみを表示したいときに使うモジュール
        メッセージは自動改行される
        リスト化すると、文中でも改行ができる。
        fontsizeはmiddleかlargeの二択
        """
        if type(message) == str:
            self.message_screen_single(message,fontsize)
        elif type(message) == list:
            for i, line in enumerate(message):
                self.message_screen_single(line,fontsize,i)
            

    def message_screen_single(self, message:str,fontsize:str = "large",row_pos:int=0):
        self.choice_buttonrect = []
        choice_answer = False
        font_title = pygame.font.SysFont(
            "bizudminchomediumbizudpminchomediumtruetype", 26*self.screen_size)
        font = pygame.font.SysFont(
            "bizudminchomediumbizudpminchomediumtruetype", 21*self.screen_size)
        font2 = pygame.font.SysFont(
            "bizudminchomediumbizudpminchomediumtruetype", 16*self.screen_size)
        # 自動改行
        if fontsize == "middle":
            message = str(message)
            text_list = self.line_break(message, 32)
            for i, name in enumerate(text_list):
                print_message = font.render(name, True, "WHITE")
                self.screen.blit(
                    print_message, (11*self.screen_size, (100+27*(i+row_pos))*self.screen_size))
            self.screen.blit(self.return_button_img, self.return_buttonrect)

        else:
            message = str(message)
            text_list = self.line_break(message, 24)
            for i, name in enumerate(text_list):
                print_message = font_title.render(name, True, "WHITE")
                self.screen.blit(
                    print_message, (18*self.screen_size, (100+34*(i+row_pos))*self.screen_size))
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
            

    def damage_effect(self,mode="normal",count=2,period=0.1):
        
        self.enemyrect_move = Rect(180*self.screen_size-int(self.enemy_list[self.dungeon_num].get_width()/2), 70*self.screen_size,187*self.screen_size, 250*self.screen_size)
        if mode != "boss":
            pygame.mixer.Channel(0).play(
                pygame.mixer.Sound(self.se_dict["attack"]))
        for i in range(count):
            for i in range(2):
                self.screen.blit(self.enemy_list[self.dungeon_num],self.enemyrect_move)
                pygame.display.update()
                time.sleep(period)
                self.screen.blit(self.enemy_list[self.dungeon_num],self.enemyrect[self.dungeon_num])
                pygame.display.update()
                time.sleep(period)

    def show_map(self):
        self.world_map_image = pygame.image.load("./new_system/mypj3/img/world_map.jpg")
        self.world_map_image = pygame.transform.rotozoom(self.world_map_image, 0, self.screen_size)
        self.screen.blit(self.world_map_image,(0,0))
        self.arrow_image = pygame.image.load("./new_system/mypj3/img/arrow.png").convert_alpha()
        self.arrow_image = pygame.transform.rotozoom(self.arrow_image, 0, self.screen_size)
        self.stage_range_image = pygame.image.load("./new_system/mypj3/img/rect_70.png").convert_alpha()
        self.stage_range_image = pygame.transform.rotozoom(self.stage_range_image, 0, self.screen_size)
        self.show_allow()

    def show_allow(self):
        """現在の一番進んでいるステージ番号をエクセルから取得し、そのステージまでの矢印と当たり判定を追加する関数。
        画面上表示がarrow、当たり判定はrect、位置が異なるので注意"""

        # 透過処理のやり方(備忘録）
        # まず、画像を透過処理する（ウェブサイトでできる）
        # 画像を読み込むとき（パスを書く行）、最後に.convert_alpha()をつける

        # stage_position_dict:{ステージ番号:タップポイントの中心座標}
        # ステージ0は街
        self.frontier_stage_id = min(int(self.vlookup(self.mysheet,"frontier",2)),15)
        self.stage_rect_dict_360p = {0:(93,566),1:(190,577),2:(280,503),3:(260,417),4:(255,332),5:(270,246),6:(166,263),7:(168,368),8:(91,430),9:(53,340),10:(67,253),
        11:(90,160),12:(51,75),13:(176,51),14:(268,62),15:(319,146)}
        self.stage_arrow_dict={}
        self.stage_buttonrect = [0 for i in range(16)]
        self.stage_type_dict = {"normal":1,"boss":2}
        for stage_id in range(self.frontier_stage_id+1):
            # arrowの「左上」位置を、ステージ選択のタップ判定の「中央」位置から左に11、上に48の位置に設定する
            for i in range(len(self.stage_rect_dict_360p)):
                self.stage_arrow_dict[i] = ((self.stage_rect_dict_360p[i][0]-11)*self.screen_size,(self.stage_rect_dict_360p[i][1]-48)*self.screen_size)
            self.screen.blit(self.arrow_image,self.stage_arrow_dict[stage_id])
            # print([(self.stage_rect_dict_360p[stage_id][0]-40)*self.screen_size, (self.stage_rect_dict_360p[stage_id][1]-40)*self.screen_size])
            self.stage_buttonrect[stage_id] = Rect((self.stage_rect_dict_360p[stage_id][0]-35)*self.screen_size, (self.stage_rect_dict_360p[stage_id][1]-35)*self.screen_size, 70*self.screen_size, 70*self.screen_size)
            # 当たり判定を表示
            if self.demand[5] >= 2:
                self.screen.blit(self.stage_range_image,((self.stage_rect_dict_360p[stage_id][0]-35)*self.screen_size,(self.stage_rect_dict_360p[stage_id][1]-35)*self.screen_size))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
                for stage_id in range(self.frontier_stage_id+1):
                    if self.stage_buttonrect[stage_id].collidepoint(event.pos):
                        pygame.mixer.Channel(0).play(pygame.mixer.Sound(self.se_dict["start"]))
                        print(stage_id)
                        self.dungeon_num = stage_id
                        self.map_judge = 1
                        if stage_id != 0:
                            self.dungeon_type = self.vhlookup(self.book["ダンジョン"],"type",1,str(self.dungeon_num),1)
                            self.gamescene = self.stage_type_dict[self.dungeon_type]
                            self.stage_select_effect()
                        return
        return