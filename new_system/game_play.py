from systems import initialize
from systems import town
from systems import battle
import random
import pygame
from pygame import Surface, mixer
from pygame.locals import *
from typing import List, Tuple
import time
import sys
import systems
from systems import show_game4

pygame.init()
mixer.init()

def gui_title():
    display = Commander()
    # vs = battle.Battle()
    display.gui_run()
class Commander(show_game4.ShowGame):

    def __init__(self):
        """demand:デバッグを楽にするチートツール
        1でON、0でOFF
        0番目:hitblowの正答を[0,1,2,3,5]に固定
        1番目:画面選択をPCで固定
        2番目:プロローグをカット
        3番目:闇属性のみ選択肢をvalだけ削る
        4番目:属性の効果を、(1+val)倍する
        5番目:2にすると、マップのタップ当たり判定を表示
        """
        self.demand = [1,1,1,0,0,0]
        super().__init__(demand = self.demand)
        self.place = "entrance"
        self.dungeon_num = -1# 初期状態は-1。0になると街へ移動する。

    def gui_run(self):
        pygame.display.set_caption("Hit, Blow and Dragons")
        self.set_sound()
        # choice関連
        self.dict_name_list = ["初期画面", "ダイヤ購入", "ダイヤ購入確認", "街の入口","ステータストップ画面", "装備変更：変更対象",
                               "装備変更：手持ち", "ショップ画面", "ショップ確認画面", "ガチャ画面", "ガチャ確認画面", "クエスト画面", "クエスト確認画面","成長合成1","成長合成2","成長合成3","成長合成4","成長合成5","成長合成6","成長合成7","合成取消2","合成取消3","合成取消4","合成取消5","触媒購入2","触媒購入3","合成ガチャ2","合成ガチャ3","戦闘中アイテム選択画面","戦闘中アイテム使用確認画面"]
                            #    "保有アイテム","攻略済みダンジョン","攻略情報",
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
            #PCorスマホ
            if self.screen_count == 0:
                self.screen_select()
            #プロローグ
            elif self.screen_count == 1:
                if self.demand[2] != 1:
                    self.show_prologue()
                self.screen_count += 1

            # 伝えたいメッセージを表示したい場合
            # self.message = "残したいメッセージ"
            # とする。関数self.message_screenは使わない点に注意。
            elif self.message != "":
                self.message_screen(self.message)

            else:
                if self.choice_dict["初期画面"]["name"] == "False":
                    self.reset()
                    self.choice_screen("Hit and blow", [["街へ行く","戦闘準備"], ["ダンジョンへ行く","モンスターとの戦闘"], ["ダイヤ購入","課金コーナー"]],"", "初期画面")
                    self.run_count_town = [0, 0, 0, 0, 0, 0, 0]
                    self.run_count_battle = [0, 0, 0, 0, 0, 0, 0]
                    self.choice_dict.update({"初期画面": {"number": 1, "name": "ダンジョンへ行く"}})

                #街のトップページ
                #↓の行の左の>を押すと、街のコードを一気に隠せる
                elif self.choice_dict["初期画面"]["name"] == "街へ行く" or self.dungeon_num == 0:
                    if self.choice_dict["街の入口"]["number"] == "False":
                        # if self.run_count_town[0] == 0:
                        #     self.screen.blit(self.town_back_list[1],self.scenerect)
                        #     time.sleep(1)
                        #     self.run_count_town[0]+=1
                        self.choice_screen(
                            ["街の入口","Lv.{} Gold:{} Diamond:{}".format(self.lv,self.money,self.diamond)], [["ステータスチェック","現在のステータスを確認"],  ["装備","装備の変更"],  ["ショップ","アイテムの購入"],  ["ガチャ",["超強力なアイテムゲットのチャンス。","期間限定のハロウィンイベント実施中！"]], ["クエスト","依頼をこなして報酬をゲットせよ！"],["成長合成","武器をカスタマイズしよう！"],["ダイヤ購入","課金してダイヤモンドを購入します"]], "", "街の入口")

                    #ステータス表示
                    elif self.choice_dict["街の入口"]["name"] == "ステータスチェック":
                        if self.choice_dict["ステータストップ画面"]["number"] == "False":
                            if self.run_count_town[2] == 0:
                                # 装備の情報更新
                                self.status_checker()
                                id_list = self.current_equip_list("id")
                                # #アイテム情報更新
                                # all_item_type = ["戦闘用消耗品","戦闘開始時消耗品","属性付与","成長合成補助","成長合成取り消し"]
                                # all_item_list_own=[]
                                # for type in all_item_type:
                                #     all_item_list_own += self.item_type_list_multi_info(type,["name","qty","detail"],"on")
                                # all_item_list_own = list(zip(all_item_list_own))
                                # print(all_item_list_own)
                                self.run_count_town[2] += 1
                            
                            # self.choice_screen(
                            #     "何を確認しますか？", list(zip(["ステータス","攻略済みダンジョン","攻略情報"],["","","",""])),"", "ステータストップ画面", ["街の入口"])
                        # # アイテム表示
                        # elif self.choice_dict["ステータストップ画面"]["name"] == "アイテム":
                        #     if self.choice_dict["保有アイテム"]["name"] == "False":
                        #         #道具箱のところどうしよう…
                                
                        #         self.choice_screen("保有アイテム一覧",list(zip(["{}:{}".format(all_item_list_own[0],all_item_list_own[1])],[all_item_list_own[2]])),"","保有アイテム",["ステータストップ画面"])
                        
                        # # ステータス表示
                        # elif self.choice_dict["ステータストップ画面"]["name"] == "ステータス":
                            self.message = ["Level :{}".format(self.lv),"HP　　:{}(+{})".format(self.hp,self.mysheet["D3"].value),"水属性:{}".format(self.attr_power[0]),"木属性:{}".format(self.attr_power[1]),"闇属性:{}".format(self.attr_power[2]),"雷属性:{}".format(self.attr_power[3])]
                            self.init_town_info()


                        # # 旧ステータスチェック（装備情報や成長合成情報が保存されないとき、これを実行するとなぜか上手くいったので残しておく）
                        # self.town_status()
                        # self.init_town_info()
                        # self.save()

                    # 装備変更
                    elif self.choice_dict["街の入口"]["name"] == "装備":
                        if self.choice_dict["装備変更：変更対象"]["number"] == "False":
                            # 装備の情報更新
                            if self.run_count_town[1] == 0:
                                self.status_checker()
                                id_list = self.current_equip_list("id")
                                self.run_count_town[1] += 1
                            self.choice_screen("どの装備を変更しますか？" ,list(["{}:{}".format(self.id_equip_info(id_list[i],"position"),self.id_equip_info(id_list[i],"name")),self.id_equip_summery(id_list[i])]for i in range(len(id_list))),"" , "装備変更：変更対象", ["街の入口"])

                        elif self.choice_dict["装備変更：変更対象"]["number"] != "False" and self.choice_dict["装備変更：手持ち"]["number"] == "False":
                            selected_position = self.choice_dict["装備変更：変更対象"]["name"].split(':')[0]
                            current_id = id_list[self.choice_dict["装備変更：変更対象"]["number"]]
                            equip_list_name = self.equip_list_position(selected_position,"name")
                            equip_list_id = self.equip_list_position(selected_position,"id")
                            self.choice_screen_multi(
                                "{}の装備を変更".format(selected_position), list(["{}:{}".format(equip_list_id[i],equip_list_name[i]),self.id_equip_summery(equip_list_id[i])]for i in range(len(equip_list_name))),["現在装備:{}".format(self.id_equip_info(current_id,"name")),self.id_equip_summery(current_id)[0],self.id_equip_summery(current_id)[1]] , "装備変更：手持ち", ["装備変更：変更対象"])

                        elif self.choice_dict["装備変更：手持ち"]["number"] != "False":
                            selected_id = self.choice_dict["装備変更：手持ち"]["name"].split(":")[0]
                            self.mysheet[self.vhindex_super(self.mysheet, selected_position,
                                    1, "id", "position", "excel","off")] = int(selected_id)
                            self.status_checker()
                            self.init_town_info()
                            self.save()

                    #アイテムショップ
                    elif self.choice_dict["街の入口"]["name"] == "ショップ":
                        # 素材を魔女のところへ、装備購入をこちらで。進度に応じて変更したい。
                        if self.choice_dict["ショップ画面"]["number"] == "False":
                            item_list_consume = ["薬草","回復薬","妨害の笛","知恵の書","ハイポーション"]
                            item_list_material = ["水の砂","木の砂","闇の砂","雷の砂","砂金"]
                            self.choice_screen_multi(["ショップ","所持金:{}G".format(self.money)],
                            [self.show_nonequip_item(item_list_consume),self.show_nonequip_item(item_list_material)]
                            ,[["戦闘用消耗品コーナー", "右下・左下のボタンで他のコーナーに行けるよ"],["属性の砂コーナー", "付与属性値が増えると、", "各々の色の選択肢が一定確率で減少する"]]
                            , "ショップ画面",[],"off","on")
                        elif self.choice_dict["ショップ画面"]["name"] != "False" and self.choice_dict["ショップ確認画面"]["name"] == "False":
                            self.choice_screen(
                                ["{}を{}Gで買います。".format(self.choice_dict["ショップ画面"]["name"],self.item_info(self.choice_dict["ショップ画面"]["name"],"value")),"よろしいですか？"], [["はい",""], ["いいえ",""]], [""], "ショップ確認画面", ["ショップ画面"])
                        elif self.choice_dict["ショップ確認画面"]["name"] == "はい":
                            # お金が足りないときの処理を忘れずに
                            value = self.vhlookup(
                                self.book["アイテム箱"], self.choice_dict["ショップ画面"]["name"], 2, "value", 1)
                            if self.buy_item(self.choice_dict["ショップ画面"]["name"], value) == False:
                                self.message="ゴールドかダイヤモンドが足りません"
                            print("{}を購入".format(self.choice_dict["ショップ画面"]["name"]))
                            self.choice_dict["ショップ確認画面"] = {"number": "False", "name": "False"}
                            self.choice_dict["ショップ画面"] = {"number": "False", "name": "False"}
                            self.save()
                        elif self.choice_dict["ショップ確認画面"]["name"] == "いいえ":
                            self.choice_dict["ショップ確認画面"] = {"number": "False", "name": "False"}
                            self.choice_dict["ショップ画面"] = {"number": "False", "name": "False"}
                            
                    #クエスト
                    elif self.choice_dict["街の入口"]["name"] == "クエスト":
                        if self.choice_dict["クエスト画面"]["number"] == "False":
                            self.choice_screen(
                                "クエスト", [["装備の錆取り",""],["ゴブリン討伐依頼",""],["最高の豚肉を求めて",""],["城壁の修復",""],["古龍の足跡",""]], "未実装です", "クエスト画面")
                        elif self.choice_dict["クエスト画面"]["name"] != "False" and self.choice_dict["クエスト確認画面"]["name"] == "False":
                            self.choice_screen(
                                "クエスト：{}を受諾しますか？".format(self.choice_dict["クエスト画面"]["name"]), [["はい",""],["いいえ",""]], "受けられないよ", "クエスト確認画面", ["クエスト画面"])
                        elif self.choice_dict["クエスト確認画面"]["name"] == "はい":
                            self.message = "クエスト：{}を受諾しました。".format(self.choice_dict["クエスト画面"]["name"])
                            self.choice_dict["クエスト確認画面"] = {
                                "number": "False", "name": "False"}
                            self.choice_dict["クエスト画面"] = {
                                "number": "False", "name": "False"}
                        elif self.choice_dict["クエスト確認画面"]["name"] == "いいえ":
                            self.choice_dict["クエスト確認画面"] = {
                                "number": "False", "name": "False"}
                            self.choice_dict["クエスト画面"] = {
                                "number": "False", "name": "False"}

                    #ガチャ
                    elif self.choice_dict["街の入口"]["name"] == "ガチャ":
                        if self.choice_dict["ガチャ画面"]["number"] == "False":
                            self.choice_screen(
                                "ガチャ　　　　　　　　　　　保有ダイヤモンド:{}".format(self.diamond), [["【期間限定】ハロウィンガチャ","3ダイヤモンド　10/31までの期間限定。ハロウィン装備を手に入れよう！"], ["スーパーガチャ","1ダイヤモンド　限定装備や限定素材が盛りだくさん！"], ["ノーマルガチャ","500G　ゲーム内通貨で回せるお得なガチャ"]],"", "ガチャ画面")
                            value_dict = {"【期間限定】ハロウィンガチャ":[0,3],"スーパーガチャ":[0,1],"ノーマルガチャ":[500,0]}
                        elif self.choice_dict["ガチャ画面"]["name"] != "False" and self.choice_dict["ガチャ確認画面"]["name"] == "False":
                            gold_value = value_dict[self.choice_dict["ガチャ画面"]["name"]][0]
                            diamond_value = value_dict[self.choice_dict["ガチャ画面"]["name"]][1]
                            self.choice_screen(
                                "本当に{}を買いますか？".format(self.choice_dict["ガチャ画面"]["name"]), [["はい",""], ["いいえ",""]], "", "ガチャ確認画面", ["ガチャ画面"])
                            atodekesu_count = 0
                        elif self.choice_dict["ガチャ確認画面"]["name"] == "はい":
                            if atodekesu_count == 0:
                                print("{}を回した！".format(
                                    self.choice_dict["ガチャ画面"]["name"]))
                                selected_item, item_rarity = self.gacha(self.book["ガチャ"],self.choice_dict["ガチャ画面"]["name"])
                                if self.buy_item(selected_item,gold_value,diamond_value) == False:
                                    self.message = "ゴールドかダイヤモンドが足りません"
                                    self.choice_dict["ガチャ確認画面"] = {"number": "False", "name": "False"}
                                    self.choice_dict["ガチャ画面"] = {"number": "False", "name": "False"}
                                else:
                                    print("{}:{}を手に入れた！".format(item_rarity, selected_item))
                                    self.save()
                                atodekesu_count += 1
                            self.gacha_show(item_rarity)
                            self.message =("{}:{}を手に入れた！".format(self.rarity_dict[item_rarity], selected_item))
                            self.choice_dict["ガチャ確認画面"] = {
                                "number": "False", "name": "False"}
                            self.choice_dict["ガチャ画面"] = {
                                "number": "False", "name": "False"}
                        elif self.choice_dict["ガチャ確認画面"]["name"] == "いいえ":
                            self.choice_dict["ガチャ確認画面"] = {
                                "number": "False", "name": "False"}
                            self.choice_dict["ガチャ画面"] = {
                                "number": "False", "name": "False"}
                    
                    # 成長合成関連のトップページ
                    elif self.choice_dict["街の入口"]["name"] == "成長合成":
                        if self.choice_dict["成長合成1"]["number"] == "False":
                            # 装備の情報更新
                            if self.run_count_town[5] == 0:
                                self.status_checker()
                                id_list = self.current_equip_list("id")
                                self.run_count_town[5] += 1
                            self.choice_screen(["ここは魔女の隠れ家。","何をしますか？"], [["魔女の鍛冶場","成長合成を行い、武器に属性を付与します"],["魔女の実験室","魔女の秘薬を用いて、満足な結果が得られなかったスロットを消去します"],["魔女の闇市","成長合成を補助する触媒や秘薬を購入します"],["魔女の宝箱","最高性能の素材や触媒を手に入れるチャンス"]],["武器は、成長合成を経て初めて効果を発揮する。","属性基礎力が強いほど、よい属性値がつきやすい。","ただし、結果は、魔女の気まぐれ次第。"],"成長合成1", ["街の入口"])


                        #成長合成の開始
                        elif self.choice_dict["成長合成1"]["name"] =="魔女の鍛冶場":
                            # 右手装備以外にも実装したらここを有効化し、12行下の【"成長合成3", ["成長合成1"]】を【"成長合成2", ["成長合成1"]】にする。
                            # if self.choice_dict["成長合成2"]["number"] == "False":
                            #     self.choice_screen(
                            #         "現在、成長合成の可能な装備は武器（右手）のみです。",list(zip(self.equip_position,["","","","",""])) ,"", "成長合成2", ["成長合成1"])
                            # elif self.choice_dict["成長合成2"]["number"] != "False" and self.choice_dict["成長合成3"]["number"] == "False":
                            if self.choice_dict["成長合成3"]["number"] == "False":
                                id_list = self.equip_list_position("右手","id")
                                dic_list = []
                                for id_num in id_list:
                                    dic_list.append(self.id_equip_dict(id_num))
                                self.choice_screen_multi("どの装備を成長合成しますか？", list(["{}:{}".format(dic_list[i]["id"],dic_list[i]["name"]),
                                self.id_equip_summery(id_list[i])]for i in range(len(dic_list))),"" , "成長合成3", ["成長合成1"])

                            elif self.choice_dict["成長合成3"]["name"] != "False" and self.choice_dict["成長合成4"]["number"] == "False":
                                sel_num = self.choice_dict["成長合成3"]["number"]
                                dic = dic_list[sel_num]
                                equip_id = id_list[sel_num]
                                slot_val_list = []
                                for j in range(dic["slot_qty"]):
                                    if dic["slot{}_attr".format(j+1)] == None:
                                        slot_val_list.append("Slot{}:空き".format(j+1))
                                    else:
                                        slot_val_list.append("Slot{}:{}+{}%".format(j+1,self.attr_dict[dic["slot{}_attr".format(j+1)]],dic["slot{}_val".format(j+1)]))
                                self.choice_screen("{}への成長合成".format(self.choice_dict["成長合成3"]["name"].split(":")[1]),list(zip(slot_val_list,["","","","",""])),"","成長合成4",["成長合成3"])

                            elif self.choice_dict["成長合成4"]["name"] != "False" and self.choice_dict["成長合成4"]["name"].split(":")[1]!="空き":
                                self.message = "そのスロットはすでに付与されています。"
                                self.choice_dict["成長合成4"] = {"number": "False", "name": "False"}
                            elif self.choice_dict["成長合成4"]["name"] != "False" and self.choice_dict["成長合成5"]["number"] == "False":
                                sel_slot = self.choice_dict["成長合成4"]["number"]+1
                                material_infos = self.item_type_list_multi_info("属性付与",["name","effect_type","effect_val","effect_val_max"],"on")
                                material_list_name = material_infos[0]
                                material_list_attr = material_infos[1]
                                material_list_min = material_infos[2]
                                material_list_max = material_infos[3]
                                material_detail_list = []
                                for i in range(len(material_list_name)):
                                    material_detail_list.append("属性:{},付与値：+{}～+{}".format(self.attr_dict[material_list_attr[i].split("_")[0]],round(material_list_min[i]*dic["atk"]/100),round(material_list_max[i]*dic["atk"]/100)))
                                self.choice_screen_multi("成長合成の素材を選択",list(zip(material_list_name,material_detail_list)),"","成長合成5",["成長合成4"])

                            elif self.choice_dict["成長合成5"]["name"] != "False" and self.choice_dict["成長合成6"]["number"] == "False":
                                material = self.choice_dict["成長合成5"]["name"]
                                catalyst_infos = self.item_type_list_multi_info("成長合成補助",["name","effect_type","effect_val_max"],"on")
                                catalyst_dict = {"compound_max_up":"最大値上昇","compound_min_up":"最小値上昇","compound_luck_up":"ランダム数値向上"}
                                catalyst_list_name = ["なし"]
                                catalyst_list_name.extend(catalyst_infos[0])
                                catalyst_list_effect=(catalyst_infos[1])
                                catalyst_list_val=(catalyst_infos[2])
                                catalyst_detail_list=[""]
                                catalyst = ""
                                catalyst_red = ""
                                catalyst_blue = ""
                                catalyst_green = ""
                                for i in range(len(catalyst_list_name)-1):
                                    catalyst_detail_list.append("{}:+{}%".format(catalyst_dict[catalyst_list_effect[i]],catalyst_list_val[i]))
                                self.choice_screen_multi("成長合成補助の触媒を選択",list(zip(catalyst_list_name,catalyst_detail_list)),"","成長合成6",["成長合成5"])

                            elif self.choice_dict["成長合成6"]["name"] not in ["False","なし","これで決定"] and self.choice_dict["成長合成7"]["number"] == "False":
                                if self.choice_dict["成長合成6"]["name"] == "選択取消":
                                    catalyst = ""
                                    catalyst_red = ""
                                    catalyst_blue = ""
                                    catalyst_green = ""
                                else:
                                    catalyst = self.choice_dict["成長合成6"]["name"]
                                catalyst_red,catalyst_blue,catalyst_green =  self.catalyst_judge(catalyst,catalyst_red,catalyst_blue,catalyst_green)
                                material = self.choice_dict["成長合成5"]["name"]
                                catalyst_infos = self.item_type_list_multi_info("成長合成補助",["name","effect_type","effect_val_max"],"on")
                                catalyst_dict = {"compound_max_up":"最大値上昇","compound_min_up":"最小値上昇","compound_luck_up":"ランダム数値向上"}
                                catalyst_list_name = ["これで決定","選択取消"]
                                catalyst_list_name.extend(catalyst_infos[0])
                                catalyst_list_effect=(catalyst_infos[1])
                                catalyst_list_val=(catalyst_infos[2])
                                catalyst_detail_list=["",""]
                                catalyst_red_detail = "{}:最大値上昇+{}%".format(catalyst_red,self.if_return(self.item_info(catalyst_red,"effect_val_max"),False,0))
                                catalyst_blue_detail = "{}:最小値上昇+{}%".format(catalyst_blue,self.if_return(self.item_info(catalyst_blue,"effect_val_max"),False,0))
                                catalyst_green_detail = "{}:ランダム数値上昇+{}%".format(catalyst_green,self.if_return(self.item_info(catalyst_green,"effect_val_max"),False,0))
                                for i in range(len(catalyst_list_name)-2):
                                    catalyst_detail_list.append("{}:+{}%".format(catalyst_dict[catalyst_list_effect[i]],catalyst_list_val[i]))
                                self.choice_screen_multi("成長合成補助の触媒を選択",list(zip(catalyst_list_name,catalyst_detail_list)),[catalyst_red_detail,catalyst_blue_detail,catalyst_green_detail],"成長合成6",["成長合成5"])

                            elif self.choice_dict["成長合成6"]["name"] in ["なし","これで決定"] and self.choice_dict["成長合成7"]["number"] == "False":
                                min_val,max_val = self.compound_min_max(equip_id,sel_slot,material,catalyst_red,catalyst_blue,catalyst_green)
                                self.choice_screen("以下の内容で成長合成を行います。よろしいですか？",list(zip(["はい","いいえ"],["",""])),["対象：{}, 合成素材:{}".format(self.id_equip_info(equip_id,"name"),material),"触媒:{}".format(catalyst),"最小値:{},最大値:{}".format(min_val,max_val)],"成長合成7",["成長合成6"])
                            elif self.choice_dict["成長合成7"]["name"] == "はい":
                                attr,value,rand_value = self.compound(equip_id,sel_slot,material,catalyst_red,catalyst_blue,catalyst_green)
                                self.status_checker()
                                self.save()
                                self.gacha_show(rand_value,"on")
                                self.message =("{}属性値が{}上昇した！".format(self.attr_dict[attr],value))
                                self.choice_dict["成長合成7"] = {"number": "False", "name": "False"}
                                self.choice_dict["成長合成6"] = {"number": "False", "name": "False"}
                                self.choice_dict["成長合成5"] = {"number": "False", "name": "False"}
                                self.choice_dict["成長合成4"] = {"number": "False", "name": "False"}
                                self.choice_dict["成長合成3"] = {"number": "False", "name": "False"}
                            elif self.choice_dict["成長合成7"]["name"] == "いいえ":
                                self.choice_dict["成長合成7"] = {"number": "False", "name": "False"}
                                self.choice_dict["成長合成6"] = {"number": "False", "name": "False"}

                        #成長合成の取り消し
                        elif self.choice_dict["成長合成1"]["name"] =="魔女の実験室":
                            # if self.choice_dict["合成取消2"]["number"] == "False":
                            #     self.choice_screen(
                            #         "現在、成長合成取り消しの可能な装備は武器（右手）のみです。",list(zip(self.equip_position,["","","","",""])) ,"", "合成取消2", ["成長合成1"])
                            # elif self.choice_dict["合成取消2"]["number"] != "False" and self.choice_dict["合成取消3"]["number"] == "False":
                            if self.choice_dict["合成取消3"]["number"] == "False":
                                id_list = self.equip_list_position("右手","id")
                                dic_list = []
                                for id_num in id_list:
                                    dic_list.append(self.id_equip_dict(id_num))
                                self.choice_screen_multi("どの装備の付与を取り除きますか？", list(["{}:{}".format(dic_list[i]["id"],dic_list[i]["name"]),
                                self.id_equip_summery(id_list[i])]for i in range(len(dic_list))),"" , "合成取消3", ["成長合成1"])
                            elif self.choice_dict["合成取消3"]["name"] != "False" and self.choice_dict["合成取消4"]["number"] == "False":
                                sel_num = self.choice_dict["合成取消3"]["number"]
                                dic = dic_list[sel_num]
                                equip_id = id_list[sel_num]
                                slot_val_list = []
                                for j in range(dic["slot_qty"]):
                                    if dic["slot{}_attr".format(j+1)] == None:
                                        slot_val_list.append("Slot{}:空き".format(j+1))
                                    else:
                                        slot_val_list.append("Slot{}:{}+{}%".format(j+1,dic["slot{}_attr".format(j+1)],dic["slot{}_val".format(j+1)]))
                                self.choice_screen("{}の成長合成を取り消し".format(self.choice_dict["合成取消3"]["name"].split(":")[1]),list(zip(slot_val_list,["","","","",""])),"","合成取消4",["合成取消3"])
                            elif self.choice_dict["合成取消4"]["name"] != "False" and self.choice_dict["合成取消4"]["name"].split(":")[1]=="空き" and self.choice_dict["合成取消5"]["name"] == "False":
                                self.message = "そのスロットには何も合成されていません。"
                                self.choice_dict["合成取消4"] = {"number": "False", "name": "False"}
                            elif self.choice_dict["合成取消4"]["name"] != "False" and self.choice_dict["合成取消4"]["name"].split(":")[1]!="空き"and self.choice_dict["合成取消5"]["name"] == "False":
                                sel_slot = self.choice_dict["合成取消4"]["number"]+1
                                self.choice_screen("本当に成長合成を取り除きますか？",list(zip(["はい","いいえ"],["魔女の秘薬を消費します",""])),["【注意】取り除いた合成の素材、触媒は","戻ってきません。"],"合成取消5",["合成取消4"])
                            elif self.choice_dict["合成取消5"]["name"] =="はい":
                                if self.item_info("魔女の秘薬","qty") <= 0:
                                    self.message="魔女の秘薬がありません。"
                                    self.init_town_info()
                                else:
                                    self.decompound(equip_id,sel_slot)
                                    self.choice_dict["合成取消5"] = {"number": "False", "name": "False"}
                                    self.choice_dict["合成取消4"] = {"number": "False", "name": "False"}
                                    self.choice_dict["合成取消3"] = {"number": "False", "name": "False"}
                                    self.status_checker()
                                    self.save()
                                    self.message = "成長合成を取り消しました。"
                            elif self.choice_dict["合成取消5"]["name"] == "いいえ":
                                self.choice_dict["合成取消5"] = {"number": "False", "name": "False"}
                                self.choice_dict["合成取消4"] = {"number": "False", "name": "False"}

                        #成長合成関連アイテム購入
                        elif self.choice_dict["成長合成1"]["name"] == "魔女の闇市":
                            if  self.choice_dict["触媒購入2"]["number"] == "False":
                                witch_name_list = ["ルビー","サファイア","エメラルド","魔女の秘薬"]
                                witch_detail_list = list(["{}ダイヤモンド".format(self.item_info(name,"extra_value")),self.item_info(name,"detail")]for name in witch_name_list)
                                self.choice_screen(["ここは魔女の闇市","{}ダイヤモンド".format(self.diamond)],list(zip(witch_name_list,witch_detail_list)) ,"", "触媒購入2", ["成長合成1"])
                                    
                            elif self.choice_dict["触媒購入2"]["name"] !="False" and self.choice_dict["触媒購入3"]["number"] == "False":
                                sel_item = self.choice_dict["触媒購入2"]["name"]
                                dia_value = self.item_info(sel_item,"extra_value")
                                self.yes_no_choice("{}を{}ダイヤモンドで購入します。よろしいですか？".format(sel_item,dia_value),"","触媒購入3", ["触媒購入2"])
                            elif self.choice_dict["触媒購入3"]["name"] =="はい":
                                if self.buy_item(sel_item, 0,dia_value) == False:
                                    self.message="ゴールドかダイヤモンドが足りません"
                                print("{}を購入".format(sel_item))
                                self.choice_dict["触媒購入3"] = {"number": "False", "name": "False"}
                                self.choice_dict["触媒購入2"] = {"number": "False", "name": "False"}
                                self.save()
                            elif self.choice_dict["触媒購入3"]["name"] == "いいえ":
                                self.choice_dict["触媒購入3"] = {"number": "False", "name": "False"}
                                self.choice_dict["触媒購入2"] = {"number": "False", "name": "False"}

                        #成長合成ガチャ
                        elif self.choice_dict["成長合成1"]["name"] == "魔女の宝箱":
                            if  self.choice_dict["合成ガチャ2"]["number"] == "False":
                                self.choice_screen(["ここは魔女の宝物庫","{}ダイヤモンド".format(self.diamond)], [["魔女の宝箱","2ダイヤモンド　闇市にすら出回らないレアな触媒や素材が入っているかも？"],["禁忌の宝箱","10ダイヤモンド　神々の素材や魔石が入っているといわれている。"]],"", "合成ガチャ2",["成長合成1"])
                                value_dict = {"魔女の宝箱":[0,2],"禁忌の宝箱":[0,10]}
                            elif self.choice_dict["合成ガチャ2"]["name"] != "False" and self.choice_dict["合成ガチャ3"]["name"] == "False":
                                gold_value = value_dict[self.choice_dict["合成ガチャ2"]["name"]][0]
                                diamond_value = value_dict[self.choice_dict["合成ガチャ2"]["name"]][1]
                                self.choice_screen(
                                    "本当に{}を買いますか？".format(self.choice_dict["合成ガチャ2"]["name"]), [["はい",""], ["いいえ",""]], "", "合成ガチャ3", ["合成ガチャ2"])
                                atodekesu_count = 0
                            elif self.choice_dict["合成ガチャ3"]["name"] == "はい":
                                if atodekesu_count == 0:
                                    print("{}を回した！".format(
                                        self.choice_dict["合成ガチャ2"]["name"]))
                                    selected_item, item_rarity = self.gacha(self.book["ガチャ"],self.choice_dict["合成ガチャ2"]["name"])
                                    if self.buy_item(selected_item,gold_value,diamond_value) == False:
                                        self.message = "ゴールドかダイヤモンドが足りません"
                                        self.choice_dict["合成ガチャ3"] = {"number": "False", "name": "False"}
                                        self.choice_dict["合成ガチャ2"] = {"number": "False", "name": "False"}
                                    else:
                                        print("{}:{}を手に入れた！".format(item_rarity, selected_item))
                                        self.save()
                                    atodekesu_count += 1
                                self.gacha_show(item_rarity)
                                self.message =("{}:{}を手に入れた！".format(self.rarity_dict[item_rarity], selected_item))
                                self.choice_dict["合成ガチャ3"] = {
                                    "number": "False", "name": "False"}
                                self.choice_dict["合成ガチャ2"] = {
                                    "number": "False", "name": "False"}
                            elif self.choice_dict["合成ガチャ3"]["name"] == "いいえ":
                                self.choice_dict["合成ガチャ3"] = {
                                    "number": "False", "name": "False"}
                                self.choice_dict["合成ガチャ2"] = {
                                    "number": "False", "name": "False"}

                    elif self.choice_dict["街の入口"]["name"] == "ダイヤ購入":
                        if self.choice_dict["ダイヤ購入"]["number"] == "False":
                            self.choice_screen(["何個購入しますか？","保有ダイヤモンド:{}".format(self.diamond)], list(zip(["1個","10個","50個","100個"],["¥100","¥900","¥4000","¥7500"])), ["※現在は無料で購入できます"],  "ダイヤ購入")
                        elif self.choice_dict["ダイヤ購入"]["name"] != "False" and self.choice_dict["ダイヤ購入確認"]["name"] == "False":
                            diamond_qty = int(self.choice_dict["ダイヤ購入"]["name"][:-1])
                            self.choice_screen("ダイヤを{}個購入します。本当によろしいですか？".format(diamond_qty), [["はい",""],["いいえ",""]], [""], "ダイヤ購入確認", ["ダイヤ購入"])
                        elif self.choice_dict["ダイヤ購入確認"]["name"] == "はい":
                            self.message = "ご購入ありがとうございます！"
                            self.buy_diamond(diamond_qty)
                            self.save()
                            print("ダイヤ{}個購入".format(diamond_qty))
                            self.choice_dict["ダイヤ購入確認"] = {"number": "False", "name": "False"}
                            self.choice_dict["ダイヤ購入"] = {"number": "False", "name": "False"}
                        elif self.choice_dict["ダイヤ購入確認"]["name"] == "いいえ":
                            self.choice_dict["ダイヤ購入確認"] = {"number": "False", "name": "False"}
                            self.choice_dict["ダイヤ購入"] = {"number": "False", "name": "False"}

                elif self.choice_dict["初期画面"]["name"] == "ダンジョンへ行く":
                    if self.gamescene == 0:
                        self.show_map()
                    elif self.error_count == 1:
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

                    elif self.item_screen_count == 1:
                        if self.choice_dict["戦闘中アイテム選択画面"]["name"] == "False":
                            item_list_battle = self.item_type_list("戦闘用消耗品","name")
                            self.choice_screen_multi("アイテム",list([item_list_battle[i],self.item_info(item_list_battle[i],"detail")]for i in range(len(item_list_battle))),"","戦闘中アイテム選択画面",["戦闘中アイテム選択画面"],"on","off",1)
                        elif self.choice_dict["戦闘中アイテム選択画面"]["name"] != "False" and self.choice_dict["戦闘中アイテム使用確認画面"]["name"] == "False":
                            self.choice_screen("{}を使用しますか？".format(self.choice_dict["戦闘中アイテム選択画面"]["name"]), [["はい",""],["いいえ",""]],[self.item_info(self.choice_dict["戦闘中アイテム選択画面"]["name"],"detail")], "戦闘中アイテム使用確認画面", ["戦闘中アイテム選択画面"])
                        elif self.choice_dict["戦闘中アイテム使用確認画面"]["name"] == "はい":
                            self.item_use_battle(self.choice_dict["戦闘中アイテム選択画面"]["name"])
                            self.choice_dict["戦闘中アイテム使用確認画面"] = {
                                "number": "False", "name": "False"}
                            self.choice_dict["戦闘中アイテム選択画面"] = {
                                "number": "False", "name": "False"}
                            self.turn += 1
                            self.item_screen_count = 0
                        elif self.choice_dict["戦闘中アイテム使用確認画面"]["name"] == "いいえ":
                            self.choice_dict["戦闘中アイテム使用確認画面"] = {
                                "number": "False", "name": "False"}
                            self.choice_dict["戦闘中アイテム選択画面"] = {
                                "number": "False", "name": "False"}
                        if self.enemy_stop < 1 and self.item_screen_count == 0:
                            time.sleep(0.4)
                            self.damage_effect()

                    elif self.gamescene == 0:  # ホーム画面
                        self.show_map()
                        self.reset()
                        # self.home_show()
                        self.home_judge()
                    elif self.gamescene == 5:  # how to play
                        self.how_to_play()
                        self.how_to_play_judje()

                    elif self.gamescene == 1:  # Normal Stage
                        if self.run_count_battle[1] == 0:
                            # 各戦闘毎に一回のみ動作させたい 
                            #第一ステージのときはhow to playを毎回出現させる。
                            self.dungeon_init()
                            self.second_init_showgame()
                            self.print_status()
                            self.run_count_battle[1] += 1
                            self.run_count_battle[6] = 1
                            self.enemy_stop = 0
                        if self.run_count_battle[6] < self.turn:
                            # 各ターンに一度だけ動作させたい
                            if self.enemy_stop >= 1:
                                self.enemy_stop -= 1
                            else:
                                self.hp_g -= self.damage
                            self.run_count_battle[6] += 1
                        self.normal_stage()
                        self.normal_stage_judge()
                        self.boss_action() #消し忘れ？

                    elif self.gamescene == 2:  # Boss Stage
                        if self.run_count_battle[2] == 0:
                            self.dungeon_init()
                            self.autoplay()
                            self.boss_history = self.hist[1]
                            # print(self.boss_history)
                            self.second_init_showgame()
                            self.run_count_battle[2] += 1
                            self.run_count_battle[6] = 1
                        if self.run_count_battle[6] < self.turn:
                            # 各ターンに一度だけ動作させたい
                            # print(self.turn)
                            # self.hp_g -= self.damage
                            self.run_count_battle[6] += 1
                        if self.switch_judge("turn_switch", self.turn_switch, 0) == True:
                            if self.jamming_judge("player") == "stop":
                                print("調査を妨害された！")
                                time.sleep(1)
                                self.boss_action("boss")

                        self.turn_switch = 0

                        self.boss_stage()
                        self.normal_stage_judge("boss")

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
                        self.level_up_screen()
                        self.result_judge()

                    if self.switch_judge("gamescene", self.gamescene, 0) == True:
                        self.init_battle_info()

            pygame.display.update()  # スクリーン上のものを書き換えた時にはupdateが必要
    def init_town_info(self):
        """街の入口に戻る
        「初期画面」以外のdict_name情報は（戦闘関連も含めて）すべて初期化される"""
        init_list = self.dict_name_list[1:]
        for i in init_list:
            self.choice_dict[i]["number"] = "False"
            self.choice_dict[i]["name"] = "False"
        self.run_count_town = [0, 0, 0, 0, 0, 0, 0]

    def init_battle_info(self):
        self.run_count_battle = [0, 0, 0, 0, 0, 0, 0]
        self.turn_switch = 0

    def show_nonequip_item(self,item_list):
        """1ページ分の情報を表示する"""
        return list([item_list[i],"{}G  {}".format(self.item_info(item_list[i],"value"),self.item_info(item_list[i],"detail"))]for i in range(len(item_list)))

    # def show_quest_info(self,quest_list)
class Debug(Commander):

    def __init__(self):
        super().__init__()


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