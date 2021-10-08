import openpyxl
import pprint
import random
import math
import copy
from systems import judge_manual
import try_1003
import send_recieve
# from systems import testtry

"""よくやるミス
self忘れ
=と==
関数の()
"""

"""
やること
runにまとめる
通常戦：（単発のhitblowで終わらない場合）→とき終わったら、再度答えを生成
ボス戦（単発のhitblowで終わらない場合）→どちらかが終わったら、アルゴリズム再起動
"""

"""
やりたいこと
special mode→クリティカル攻撃
"""

"""メモ
ゲーム序盤は2回、中盤は4回、終盤は7回ほどで次のダンジョンに行けるようゲームバランス調整
（慣れれば慣れるほど、解くのが早くなって所要時間が短縮される）
"""


# drun = SendReceive(room_id=room)

# room_id:Optional[int]=None,
# self.room_id = room_id

class Function():
    def __init__(self):
        pass

    def vlookup(self, sheet, index, column_order):
        """excelのvlookup関数を再現。
        先頭行・列からスタートで固定"""
        for i in range(500):
            output = 0
            if str(sheet.cell(row=i + 1, column=1).value) == index:
                output = sheet.cell(row=i+1, column=column_order).value
                return output
        return False

    def vlookup_plus(self, sheet, index, column_order, left_index_position):
        """excelのvlookup関数を再現。
        スタート位置をずらせる
        """
        for i in range(500):
            output = 0
            if str(sheet.cell(row=i + 1, column=left_index_position).value) == index:
                output = sheet.cell(
                    row=i+1, column=left_index_position+column_order-1).value
                return output
        return False

    def hlookup(self, sheet, index, row_order):
        """excelのhlookup関数を再現
        先頭行・列からスタートで固定"""
        for i in range(100):
            output = 0
            if str(sheet.cell(row=i + 1, column=1).value) == index:
                output = sheet.cell(row=row_order, column=i+1).value
                return output
        return False

    def vhlookup(self, sheet, left_index, left_index_position, top_index, top_index_position):
        """excelの、vlookup関数とhlookup関数を組み合わせた関数
        indexとmatchを組み合わせて作るアレ
        動作未確認
        """
        for i in range(500):
            if str(sheet.cell(row=i + top_index_position, column=left_index_position).value) == left_index:
                for j in range(100):
                    if str(sheet.cell(row=top_index_position, column=j+left_index_position).value) == top_index:
                        return sheet.cell(row=i+top_index_position, column=j+left_index_position).value
        return False

    def vindex(self, sheet, index):
        """excelのindex関数もどきを再現
        該当する文字がある行番号を返す（先頭列に限る）"""
        for i in range(500):
            output = 0
            if str(sheet.cell(row=i + 1, column=1).value) == index:
                return i + 1
        return False

    def hindex(self, sheet, index):
        """excelのindex関数もどきを再現
        該当する文字がある列番号を返す（先頭行に限る）"""
        for i in range(100):
            output = 0
            if str(sheet.cell(row=1, column=i+1).value) == index:
                return i + 1
        return False

    def xy_index(self, sheet, left_index, left_index_position, top_index, top_index_position, return_type):
        """excelのindex関数もどきを再現
        縦横両方向に対応し、さらに先頭行（列）以外にも対応
        return_type:"excel"→セル番号形式
                    その他→row,column
        """
        for i in range(500):
            output = 0
            if str(sheet.cell(row=i + top_index_position, column=left_index_position).value) == left_index:
                # print("a")
                for j in range(100):
                    #     print(sheet.cell(row=j + 1, column=1).value)
                    #     print(top_index)
                    if str(sheet.cell(row=top_index_position, column=j+left_index_position).value) == top_index:
                        if return_type == "excel":
                            return openpyxl.utils.get_column_letter(j + left_index_position)+str(i + top_index_position)
                        else:
                            return i + top_index_position, j + left_index_position
        return False

    def zero_false(self, x):
        if x == 0:
            return False
        else:
            return True


