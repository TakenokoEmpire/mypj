from systems import initialize
from systems import town
from systems import battle

import pygame
from pygame import Surface, mixer
from pygame.locals import *
from typing import List, Tuple
import time
# from mypj3.game_number_guess import NumberGuess
import sys
import systems
from systems import show_game4


# gui = show_game3.ShowGame(demand=0, gamescene=0, dungeon_num=0)
pygame.init()
mixer.init()
# numberguess = mypj3.game_number_guess.NumberGuess()


def gui_title():
    display = Commander()
    # vs = battle.Battle()
    display.gui_run()


# def __init__(self, dungeon_type, dungeon_num):
#     super().__init__(dungeon_type, dungeon_num)

class Commander(show_game4.ShowGame):

    def __init__(self):
        super().__init__()
        self.place = "entrance"

    def gui_run(self):
        pygame.display.set_caption("Hit, Blow and Dragons")
        self.set_player()
        self.set_mark()
        self.set_enemy()
        self.set_button()
        self.set_mark_entry()
        self.set_sound()
        # choice関連
        self.dict_name_list = ["初期画面", "街の入り口", "装備：変更対象", "装備：手持ち"]
        # ↑【重要】選択肢を使う場合、そのdict_nameは必ずこのリストにいれる
        self.choice_dict_initialize()

        pygame.mixer.music.load(self.bgm_dict["home"])
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(loops=-1)
        while self.running:
            self.screen.fill((0, 0, 0))
            """「選択肢」の使い方
            まず、self.dict_name_listに【選択肢の名称】を追加
            次に、「if self.choice_dict["装備"]["number"] == "False":」の["装備"]を、【選択肢の名称】に変更する
            さらに、self.choice_screenの最後の引数に【選択肢の名称】を入力する。
            【10/8-14:30追加】：「RETURN」ボタンを押した際に、削除するべき｛ 前 の 選択肢の名称｝を決定する(設定がなければ、ホーム画面に戻る)
            選択結果は、self.choice_dictに保存される。

            何かおかしいと思ったら、
            ・self.dict_name_listに【選択肢の名称】を追加したか
            ・3箇所の【選択肢の名称】が全て同じであるか
            ・dict検索時のnumberとnameを間違えてないか
            をチェック
            """
            if self.choice_dict["初期画面"]["name"] == "False":
                self.reset()
                # if self.choice_dict["初期画面"]["number"] == "False":
                self.choice_screen("<Hit and blow タイトル画面>", ["街へ行く", "ダンジョンへ行く"], [
                    "街へ行く：装備の調整", "ダンジョンへ行く：モンスターバトル"], "初期画面")
                self.run_count_town = [0, 0, 0, 0, 0, 0, 0]
                self.run_count_battle = [0, 0, 0, 0, 0, 0, 0]

            elif self.choice_dict["初期画面"]["name"] == "街へ行く":
                if self.choice_dict["街の入り口"]["number"] == "False":
                    self.choice_screen(
                        "何をする？", ["クエスト", "ステータスチェック", "スキル", "装備", "アイテム", "ショップ",  "セーブして戻る"], ["「装備」のみ対応"], "街の入り口")
                # 装備変更
                elif self.choice_dict["街の入り口"]["name"] == "装備" and self.choice_dict["装備：変更対象"]["number"] == "False":
                    # 装備の情報更新
                    if self.run_count_town[1] == 0:
                        self.equip_checker()
                        # equip_list = []
                        print(self.basic_status_index)
                        position_choice_list, position_detail_list = self.town_equip1()
                        # print(current_equip_list)
                        self.run_count_town[1] += 1
                    self.choice_screen(
                        "どの部位を変更する？", position_choice_list, position_detail_list, "装備：変更対象", ["街の入り口"])
                elif self.choice_dict["装備：変更対象"]["number"] != "False" and self.choice_dict["装備：手持ち"]["number"] == "False":
                    equip_list = self.town_equip2(
                        self.choice_dict["装備：変更対象"]["number"])
                    self.choice_screen(
                        self.choice_dict["装備：手持ち"]["number"], equip_list, ["ここに現在の装備の情報を表示させたい"], "装備：手持ち", ["装備：変更対象"])
                elif self.choice_dict["装備：手持ち"]["number"] != "False":
                    self.town_equip3(
                        self.choice_dict["装備：変更対象"]["number"], equip_list, self.choice_dict["装備：手持ち"]["number"])
                    self.init_choice_info()

            elif self.choice_dict["初期画面"]["name"] == "ダンジョンへ行く":
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
                elif self.dungeon_num == 0:
                    self.stage_select()
                    self.judge_stage_select()

                elif self.gamescene == 1:  # Normal Stage
                    if self.run_count_battle[1] == 0:
                        print("second_init")
                        print(self.gamescene)
                        # 各戦闘毎に一回のみ動作させたい

                        self.dungeon_init()
                        self.second_init_showgame()
                        self.print_status()
                        self.run_count_battle[1] += 1
                    self.normal_stage()
                    self.normal_stage_judge()

                elif self.gamescene == 2:  # Boss Stage
                    if self.run_count_battle[2] == 0:
                        self.dungeon_init(self.gamescene, self.dungeon_num)
                        self.second_init_showgame()
                        self.run_count_battle[2] += 1
                    self.boss_stage()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.running = False
                        if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
                            if self.return_buttonrect.collidepoint(event.pos):
                                self.gamescene = 0

                elif self.gamescene == 3:  # game over
                    # システム側では特に何もしない
                    print("YOU LOSE...")
                    self.game_over()
                    self.result_judge()

                elif self.gamescene == 4:
                    if self.run_count_battle[4] == 0:
                        print("VICTORY!!")
                        self.win()
                        self.run_count_battle[4] += 1
                    self.clear()
                    self.result_judge()

                if self.switch_judge(self.gamescene, 0) == True:
                    self.init_battle_info()

            pygame.display.update()  # スクリーン上のものを書き換えた時にはupdateが必要

    def init_town_info(self):
        init_list = ["街の入り口", "装備：変更対象", "装備：手持ち"]
        for i in init_list:
            self.choice_dict[i]["number"] = "False"
            self.choice_dict[i]["name"] = "False"
        self.run_count_town = [0, 0, 0, 0, 0, 0, 0]

    def init_battle_info(self):
        self.run_count_battle = [0, 0, 0, 0, 0, 0, 0]


def system_run():
    # システム起動後にターミナルに入力すると、ゲーム画面が前面に表示されなくなる
    print("1:街")
    print("2:ダンジョン（現在、gui経由以外では使用不可）")
    print("3:gui")
    print("9:データ削除")
    choice = input("どこ行く？->")
    # choice = "3"
    if choice == "1":
        rest = town.Town()
        rest.main()

    if choice == "2":
        # dungeon_type = input("choose dungeon type [boss/normal] ->")
        # dungeon_num = input("choose dungeon number ->")
        # vs = battle.Battle(dungeon_type, int(dungeon_num))
        vs = battle.Battle("console")
        vs.main()

    if choice == "3":
        gui_title()

    if choice == "9":
        delete = initialize.Initialize()
        delete.confirm()


system_run()

# Rect(ボタンの位置とサイズ)
# screen.blit→指定された位置に画像を表示


# def __init__(self, dungeon_type, dungeon_num):
#     super().__init__(dungeon_type, dungeon_num)
