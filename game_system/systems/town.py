from typing import List, Tuple, Optional
import random

from . import battle


class Town(battle.Battle):
    """街"""

    def __init__(self, dungeon_type, dungeon_num):
        super().__init__(dungeon_type, dungeon_num)

    def main(self):

        while True:
            print("メニュー")
            print("1:ステータスチェック")
            print("2:スキル")
            print("3:装備")
            print("4:アイテム")
            print("5:ショップ")
            print("6:クエスト")
            print("9:セーブしてタイトルに戻る")
            choice = input("何する？->")
            if choice == "1":
                self.town_status()
            elif choice == "2":
                self.town_skill()
            elif choice == "3":
                self.town_equip()
            elif choice == "4":
                self.town_item()
            elif choice == "5":
                self.town_shop()
            elif choice == "6":
                self.town_quest()
            elif choice == "7":
                self.town_debug()
            elif choice == "9":
                self.save()
                exit()

    def town_status(self):
        print(1)
        self.status_checker()
        self.status_printer()

    def town_equip(self):
        # 装備の情報更新
        self.equip_checker()
        equip_list = []
        # 今の装備を表示
        for i in range(self.vlookup(self.mysheet,"equip_qty",2)):
            print(("{} {} :{} (hp:+{}, atk:+{})").format(i,self.equip_position[i],self.vhlookup(self.mysheet, self.equip_position[i], 1,"name",self.equip_index_rownum),self.vhlookup(self.mysheet, self.equip_position[i], 1,"hp",self.equip_index_rownum),self.vhlookup(self.mysheet, self.equip_position[i], 1,"atk",self.equip_index_rownum)))
        # 装備変更
        s_pos = self.hindex(self.book["装備"],"position")
        s_name = self.hindex(self.book["装備"],"name")
        s_qty = self.hindex(self.book["装備"],"qty")
        choice_position = int(input("どの装備を変更しますか？[0~{}]->".format(self.equip_qty-1)))
        for i in range(500):
            # 部位が一致する装備を一覧表示するためにリストに追加
            # 所持数が空白だとエラー起きる
            if self.book["装備"].cell(row = i+1, column = s_pos).value == self.equip_position[choice_position] and self.book["装備"].cell(row = i+1, column = s_qty).value >=1:
                equip_list.append(self.book["装備"].cell(row = i+1, column = s_name).value)
        for i in range(len(equip_list)):
            print("{}:{}".format(i,equip_list[i]))
        choice_equips = int(input("どれと交換しますか？[0~{}]->".format(len(equip_list)-1)))
        self.mysheet[self.xy_index(self.mysheet, self.equip_position[choice_position], 1,"name",self.equip_index_rownum,"excel")] = equip_list[choice_equips]

        # 変更した状態を表示
        self.equip_checker()
        print("装備を変更しました。")
        for i in range(self.vlookup(self.mysheet,"equip_qty",2)):
            print(("{} {} :{} (hp:+{}, atk:+{})").format(i,self.equip_position[i],self.vhlookup(self.mysheet, self.equip_position[i], 1,"name",self.equip_index_rownum),self.vhlookup(self.mysheet, self.equip_position[i], 1,"hp",self.equip_index_rownum),self.vhlookup(self.mysheet, self.equip_position[i], 1,"atk",self.equip_index_rownum)))



    def town_debug(self):
        print(self.vhlookup(self.mysheet, "右手", 1,"name",22))


            #     def cul_pow2(self, num):
            #         return num ** 2

            # class classB(classA):
            #     def __init__(self):
            #         self.ans = ans

            #     def cul_pow3(self, num):
            #         return num ** 3

            # subClass = classB()
            # print(subClass.cul_pow3(3))