class Battle(Function):
    """ダメージを入力し、その結果を出力するように子クラスを設計中
    主にエクセルファイルとやり取りする
    """

    def __init__(self):
        # 「プレイヤー」の「レベル」だけダンジョン選択前に必要なので、それだけ先に得る
        self.book = openpyxl.load_workbook('systems/base.xlsx', data_only=True)
        self.mysheet = self.book["プレイヤーステータス"]
        self.lv = [self.vlookup(self.mysheet, "lv", 2), False]
        # for num, sheet in enumerate(self.vs_sheet):
        #     self.lv[0] = self.vlookup(sheet, "lv", 2)

    def second_init_battle(self, place: str = "battle"):
        # GUIに対応
        # ダンジョンに依存するステータス等は、この段階まで待つ必要があるため、
        # 進入ダンジョンが決定する前(initで強制的に実行される内容)と後でself設定を分割する。

        # 戦闘時だけでなく、Townからもここにアクセスする。
        # その場合は、通常ダンジョンのダンジョン番号1にアクセスしたものとして扱う（便宜上、敵も設定する必要がある）
        if place != "battle":
            print("notice: second_init_battle has accessed by safe area")
            self.gamescene = 1
            self.dungeon_num = 1
        dungeon_type_list = ["none", "normal", "boss"]
        self.dungeon_type = dungeon_type_list[self.gamescene]
        self.ans = ["12345", "abcde"]
        self.turn_count = [0, 0]
        self.hist = [[], []]
        self.max_ans = 16
        self.length = 5

        self.mobname = self.vlookup(
            self.choose_dungeon(), str(self.dungeon_num), 3)
        self.mobsheet = self.book[self.mobname]
        self.vs_sheet = [self.mysheet, self.mobsheet]
        if place == "battle":
            print("野生の{}が現れた！".format(self.mobname))

        self.equip_position = ["右手", "左手", "鎧", "靴", "装飾品"]
        self.equip_index_rownum = self.vindex(self.mysheet, "position")
        self.equip_sheetsoubi_name_columnnum = self.hindex(
            self.book["装備"], "name")
        self.equip_qty = self.vlookup(self.mysheet, "equip_qty", 2)

        """
        lv,hp,atk,skill[0]~[2],exp,moneyはリストとなっており、[0]がプレイヤーの値、[1]が敵の値
        """
        self.basic_status_index = ["lv", "hp", "atk"]
        self.status_checker()  # ステータス取得前にステータスを更新しておく
        self.lv = [0, 0]
        self.hp = [0, 0]
        self.atk = [0, 0]
        self.skill = [[0, 0] for j in range(3)]
        self.exp = [0, 0]
        self.money = [0, 0]
        for num, sheet in enumerate(self.vs_sheet):
            self.lv[num] = self.vlookup(sheet, "lv", 2)
            self.hp[num] = self.vlookup(sheet, "hp", 2)
            self.atk[num] = self.vlookup(sheet, "atk", 2)
            for j in range(3):
                self.skill[j][num] = self.vlookup(
                    sheet, "skill{}".format(j), 2)
            self.exp[num] = self.vlookup(sheet, "exp", 2)
            self.money[num] = self.vlookup(sheet, "money", 2)
        self.droplist = []

    def choose_dungeon(self):
        # 小文字化させたい
        while True:
            if self.dungeon_type == "normal":
                return self.book["通常ダンジョン"]
            elif self.dungeon_type == "boss":
                # ボス戦の場合、この段階でアルゴリズムを最後まで回す。
                # なお、16進5桁以外は非対応である。
                self.autoplay()
                return self.book["ボスダンジョン"]
            else:
                self.dungeon_type = "normal"
                print("normalダンジョンに入ります。")
                return self.book["通常ダンジョン"]

    def main(self):
        self.second_init_battle()
        self.status_printer()
        print(self.hist)
        while True:
            if self.my_turn() == "finish":
                break
            if self.mob_turn() == "finish":
                break
            self.end_of_turn()

    def status_checker(self):
        self.equip_checker()
        for stat in self.basic_status_index:
            self.mysheet[self.xy_index(self.mysheet, stat, 1, "total", 1, "excel")] = self.vhlookup(
                self.mysheet, stat, 1, "raw", 1) + self.vhlookup(self.mysheet, stat, 1, "equip", 1)

    def equip_checker(self):
        # 装備欄に登録された名前から、hp,atkの値を「装備」ブックから参照し記録する
        update_stat = ["hp", "atk"]
        sum_stat = [0, 0]
        for i in range(self.equip_qty):
            equip_name = self.vhlookup(
                self.mysheet, self.equip_position[i], 1, "name", self.equip_index_rownum)
            for j in range(len(update_stat)):
                self.mysheet[self.xy_index(self.mysheet, self.equip_position[i], 1, update_stat[j], self.equip_index_rownum, "excel")] = self.vhlookup(
                    self.book["装備"], equip_name, self.equip_sheetsoubi_name_columnnum, update_stat[j], 1)
        # 装備欄に記録されたhp,atkの補正値をステータスに反映する(補正値の合計sum_statを計算し、該当する位置に貼り付ける)
        for j in range(len(update_stat)):
            for i in range(self.equip_qty):
                sum_stat[j] += self.vhlookup(self.mysheet, self.equip_position[i],
                                             1, update_stat[j], self.equip_index_rownum)
            self.mysheet[self.xy_index(
                self.mysheet, update_stat[j], 1, "equip", 1, "excel")] = sum_stat[j]

    def status_printer(self, place: str = "battle"):
        print("my status")
        print("lv,hp,atk,exp")
        print([self.lv[0], self.hp[0], self.atk[0], self.exp[0]])
        # Townで敵情報を表示させないため分離
        if place == "battle":
            print("mob status")
            print("lv,hp,atk,exp")
            print([self.lv[1], self.hp[1], self.atk[1], self.exp[1]])

    def end_of_turn(self):
        if len(self.hist[0]) == min(self.turn_count)-1:
            self.hist[0].append({"guess": "-----", "hit": "0", "blow": "0"})
        elif len(self.hist[0]) == min(self.turn_count):
            pass
        else:
            print("error end_of_turn")
        self.print_history()
        print("残りHP{}".format(self.hp))

        # try:
        #     self.print_out_history()
        # except IndexError:
        #     self.hist[0].append({"guess": "-----", "hit": "0", "blow": "0"})
        #     self.print_out_history()
        # print("残りHP{}".format(self.hp))

    def print_history(self):
        for i in range(min(self.turn_count)):
            if self.dungeon_type == "normal":
                print("turn{}:".format(i) + str(self.hist[0][i]))
            elif self.dungeon_type == "boss":
                print("turn{}:".format(i) +
                      str(self.hist[0][i]) + str(self.hist[1][i]))

    """
    プレイヤーの行動
    """

    def my_turn(self):
        while True:
            self.turn_count[0] += 1
            act = input("0:攻撃,1:スキル,2:アイテム,3:逃げる ->")
            if act == "0":
                if self.jamming_judge() == "stop":
                    return "continue"
                self.hp[1] -= int(self.atk[0] * self.my_atk_ratio())
                if self.hp[1] <= 0:
                    self.win()
                    return "finish"
                else:
                    return "continue"
            else:
                print("未対応です")

    def jamming_judge(self):
        lv_ratio = self.lv[0] / self.lv[1]
        print("level ratio:{}".format(lv_ratio))
        if random.random() > lv_ratio and self.dungeon_type == "boss":
            print("調査を妨害された！")
            return "stop"
        return "go"

    def my_atk_ratio(self):
        # if input("do hit blow? [y/n] ->") == "y":
        while True:
            guess = input("input guess ->")
            if self.guess_checker(guess) == True:
                break
        runner = judge_manual.JudgeManual(
            guess, self.ans[0], self.length, self.max_ans)
        hit, blow = runner.run()
        self.hist[0].append({"guess": guess, "hit": hit, "blow": blow})
        if hit == 5:
            print("必殺の一撃！")
            return 1
        else:
            return hit * 0.1 + blow * 0.05
        #     # ショートカット用。
        # else:
        #     try:
        #         choice = float(input("my atk ratio->"))
        #     except ValueError:
        #         choice = 0
        #     return choice

    def guess_checker(self, guess):
        if len(guess) != self.length:
            print("{}文字で入力してください。".format(self.length))
            return False
        guess_list = []
        for i in range(len(guess)):
            try:
                int(guess[i], base=self.max_ans)
            except ValueError:
                print("不正な数字・文字が入力されています。各桁の最大数字は{}までです。".format(self.max_ans - 1))
                return False
            guess_list.append(guess[i])
        if len(guess_list) != len(set(guess_list)):
            print("同じ数字を複数の桁に入力することはできません。")
            return False
        return True

    """
    敵の行動
    """

    def autoplay(self):
        vs = try_1003.AutoPlay("off")
        self.hist[1] = vs.run()

    def mob_turn(self):
        self.hp[0] -= int(self.atk[1] * self.mob_atk_ratio())
        if self.hp[0] <= 0:
            self.lose()
            return "finish"
        else:
            return "continue"

    def mob_atk_ratio(self):
        self.turn_count[1] += 1
        if self.dungeon_type == "normal":
            return 1
        # ボスの場合、アルゴリズムにhitblowを解かせる。
        # その際、内部処理としては、一度全て解かせて、全てのターンの情報を保存する。
        # プレイヤーが見える情報は、その内の一部の情報のみとする。
        if self.dungeon_type == "boss":
            #     print("----------")
            #     print(self.hist[1][self.turn_count[1] - 1])
            hit = self.hist[1][self.turn_count[1] - 1]["hit"]
            blow = self.hist[1][self.turn_count[1] - 1]["blow"]
            if hit == 3:
                print("強烈な力を感じる…")
            if hit == 5:
                print("周囲が光に包まれた！")
                return 1
            else:
                return hit * 0.05 + blow * 0.01

    """
    戦闘終了後
    """

    def win(self):
        print("敵を撃破した！")
        self.exp[0] += self.exp[1]
        self.money[0] += self.money[1]
        self.level_up_judge()
        self.drop()
        self.after_battle()

    def lose(self):
        print("You lose...")

    def level_up_judge(self):
        while True:
            if self.exp[0] > self.vlookup(self.book["level_table"], str(self.lv[0] + 1), 2):
                print("おめでとう！レベルが{}に上がった！".format(self.lv[0] + 1))
                print("HPが{}上がった！".format(self.vlookup(
                    self.book["level_table"], str(self.lv[0] + 1), 7)))
                print("攻撃が{}上がった！".format(self.vlookup(
                    self.book["level_table"], str(self.lv[0] + 1), 8)))
                self.lv[0] += 1
            else:
                break

    def drop(self) -> None:
        rand = random.random()
        for i in range(6):
            if rand < float(self.vlookup(self.mobsheet, "drop" + str(i + 1), 4)):
                print("{}を手に入れた！".format(self.vlookup(
                    self.mobsheet, "drop" + str(i + 1), 2)))
                self.droplist.append(self.vlookup(
                    self.mobsheet, "drop" + str(i + 1), 2))
                return(self.droplist)
        print(self.droplist)

    def after_battle(self):
        """戦闘後の処理
        ステータスの更新
        経験値の更新
        金の更新
        アイテムの更新
        以上の情報をエクセルファイルに更新・保存
        """
        # ステータス更新
        new_lv = self.lv[0]
        new_hp = self.vlookup(self.book["level_table"], str(new_lv), 3)
        new_atk = self.vlookup(self.book["level_table"], str(new_lv), 4)
        new_stats = [new_lv, new_hp, new_atk]
        for i, stat in enumerate(self.basic_status_index):
            self.mysheet[self.xy_index(
                self.mysheet, stat, 1, "raw", 1, "excel")] = new_stats[i]
        # self.mysheet[self.xy_index(
        #     self.mysheet, "lv", 1, "raw", 1, "excel")] = new_lv
        # self.mysheet[self.xy_index(
        #     self.mysheet, "hp", 1, "raw", 1, "excel")] = new_hp
        # self.mysheet[self.xy_index(
        #     self.mysheet, "atk", 1, "raw", 1, "excel")] = new_atk
        self.status_checker()
        # 経験値、金の更新
        self.mysheet.cell(row=self.vindex(
            self.mysheet, "exp"), column=2, value=self.exp[0])
        self.mysheet.cell(row=self.vindex(
            self.mysheet, "money"), column=2, value=self.money[0])
        # ドロップアイテム数は1のみ対応。
        # 解説：ゲットしたアイテムがまだ道具箱に1個もない→新しくインデックスを追加し個数を1増やす(実際に行う順序は、個数を1にしてからインデックス追加)
        # 　　　そうでない（すでにある）→個数を1増やす
        if self.vindex(self.book["道具箱"], self.droplist[0]) == False:
            self.book["道具箱"].cell(row=self.vindex(
                self.book["道具箱"], "empty"), column=2, value=self.vlookup(self.book["道具箱"], "empty", 2)+1)
            self.book["道具箱"].cell(row=self.vindex(
                self.book["道具箱"], "empty"), column=1, value=self.droplist[0])
        else:
            self.book["道具箱"].cell(row=self.vindex(self.book["道具箱"], self.droplist[0]),
                                  column=2, value=self.vlookup(self.book["道具箱"], self.droplist[0], 2)+1)
        print(self.vindex(self.book["道具箱"], "empty"))
        """開いてる途中だとエラー出るよ"""
        self.save()

    def save(self):
        """開いてる途中だとエラー出るよ"""
        try:
            self.book.save("systems/base.xlsx")
        except PermissionError:
            print("エクセルファイルを閉じてください")  # これ戦闘前に欲しい
            exit()


