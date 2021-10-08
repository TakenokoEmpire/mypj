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
        self.dict_name_list = ["初期画面", "街の選択", "装備部位選択", "装備詳細選択"]
        # ↑【重要】選択肢を使う場合、そのdict_nameは必ずこのリストにいれる
        self.choice_dict_initialize()

        pygame.mixer.music.load(self.bgm_dict["home"])
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(loops=-1)
        while self.running:
            self.screen.fill((0, 0, 0))
            """「選択肢」の使い方
            まず、self.dict_name_listに【選択肢の名称】を追加
            次に、「if self.choice_dict["装備"]["number"] == False:」の["装備"]を、【選択肢の名称】に変更する
            最後に、self.choice_screenの最後の引数に【選択肢の名称】を入力する。
            選択結果は、self.choice_dictに保存される。

            何かおかしいと思ったら、
            ・self.dict_name_listに【選択肢の名称】を追加したか
            ・3箇所の【選択肢の名称】が全て同じであるか
            ・dict検索時のnumberとnameを間違えてないか
            をチェック
            """
            if self.choice_dict["初期画面"]["name"] == False:
                # if self.choice_dict["初期画面"]["number"] == False:
                self.choice_screen("<Hit and blow タイトル画面>", ["街へ行く", "ダンジョンへ行く"], [
                    "街へ行く：装備の調整", "ダンジョンへ行く：モンスターバトル"], "初期画面")
                run_count_town = [0, 0, 0, 0, 0, 0, 0]

            elif self.choice_dict["初期画面"]["name"] == "街へ行く":
                if self.choice_dict["街の選択"]["number"] == False:
                    if run_count_town[0] == 0:
                        self.second_init_battle("town")
                        run_count_town[0] += 1
                    self.choice_screen(
                        "何をする？", ["クエスト", "ステータスチェック", "スキル", "装備", "アイテム", "ショップ",  "セーブして戻る"], ["「装備」のみ対応"], "街の選択")
                elif self.choice_dict["街の選択"]["name"] == "装備" and self.choice_dict["装備部位選択"]["number"] == False:
                    # 装備の情報更新
                    if run_count_town[1] == 0:
                        self.equip_checker()
                        # equip_list = []
                        rest = town.Town()
                        current_equip_list = rest.town_equip1()
                        print(current_equip_list)
                        run_count_town[1] += 1
                    self.choice_screen(
                        "どの部位を変更する？", current_equip_list, ["「右手」のみ対応", "ここに現在の装備の情報を表示させたい"], "装備部位選択")
                elif self.choice_dict["装備部位選択"]["number"] != False and self.choice_dict["装備詳細選択"]["number"] == False:
                    choice_position = self.choice_dict["装備部位選択"]["number"]
                    s_pos = self.hindex(self.book["装備"], "position")
                    s_name = self.hindex(self.book["装備"], "name")
                    s_qty = self.hindex(self.book["装備"], "qty")
                    self.choice_screen(
                        "どの装備と変更する？", ["右手", "左手", "鎧", "靴", "装飾品"], ["ここに現在の装備の情報を表示させたい"], "装備詳細選択")
                elif self.choice_dict["装備詳細選択"]["number"] != False:
                    delete_list = ["街の選択", "装備部位選択", "装備詳細選択"]
                    for i in delete_list:
                        self.choice_dict[i]["number"] = False
                        self.choice_dict[i]["name"] = False

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
                    run_count = [0, 0, 0, 0, 0, 0, 0]
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
                    if run_count[1] == 0:
                        print("second_init")
                        # 各戦闘毎に一回のみ動作させたい
                        self.second_init_battle()
                        self.second_init_showgame()
                        self.status_printer()
                        run_count[1] += 1
                    self.normal_stage()
                    self.normal_stage_judge()

                elif self.gamescene == 2:  # Boss Stage
                    if run_count[2] == 0:
                        self.second_init_battle()
                        self.second_init_showgame()
                        run_count[2] += 1
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
                    if run_count[4] == 0:
                        print("VICTORY!!")
                        self.win()
                        run_count[4] += 1
                    self.clear()
                    self.result_judge()

            pygame.display.update()  # スクリーン上のものを書き換えた時にはupdateが必要


def automation_test():
    woven = City()
    woven.city_run()


class City(show_game4.ShowGame):

    def __init__(self):
        super().__init__()

    def city_run(self):
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
                self.dict_name_list = ["装備", "装備2"]
                # ↑【重要】選択肢を使う場合、そのdict_nameは必ずこのリストにいれる
                self.choice_dict_initialize()
                self.reset()
                self.home_show()
                self.home_judge()
            elif self.gamescene == 5:  # how to play
                self.how_to_play()
                self.how_to_play_judje()
            elif self.dungeon_num == 0:
                """「選択肢」の使い方
                まず、self.dict_name_listに【選択肢の名称】を追加
                次に、「if self.choice_dict["装備"]["number"] == False:」の["装備"]を、【選択肢の名称】に変更する
                最後に、self.choice_screenの最後の引数に【選択肢の名称】を入力する。
                選択結果は、self.choice_dictに保存される。
                何かおかしいと思ったら、
                ・self.dict_name_listに【選択肢の名称】を追加したか
                ・3箇所の【選択肢の名称】が全て同じであるか
                をチェック
                """
                if self.choice_dict["装備"]["number"] == False:
                    self.choice_screen(
                        "全角で最大２８文字まで入力可能で、１５字目以降は自動改行される", ["木の剣 ATK+10", "鉄の剣：ATK+25", "鉄の剣",
                                                            "鉄の剣", "鉄の剣", "鉄の剣", "選択肢は最大7つまで"], ["現在装備：木の剣(攻撃力+10,防御力+0)",
                                                                                                 "攻撃力：25(+15)、防御力：0(+0)", "あ", "あ", "メッセージは最大5行まで"], "装備")
                elif self.choice_dict["装備2"]["number"] == False:
                    self.choice_screen(
                        "装備変更するぞ", ["木の剣 ATK+10", "鉄の剣：ATK+25", "選択肢は最大7つまで"], ["現在装備：木の剣(攻撃力+10,防御力+0)", "メッセージは最大5行まで"], "装備2")
                else:

                    rest = town.Town()
                    rest.town_status()
                    print("a")
                    time.sleep(1)

                # self.judge_choice_screen()

            pygame.display.update()  # スクリーン上のものを書き換えた時にはupdateが必要


def system_run():
    # システム起動後にターミナルに入力すると、ゲーム画面が前面に表示されなくなる
    print("1:街")
    print("2:ダンジョン（現在、gui経由以外では使用不可）")
    print("3:gui")
    print("4:自動化テスト")
    print("9:データ削除")
    # choice = input("どこ行く？->")
    choice = "3"
    if choice == "1":
        rest = town.Town()
        rest.main()

    if choice == "2":
        # dungeon_type = input("choose dungeon type [boss/normal] ->")
        # dungeon_num = input("choose dungeon number ->")
        # vs = battle.Battle(dungeon_type, int(dungeon_num))
        vs = battle.Battle()
        vs.main()

    if choice == "3":
        gui_title()

    if choice == "4":
        automation_test()

    if choice == "9":
        delete = initialize.Initialize()
        delete.confirm()


system_run()

# Rect(ボタンの位置とサイズ)
# screen.blit→指定された位置に画像を表示


# def __init__(self, dungeon_type, dungeon_num):
#     super().__init__(dungeon_type, dungeon_num)
