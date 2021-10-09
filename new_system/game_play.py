from systems import initialize
from systems import town
from systems import battle

import random
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

    # def choice_command(self, *cond):
    #     cond_qty = len(cond)
    #     for i in range(cond_qty):
    #         if self.choice_dict([cond[i][0]][cond[i][1]] == cond[i][2]):
    #             return True
    #         else:
    #             return False

    def gui_run(self):
        pygame.display.set_caption("Hit, Blow and Dragons")
        self.set_sound()
        # choice関連
        self.dict_name_list = ["初期画面", "街の入り口", "装備：変更対象",
                               "装備：手持ち", "ショップ画面", "ショップ確認画面", "ガチャ画面", "ガチャ確認画面", "クエスト画面", "クエスト確認画面", "テンプレ画面", "テンプレ確認画面", ]
        # ↑【重要】選択肢を使う場合、そのdict_nameは必ずこのリストにいれる
        self.choice_dict_initialize()

        pygame.mixer.music.load(self.bgm_dict["home"])
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(loops=-1)
        while self.running:
            self.screen.fill((0, 0, 0))
            """「選択肢」の使い方
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
            if self.screen_count == 0:
                self.screen_select()
            elif self.choice_dict["初期画面"]["name"] == "False":
                self.reset()
                # if self.choice_dict["初期画面"]["number"] == "False":
                self.choice_screen("<Hit and blow タイトル画面>", ["街へ行く", "ダンジョンへ行く"], [
                    "街へ行く：装備の調整", "ダンジョンへ行く：モンスターバトル"], "初期画面")
                self.run_count_town = [0, 0, 0, 0, 0, 0, 0]
                self.run_count_battle = [0, 0, 0, 0, 0, 0, 0]

            elif self.choice_dict["初期画面"]["name"] == "街へ行く":
                if self.choice_dict["街の入り口"]["number"] == "False":
                    self.choice_screen(
                        "何をする？", ["ステータス・アイテムチェック",  "装備",  "ショップ",  "ガチャ", "クエスト", "テンプレ"], ["「装備」のみ対応", "", "", "3", "3", "6", "3777777777777777777", "688888888888888"], "街の入り口")

                elif self.choice_dict["街の入り口"]["name"] == "ステータス・アイテムチェック":
                    self.town_status()
                    self.init_town_info()

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
                    self.init_town_info()

                    # アイテム購入と装備購入で複数選択肢を作りたい
                elif self.choice_dict["街の入り口"]["name"] == "ショップ" and self.choice_dict["ショップ画面"]["number"] == "False":
                    self.choice_screen(
                        "ショップ", ["薬草", "回復薬", "ハイポーション", "叡智の実", "妨害の笛"], ["薬草:10G　HPを30回復する", "回復薬：100G　HPを100回復する", "ハイポーション:500G HPを300回復する", "叡智の実:250G 選択肢を4色から3色にする", "妨害の笛:1000G　敵BOSSの調査を1度だけ妨害する"], "ショップ画面")
                elif self.choice_dict["ショップ画面"]["name"] != "False" and self.choice_dict["ショップ確認画面"]["name"] == "False":
                    self.choice_screen(
                        "本当に{}を買いますか？".format(self.choice_dict["ショップ画面"]["name"]), ["はい", "いいえ"], [""], "ショップ確認画面", ["ショップ画面"])
                elif self.choice_dict["ショップ確認画面"]["name"] == "はい":
                    print("{}を購入".format(self.choice_dict["ショップ画面"]["name"]))
                    self.choice_dict["ショップ確認画面"] = {
                        "number": "False", "name": "False"}
                    self.choice_dict["ショップ画面"] = {
                        "number": "False", "name": "False"}
                elif self.choice_dict["ショップ確認画面"]["name"] == "いいえ":
                    self.choice_dict["ショップ確認画面"] = {
                        "number": "False", "name": "False"}
                    self.choice_dict["ショップ画面"] = {
                        "number": "False", "name": "False"}

                elif self.choice_dict["街の入り口"]["name"] == "クエスト" and self.choice_dict["クエスト画面"]["number"] == "False":
                    self.choice_screen(
                        "クエスト", ["装備の錆取り", "ゴブリン討伐依頼", "最高の豚肉を求めて", "城壁の修復", "古龍の足跡"], ["クエスト詳細をここに表示"], "クエスト画面")
                elif self.choice_dict["クエスト画面"]["name"] != "False" and self.choice_dict["クエスト確認画面"]["name"] == "False":
                    self.choice_screen(
                        "クエスト：{}を受諾しますか？".format(self.choice_dict["クエスト画面"]["name"]), ["はい", "いいえ"], ["ここにクエストの条件・報酬・ストーリーを表示"], "クエスト確認画面", ["クエスト画面"])
                elif self.choice_dict["クエスト確認画面"]["name"] == "はい":
                    print("{}を受諾".format(self.choice_dict["クエスト画面"]["name"]))
                    self.choice_dict["クエスト確認画面"] = {
                        "number": "False", "name": "False"}
                    self.choice_dict["クエスト画面"] = {
                        "number": "False", "name": "False"}
                elif self.choice_dict["クエスト確認画面"]["name"] == "いいえ":
                    self.choice_dict["クエスト確認画面"] = {
                        "number": "False", "name": "False"}
                    self.choice_dict["クエスト画面"] = {
                        "number": "False", "name": "False"}

                elif self.choice_dict["街の入り口"]["name"] == "ガチャ" and self.choice_dict["ガチャ画面"]["number"] == "False":
                    self.choice_screen(
                        "ガチャ", ["【期間限定】ハロウィンガチャ", "スーパーガチャ", "ノーマルガチャ"], ["【期間限定】ハロウィンガチャ：¥300", "10/31までの期間限定。ハロウィン装備を手に入れろ！", "フルセットで揃えると…？",
                                                                          "スーパーガチャ：¥100", "限定装備や限定素材が盛りだくさん！", "ノーマルガチャ", "ゲーム内通貨で回せるお得なガチャ"], "ガチャ画面")
                elif self.choice_dict["ガチャ画面"]["name"] != "False" and self.choice_dict["ガチャ確認画面"]["name"] == "False":
                    self.choice_screen(
                        "本当に{}を買いますか？".format(self.choice_dict["ガチャ画面"]["name"]), ["はい", "いいえ"], [""], "ガチャ確認画面", ["ガチャ画面"])
                    atodekesu_count = 0
                elif self.choice_dict["ガチャ確認画面"]["name"] == "はい":
                    if atodekesu_count == 0:
                        print("{}を回した！".format(
                            self.choice_dict["ガチャ画面"]["name"]))
                        print(self.book["ガチャ"])
                        print(self.choice_dict["ガチャ画面"]["name"])
                        item_rarity, selected_item = self.gacha(self.book["ガチャ"],
                                                                self.choice_dict["ガチャ画面"]["name"])
                        print("{}:{}を手に入れた！".format(
                            selected_item, item_rarity))
                        atodekesu_count += 1
                    self.choice_screen(
                        "演出画面、RETURNで戻る".format(self.choice_dict["ガチャ画面"]["name"]), [""], [""], "ガチャ確認画面", ["ガチャ画面", "ガチャ確認画面"])
                elif self.choice_dict["ガチャ確認画面"]["name"] == "いいえ":
                    self.choice_dict["ガチャ確認画面"] = {
                        "number": "False", "name": "False"}
                    self.choice_dict["ガチャ画面"] = {
                        "number": "False", "name": "False"}

                elif self.choice_dict["街の入り口"]["name"] == "テンプレ" and self.choice_dict["テンプレ画面"]["number"] == "False":
                    self.choice_screen(
                        "テンプレ", ["【期間限定】ハロウィンテンプレ：¥300", "スーパーテンプレ：¥300", "ノーマルテンプレ：500G"], ["ハロウィン装備を入手できるのは今だけ！"], "テンプレ画面")
                elif self.choice_dict["テンプレ画面"]["name"] != "False" and self.choice_dict["テンプレ確認画面"]["name"] == "False":
                    self.choice_screen(
                        "本当に{}を買いますか？".format(self.choice_dict["テンプレ画面"]["name"]), ["はい", "いいえ"], [""], "テンプレ確認画面", ["テンプレ画面"])
                elif self.choice_dict["テンプレ確認画面"]["name"] == "はい":
                    print("{}を購入".format(self.choice_dict["テンプレ画面"]["name"]))
                    self.choice_dict["テンプレ確認画面"] = {
                        "number": "False", "name": "False"}
                    self.choice_dict["テンプレ画面"] = {
                        "number": "False", "name": "False"}
                elif self.choice_dict["テンプレ確認画面"]["name"] == "いいえ":
                    self.choice_dict["テンプレ確認画面"] = {
                        "number": "False", "name": "False"}
                    self.choice_dict["テンプレ画面"] = {
                        "number": "False", "name": "False"}
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
                    self.boss_action()

                elif self.gamescene == 2:  # Boss Stage
                    if self.run_count_battle[2] == 0:
                        # ロード画面を挿入するならココ
                        # ↓autoplayもやってくれる
                        self.dungeon_init()
                        self.boss_history = self.hist[1]
                        print(self.boss_history)
                        self.second_init_showgame()
                        self.run_count_battle[2] += 1
                    if self.switch_judge("turn_switch", self.turn_switch, 0) == True:
                        if self.jamming_judge("player") == "stop":
                            print("調査を妨害された！")
                            time.sleep(1)
                            self.boss_action("boss")

                    self.turn_switch = 0

                    self.normal_stage("boss")
                    self.normal_stage_judge("boss")
                    # for event in pygame.event.get():
                    #     if event.type == pygame.QUIT:
                    #         self.running = False
                    #     if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
                    #         if self.return_buttonrect.collidepoint(event.pos):
                    #             self.gamescene = 0

                elif self.gamescene == 3:  # game over
                    # システム側では特に何もしない
                    if self.run_count_battle[3] == 0:
                        print("You lose...")
                        self.run_count_battle[3] += 1
                    self.game_over()
                    self.result_judge()

                elif self.gamescene == 4:
                    if self.run_count_battle[4] == 0:
                        print("VICTORY!!")
                        self.win()
                        self.run_count_battle[4] += 1
                    self.clear()
                    self.result_judge()

                if self.switch_judge("gamescene", self.gamescene, 0) == True:
                    self.init_battle_info()

            pygame.display.update()  # スクリーン上のものを書き換えた時にはupdateが必要

    def init_town_info(self):
        """街の入り口に戻る
        「初期画面」以外のdict_name情報は（戦闘関連も含めて）すべて初期化される"""
        init_list = self.dict_name_list[1:]
        for i in init_list:
            self.choice_dict[i]["number"] = "False"
            self.choice_dict[i]["name"] = "False"
        self.run_count_town = [0, 0, 0, 0, 0, 0, 0]

    def init_battle_info(self):
        self.run_count_battle = [0, 0, 0, 0, 0, 0, 0]
        self.turn_switch = 0


class Debug(Commander):

    def __init__(self):
        super().__init__()

    def hlookup_plus(self, sheet, index, row_order, top_index_position):
        """excelのhlookup関数を再現。
        スタート位置をずらせる
        """
        for i in range(10):
            output = 0
            if str(sheet.cell(row=top_index_position, column=i+1).value) == index:
                output = sheet.cell(
                    row=row_order+top_index_position-1, column=i+1).value
                return output
        return False

    def debug(self):
        rand = random.random()
        top_index_position = self.vindex(self.book["ガチャ"], "ノーマルガチャ")
        # gacha_qty = self.vlookup(sheet, gachaname, 2)
        print(self.vlookup_plus(
            self.book["プレイヤーステータス"], "鋼鉄の剣", 3, 2))

        # for i in range(gacha_qty):
        #     print(self.hlookup_plus(sheet, "sum_prob", i+1, top_index_position))
        #     if rand < float(self.hlookup_plus(sheet, "sum_prob", i+1, top_index_position)):
        #         selected_item = self.hlookup_plus(
        #             sheet, "content", i+1, top_index_position)
        # return(selected_item)


def system_run():
    # システム起動後にターミナルに入力すると、ゲーム画面が前面に表示されなくなる
    print("1:街")
    print("2:ダンジョン（現在、gui経由以外では使用不可）")
    print("3:gui")
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
        vs = battle.Battle("console")
        vs.main()

    if choice == "3":
        gui_title()

    if choice == "4":
        deb = Debug()
        deb.debug()

    if choice == "9":
        delete = initialize.Initialize()
        delete.confirm()


system_run()

# Rect(ボタンの位置とサイズ)
# screen.blit→指定された位置に画像を表示


# def __init__(self, dungeon_type, dungeon_num):
#     super().__init__(dungeon_type, dungeon_num)