class Initialize(Battle):
    """めんどくさいからinitはそのままコピーした
    """

    def __init__(self) -> None:
        """コンストラクタ
        lv,hp,atk,skill[0]~[2],exp,moneyはリストとなっており、[0]がプレイヤー、[1]が敵
        """
        self.basic_status_index = ["lv", "hp", "atk"]
        self.mobname = "スライム"
        self.book = openpyxl.load_workbook('systems/base.xlsx', data_only=True)
        self.mobsheet = self.book[self.mobname]
        self.mysheet = self.book["プレイヤーステータス"]
        self.vs_sheet = [self.mysheet, self.mobsheet]
        self.lv = [0, 0]
        self.hp = [0, 0]
        self.atk = [0, 0]
        self.skill = [[0, 0] for j in range(3)]
        self.exp = [0, 0]
        self.money = [0, 0]
        for num, sheet in enumerate(self.vs_sheet):
            self.lv[num] = self.vlookup(sheet, "lv", 2)
            self.hp[num] = self.vlookup(sheet, "hp", 2)
            self.atk[num] = self.vlookup(sheet, "atk", 2)
            for j in range(3):
                self.skill[j][num] = self.vlookup(
                    sheet, "skill{}".format(j), 2)
            self.exp[num] = self.vlookup(sheet, "exp", 2)
            self.money[num] = self.vlookup(sheet, "money", 2)
        self.droplist = []

    def confirm(self):
        confirm = input("これまでのプレイデータを削除します。本当によろしいですか？[Y/n] ->")
        if confirm == "y" or confirm == "Y":
            input("削除されたデータは戻りません。本当によろしいですか？[Y/n] ->")
            if confirm == "y" or confirm == "Y":
                self.all_zero()
                print("データは削除されました m9(^Д^)")

    def all_zero(self):
        """戦闘後の処理を参考にした
        ステータスの更新
        経験値の更新
        金の更新
        アイテムの更新
        以上の情報をエクセルファイルに更新・保存
        """
        # ステータス更新
        init_lv = 0
        init_hp = 100
        init_atk = 10
        box = [init_lv, ]
        for stat in self.basic_status_index:
            for i in range(4):
                self.mysheet.cell(row=self.vindex(
                    self.mysheet, stat), column=i+2, value=init_lv)
                self.mysheet.cell(row=self.vindex(
                    self.mysheet, stat), column=i+2, value=init_hp)
                self.mysheet.cell(row=self.vindex(
                    self.mysheet, s), column=i+2, value=init_atk)
        # 経験値、金の更新
        self.mysheet.cell(row=self.vindex(
            self.mysheet, "exp"), column=2, value=0)
        self.mysheet.cell(row=self.vindex(
            self.mysheet, "money"), column=2, value=0)
        # ドロップアイテム数は1のみ対応。
        # 解説：ゲットしたアイテムがまだ道具箱に1個もない→新しくインデックスを追加し個数を1増やす(実際に行う順序は、個数を1にしてからインデックス追加)
        # 　　　そうでない（すでにある）→個数を1増やす
        for i in range(39):
            self.book["道具箱"].cell(row=i+2, column=1, value="empty")
            self.book["道具箱"].cell(row=i+2, column=2, value=0)
        self.save()
