# coding: UTF-8
# このファイルは、run.pyと同じ階層に入れないとバグる

# import send_recieve
from send_recieve import SendReceive
import random
import math
import copy
"""
やること
　【万一のバグに備える】
　もし同じ数字でループするなら、「3回cond!=9の中でランダムに実行する」をやってみるといいかも？
　なんかの手違いでhit=4になったら、blowlistの残りをぶち込むシステムを入れていいかも
　【より強くする】
　位置情報の強化：確定hitが発生したら、過去のデータを遡り、そのhitが該当してかつhit数が1である探索回があれば、その探索回におけるhit以外の数字の位置情報を1から2にする（これが一番コスパよさそう）
　終盤の強化：探索数を2にする（平均1ターンくらい早くなりそう。ただ、かなりめんどくさそう）
　中盤の強化：終盤のように、位置情報の和が大きいものを優先する（これは早く…なるのか？（終盤とは状況が違うので、これで早くなるかは分からない））
"""


class AutoPlay():
    """自動解答プログラム"""

    def __init__(self, print_mode):
        self.print_mode = print_mode
        self.ram = []
        self.gnum_count = -1
        self.ans_list = [0, 0, 0, 0, 0]
        self.ans_str = ""

        # room_id = input("input room id ->")
        # player_id = input("input your name ->")

        # グローバル関数
        self.numberinfo = [{"number": j, 0: 0, 1: 0, 2: 0, 3: 0,
                            4: 0, "cond": 0, "gnum": -1} for j in range(16)]
        self.groupinfo = []
        self.history = []
        self.wholeinfo = {"phase": 0, "turn": 1, "confirmed_blow_and_hit": 0,
                          "confirmed_hit": 0, "noob": 0, "rough_blow": 0, "special_mode": 0}
        self.blow_list = []
        self.hit_list = [-1, -1, -1, -1, -1]
        self.phase_list = {0: "Early phase", 1: "Early phase",
                           2: "Early phase", 3: "Middle phase", 4: "FINAL phase"}
        self.game_record = []
        # {"Early_phase_turns": 0, "Middle_phase_turns": 0, "Final_phase_turns": 0,}

    def pos(self, x):
        if x > 0:
            return True
        else:
            return False

    def zero_checker(self, x):
        if x == 0:
            return 0
        else:
            return 1

    def curse(self, x):
        if x == 3 and self.wholeinfo["special_mode"] >= 1:
            return 1
        else:
            return 100

    def fugaku(self, ninfo, ginfo, hist, winfo):
        """
        更新されたデータをもとに、回答を自動生成する。
        序盤、中盤、終盤で振る舞いが異なる。
        ※序盤：0~4,5~9,a~eを総当りで試す3ターン
        中盤：当たりの数字5つを探索する
        終盤：探索された5つの数字を並び替える
        """
        """序盤"""
        if winfo["phase"] < 3:
            if winfo["phase"] == 0:
                return ("01234")
            elif winfo["phase"] == 1:
                return ("56789")
            elif winfo["phase"] == 2:
                return ("abcde")
            else:
                print("unexpected error 001")

            """中盤"""
        elif winfo["phase"] == 3:
            guess_mid_list = [-1, -1, -1, -1, -1]  # 中盤用アルゴリズムの答えを入力する箱
            guess_mid_str = ""
            # # # #どのグループから探索するかを決める。ハズレを4つ見つけるまでは、ハズレ発見を優先する
            # # # if winfo["noob"] < 4:
            # # #     priority_value = [(1000 - 100 * j["leng"] - (j["blow"]+j["hit"]))* self.zero_checker((j["blow"]+j["hit"])*(j["leng"]-(j["blow"]+j["hit"]))) for j in ginfo]
            # # # else:
            # # #     priority_value = [(1000 - 100 * j["leng"] - 10 * j["hit"] + (j["blow"]+j["hit"]))*self.zero_checker((j["blow"]+j["hit"])*(j["leng"]-(j["blow"]+j["hit"]))) for j in ginfo]
            # # # print(priority_value)

            # どのグループから探索するかを決める。簡略化のため、常にハズレ発見を優先する。
            # ゼロチェッカーは、blowとhitの和が0になるか、lengthとblow+hitの差が0になったときに0を返す（探索の必要がなくなったグループを意味する）
            priority_value = [(1000 - 100 * j["leng"] - (j["blow"]+j["hit"])) * self.zero_checker(
                (j["blow"]+j["hit"])*(j["leng"]-(j["blow"]+j["hit"])))*self.curse(j["gnum"]) for j in ginfo]
            # if winfo["special_mode"] == 1:
            #     for j in gnifo:
            #         if j["gnum"] ==3:
            # 全てのpriority_valueが0になっていたら、このターンに来る前のinfo_updaterでphaseが4になっているはずであり、ここには来ていないはず。
            if sum(priority_value) == 0:
                print("error:phaseが更新されていませんby fugaku")
                
            target_gnum_order = priority_value.index(max(priority_value))
            target_gnum = ginfo[target_gnum_order]["gnum"]
            default_length = ginfo[target_gnum_order]["leng"]
            target_length = max(
                math.ceil(default_length / 2), 5 - winfo["noob"])

            """特別モードの中盤への分岐
            0~4,5~9,a~e,fそれぞれにblowがある場合(ハズレなし、つまりtarget_length=5の場合)は、特別な処理をする必要がある。
            具体的には、確定blowである「f」を「ハズレ」として用い、後で全体のblow数を1追加する。"""
            # 場合分けが簡単そうだったから、全パターン記述した。
            if target_length == 5:
                winfo["special_mode"] = 1
                print("You are in special mode...")
                self.get_gnum()
                if target_gnum == 0:
                    guess_mid_str = "f0123"
                    self.ram.append({"turn": winfo["turn"], "group_member": [0, 1, 2, 3], "non_group_member": [
                        4], "group_qty": 1, "gnum0": 0, "gnum1": 3, "gnum2": -1, "guess_mid_list": [15, 0, 1, 2, 3]})
                    for i in [0, 1, 2, 3]:
                        ninfo[i]["gnum"] = 3
                elif target_gnum == 1:
                    guess_mid_str = "f5678"
                    self.ram.append({"turn": winfo["turn"], "group_member": [5, 6, 7, 8], "non_group_member": [
                        9], "group_qty": 1, "gnum0": 1, "gnum1": 3, "gnum2": -1, "guess_mid_list": [15, 5, 6, 7, 8]})
                    for i in [5, 6, 7, 8]:
                        ninfo[i]["gnum"] = 3
                else:
                    guess_mid_str = "fabcd"
                    self.ram.append({"turn": winfo["turn"], "group_member": [10, 11, 12, 13], "non_group_member": [
                        14], "group_qty": 1, "gnum0": 2, "gnum1": 3, "gnum2": -1, "guess_mid_list": [15, 10, 11, 12, 13]})
                    for i in [10, 11, 12, 13]:
                        ninfo[i]["gnum"] = 3
                    if target_gnum != 2:
                        print("message: target_gnumの値がおかしい（続行可能）")
                return (guess_mid_str)

            """通常モードの中盤続き"""
            # 新たなグループをつくる。探索された側とされなかった側で、2つのグループに分割される。分割後の長さが1の場合、グループ解除(gnum=-1)する。
            if target_length == 1:
                gnum1 = -1
            else:
                gnum1 = self.get_gnum()
            if default_length - target_length <= 1:
                gnum2 = -1
            else:
                gnum2 = self.get_gnum()  # ターゲットの情報を集めるための空リスト
            target = []
            # メンバーの記録用リスト
            member = []
            bocchi = []
            # 探索したい数字を登録し、ninfoのgnumを更新する。
            # ninfo更新は、できればinfo_updaterに移したほうがいい
            for i in range(16):
                if ninfo[i]["gnum"] == target_gnum and len(target) < target_length:
                    target.append(ninfo[i])
                    ninfo[i]["gnum"] = gnum1
                    member.append(ninfo[i]["number"])
                elif ninfo[i]["gnum"] == target_gnum:
                    ninfo[i]["gnum"] = gnum2
                    bocchi.append(ninfo[i]["number"])

            # 【未実装事項（機能拡張）】
            # 終盤のように、それぞれの位置の位置情報値(0,1,2)の合計が大きい順に（つまり、より多くのターゲットに使われている数字から順に）選ぶようにする
            # 余ったスペースに、確定blowを乱入させたい（これは負担が膨大なので無理そう）

            # どの位置にどの数字を入力するかを決める。
            # 偏らないように、どの位置から決めるかはターンによって異なるようにする
            input_order = [(winfo["turn"] + _ - 3) % 5 for _ in range(5)]
            for p in input_order:
                for k in range(len(target)):
                    if target[k][p] == 2:  # ==1のときも考慮したい（未実装）
                        pass
                    else:
                        guess_mid_list[p] = target[k]["number"]
                        target.pop(k)
                        # print(guess_mid_list)
                        break  # これで二重に登録してしまうケースを防げるはず
            # if target != []:
            #     for p in input_order:
            #         for k in range(len(target)):
            #             print("judging"+str(p)+str(k))
            #             if target[k][p] == 1:  #←ここが1になってる、これで位置情報が1のケースも考慮できるか？後で確認
            #                 pass
            #             else:
            #                 guess_mid_list[p] = target[k]["number"]
            #                 target.pop(k)
            #                 print("written")
            #                 print(guess_mid_list)
            #                 print(target)
            #                 break #これで二重に登録してしまうケースを防げるはず
            # 上記のやり方で決まらなかった場合。位置情報に関係なく決める。
            if target != []:
                for p in input_order:
                    for k in range(len(target)):
                        guess_mid_list[p] = target[k]["number"]
                        target.pop(k)
                        break  # これで二重に登録してしまうケースを防げるはず

            # 余ったところにハズレを入れる
            # ハズレ一覧のリストをつくる
            nooblist = []
            noobcount = 0
            for i in range(16):
                if ninfo[i]["cond"] == 9:
                    nooblist.append(ninfo[i]["number"])
            for p in range(5):
                if guess_mid_list[p] == -1:
                    # nooblistの範囲外までnoobcountをforループしてそう
                    guess_mid_list[p] = ninfo[nooblist[noobcount]]["number"]
                    noobcount += 1
            # 最後に、list型のguessをstr型にする
            for p in range(5):
                guess_mid_str += str(hex(guess_mid_list[p]))[2]

            # 次のinfo_updateで処理するために必要な情報を、グローバル関数に残す
            self.ram.append({"mode": "normal", "turn": winfo["turn"], "group_member": member, "non_group_member": bocchi, "group_qty": len(
                list(filter(self.pos, [gnum1, gnum2]))), "gnum0": target_gnum, "gnum1": gnum1, "gnum2": gnum2, "guess_mid_list": guess_mid_list})
            return (guess_mid_str)

            """終盤"""
        elif winfo["phase"] == 4:
            guess_mid_list = copy.copy(self.hit_list)
            guess_mid_str = ""
            memb = ginfo[-1]["final_member"]
            posi = ginfo[-1]["position"]
            hits = 5 - len(memb)

            # 並び替えの優先順位を決める。残り場所の候補が少ない順、つまり、位置情報の和の少ない順に行う。
            order_value = []
            for i in memb:
                memo_order = 0
                for p in range(5):
                    memo_order += ninfo[i][p]
                order_value.append([i, memo_order])
            order_value.sort(key=lambda x: x[1], reverse=True)
            order = [order_value[i][0] for i in range(len(order_value))]

            # hits=0のとき、targets=3にしてもいいかも（時間あれば）。hits=3ならガチャ（位置情報次第では確定）
            # 位置情報を見て、多く残ってるようであればそこから探索するのが良さそう…
            if hits < 3:
                targets = 1
            elif hits == 3:
                targets = 2
            else:
                print("error:hit4...?blowの組間違えてない？")
                winfo["phase"] -= 1

            counter = 0
            reg_count = 0
            memo_mem = []
            memo_pos = []
            while counter < 60:
                for k in order:
                    for p in posi:
                        if reg_count >= targets:
                            counter += 999
                            break
                        if ninfo[k][p] == 2:
                            pass
                        else:
                            guess_mid_list[p] = ninfo[k]["number"]
                            reg_count += 1
                            memo_mem.append(k)
                            memo_pos.append(p)
                            posi.remove(p)
                            order.remove(k)
                            break
                counter += 1

            # ハズレ一覧のリストをつくる
            nooblist = []
            noobcount = 0
            for i in range(16):
                if ninfo[i]["cond"] == 9:
                    nooblist.append(ninfo[i]["number"])

            for p in range(5):
                if guess_mid_list[p] < 0:
                    guess_mid_list[p] = nooblist[p]
            self.ram.append({"hits": hits, "done_number": memo_mem,
                             "done_position": memo_pos})
            # 最後に、list型のguessをstr型にする
            for p in range(5):
                guess_mid_str += str(hex(guess_mid_list[p]))[2]

            return (guess_mid_str)
        else:
            print("unexpected error 101")
            

    def info_update(self, ninfo, ginfo, hist, winfo):
        new_hit_checker = 0

        """序盤の処理"""
        if winfo["phase"] < 3:
            # 位置情報(ninfo)の更新
            guessa = hist[-1]["guess"]
            hita = hist[-1]["hit"]
            blowa = hist[-1]["blow"]
            # その回の調査で、hit=0場合は、同じ位置に数字が来ないことが確定する。このとき、それぞれの位置の情報を「2」とする。
            if hita == 0:
                for order, num in enumerate(guessa):
                    ninfo[int(num, base=16)][order] = 2
            # その回の調査で、hitが発生した場合は、その位置に数字が来る可能性がある。しかし、その回の他の数字がhitし、他全てがblowであった場合、その位置情報は有効となる。この状態の位置情報は「1」とする（この状態では情報に価値はない）
            else:
                for order, num in enumerate(guessa):
                    if ninfo[int(num, base=16)][order] < 2:
                        ninfo[int(num, base=16)][order] = 1
            # 発見blow数の更新
            winfo["rough_blow"] += hita + blowa
            # 偵察した数について、ninfoのblow可能性の更新
            if hita + blowa == 0:
                for num in guessa:
                    ninfo[int(num, base=16)]["cond"] = 9
            else:
                for num in guessa:
                    ninfo[int(num, base=16)]["cond"] = 1
            # グループ情報の更新
            group_num = self.get_gnum()
            for num in guessa:
                ninfo[int(num, base=16)]["gnum"] = group_num
            ginfo.append({"gnum": group_num, "leng": 5,
                         "blow": blowa, "hit": hita})
            # 「56789」までで5blow出尽くした場合の処理
            if winfo["phase"] < 2 and winfo["rough_blow"] == 5:
                for num in range(16):
                    # これが0のときは、一回も偵察されていないことを示す。5blowが出尽くした時点で一回も偵察されていないのはハズレ確定
                    if ninfo[num]["cond"] == 0:
                        ninfo[num]["cond"] = 9
                        winfo["phase"] = 2
            # 「abcde」まで終わったとき、fがどうなってるかを判別
            elif winfo["phase"] == 2:
                if winfo["rough_blow"] == 5:
                    ninfo[15]["cond"] = 9
                elif winfo["rough_blow"] == 4:
                    ninfo[15]["cond"] = 1
                    winfo["confirmed_blow_and_hit"] += 1
                    self.blow_list.append(15)
                else:
                    print("unexpected error 003")
                    
            winfo["phase"] += 1

            """中盤の処理"""
        elif winfo["phase"] == 3:
            # 探索対象のグループ（分割前）を、hit,blowを一時期録してginfoから削除
            for i in range(100):
                try:
                    if ginfo[i]["gnum"] == self.ram[0]["gnum0"]:
                        hit_past = ginfo[i]["hit"]
                        blow_past = ginfo[i]["blow"]
                        ginfo.pop(i)
                except IndexError:
                    break

            # 「探索対象グループ」のうち、「探索された部分（表）」と「探索されなかった部分（裏）」の2つに分けて考える。
            # 例:「01234」を探索対象とし、「012」を探索した場合、「012」が表、「34」が裏
            """「表」の処理"""
            # 現状、探索対象グループ以外の数字は全てハズレにしているので、（グループ外のBlow確定の数字を乱入させることはしていない、ということ）
            #　「5文字全体のhit,blow」＝「表のhit,blow」となる。
            guessb = self.ram[0]["guess_mid_list"]
            memberb = self.ram[0]["group_member"]
            hitb = hist[-1]["hit"]
            blowb = hist[-1]["blow"]

            # 「Special mode」の場合。hit+blowが最小になるグループを探索したので、「探索対象グループ」(01234とか)のhit+blowは必ず1。
            # fはblow確定なので、hitb+blowbは必ず1か2になる。
            if winfo["special_mode"] == 1:
                # hitb+blowbが1なら脱出、2なら残留（ゲーム終了までspecial_modeのまま）

                if hitb + blowb == 1:
                    winfo["special_mode"] = 0
                # 今回の処理ではhitかblowの値を1引く(ハズレ代わりに入れたfが確定blowなので）。
                """「hitbが1以上のときはhitbから1引く」としてしまうと、hitが発生したにも関わらず位置情報に2が入力されてしまう場合がある
                これを防ぐために、blowbから常に1引くことにする。
                blowbが使用される箇所は、以下の3種類
                blowb+hitbの形（これは、hitbから引いても変わらないので問題なし）
                この回からは絶対に分岐しない位置
                ginfoへの登録
                おそらく、ginfo以外では問題を起こさないはず。"""
                blowb -= 1
                # このループには1度しか入らないようにする必要があるので、値を変更しておく。
                winfo["special_mode"] = 2

            # その回の調査で、hit=0場合は、同じ位置に数字が来ないことが確定する。このとき、それぞれの位置の情報を「2」とする。
            if hitb == 0:
                for order, num in enumerate(guessb):
                    ninfo[num][order] = 2
            # その回の調査で、hitが発生した場合は、その位置に数字が来る可能性がある。しかし、その回の他の数字がhitし、他全てがblowであった場合、その位置情報は有効となるため、情報を保存したい。そこで、この状態の位置情報は「1」とする（この状態では情報に価値はない）
            else:
                for order, num in enumerate(guessb):
                    if ninfo[num][order] < 2:
                        ninfo[num][order] = 1
            # hit,blowなしの場合
            if hitb + blowb == 0:
                for num in memberb:
                    ninfo[num]["cond"] = 9
            # 全てblow以上確定の場合
            elif hitb + blowb == len(memberb):
                # 全てhit確定の場合
                if blowb == 0:
                    for num in memberb:
                        order = guessb.index(num)
                        ninfo[num]["cond"] = 3
                        # 位置情報更新。一度全てを2にして、hit位置のみ0にする
                        for p in range(5):
                            ninfo[num][p] = 2
                        ninfo[num][order] = 0  # hit確定でも位置情報は2にしてる。3にしてもいいかも？
                        # hitlist,blowlist等を更新
                        self.blow_list.append(num)
                        self.hit_list[order] = num
                        winfo["confirmed_hit"] += 1
                        winfo["confirmed_blow_and_hit"] += 1
                        new_hit_checker = 1
                # そうでない場合（blow確定）
                else:
                    for num in memberb:
                        ninfo[num]["cond"] = 2
                        self.blow_list.append(num)
                        winfo["confirmed_blow_and_hit"] += 1
            # 探索続行の場合
            else:
                for num in memberb:
                    ninfo[num]["cond"] = 1
            # 分裂後のグループをginfoに登録（分裂後の大きさが2以上場合のみ）
            if len(memberb) >= 2:
                ginfo.append({"gnum": self.ram[0]["gnum1"], "leng": len(
                    memberb), "hit": hitb, "blow": blowb})

            """「裏」の処理"""
            # guessb,hitb,blowbの値を更新した後は、「表」の処理と似ているように思うが、いくつか違う点があるので注意。
            guessb = self.ram[0]["guess_mid_list"]
            memberb = self.ram[0]["non_group_member"]
            hitb = hit_past - hitb
            blowb = blow_past - blowb
            # 「裏」については、実際に探索したわけではないので、位置情報は更新できない。
            # hit,blowなしの場合
            if hitb + blowb == 0:
                for num in memberb:
                    ninfo[num]["cond"] = 9
            # 全てblow以上確定の場合
            elif hitb + blowb == len(memberb):
                # 「表」と異なる処理(裏では、hit確定は存在しない)
                # （blow確定）
                for num in memberb:
                    ninfo[num]["cond"] = 2
                    self.blow_list.append(num)
                    winfo["confirmed_blow_and_hit"] += 1
            # 探索続行の場合
            else:
                for num in memberb:
                    ninfo[num]["cond"] = 1
            # 分裂後のグループをginfoに登録（分裂後の大きさが2以上場合のみ）
            # 「表」の処理と異なる（gnum1とgnum2）
            if len(memberb) >= 2:
                ginfo.append({"gnum": self.ram[0]["gnum2"], "leng": len(
                    memberb), "hit": hitb, "blow": blowb})

            """共通の処理（中盤終了判定）"""
            # 「探索の必要がないグループについては0になる関数」であるpriority_valueを使い、全てのグループについて0になった場合に終了とする。
            priority_value = [(1000 - 100 * j["leng"] - (j["blow"]+j["hit"])) * self.zero_checker(
                (j["blow"]+j["hit"])*(j["leng"]-(j["blow"]+j["hit"]))) for j in ginfo]
            if sum(priority_value) == 0:
                winfo["phase"] = 4
                # もし終了してたら、既存のginfoを全て削除し、確定blowのうちhit確定していない部分のみで構成したグループをginfoに登録
                final_position = []
                ginfo = []
                gnum = self.get_gnum()
                final_member = copy.copy(self.blow_list)
                # self.hit_listに記載がない(つまり-1)場合、その位置をfinal_positionに追加し、final_memberから消す
                for p, num in enumerate(self.hit_list):
                    if num < 0:
                        final_position.append(p)
                    else:
                        final_member.pop(final_member.index(num))
                ginfo.append({"gnum": gnum, "leng": len(final_member), "hit": 0, "blow": len(
                    final_member), "final_member": final_member, "position": final_position})
                # グループ情報をninfoに登録
                for i in final_member:
                    ninfo[i]["gnum"] = gnum

            """終盤の処理"""
            # 終盤に入った瞬間の処理はすでに終えているので、elifで繋いでOK
        elif winfo["phase"] == 4:
            hits_before = self.ram[0]["hits"]
            hits_after = hist[-1]["hit"]
            memb = self.ram[0]["done_number"]
            posi = self.ram[0]["done_position"]
            """
            hits=3以外のときは、探索数を1とすることを前提に作られている（簡単に拡張できるようにはしてある）。
            """
            if hits_after == hits_before:
                # hitを探せなかったとき。位置情報を更新して次へ。
                for _, i in enumerate(memb):
                    ninfo[i][posi[_]] = 2
            elif hits_after == hits_before + 1:
                if len(memb) == 1:
                    # hit確定
                    ninfo[memb[0]]["cond"] = 3
                    # 位置情報更新。一度全てを2にして、hit位置のみ0にする
                    for p in range(5):
                        ninfo[memb[0]][p] = 2
                    ninfo[memb[0]][posi[0]] = 0  # この３行いる？
                    # self.hit_list更新
                    self.hit_list[posi[0]] = memb[0]
                    winfo["confirmed_hit"] += 1
                    new_hit_checker = 1
                else:
                    print("hitが2以上増えてるゾ（その1）")
            elif hits_before == 3:
                pass
            else:
                print("hitが2以上増えてるゾ（その2）")

            # ginfoの更新。基本的には、中盤の最後にやったのと同じ
            final_position = []
            ginfo = []
            gnum = self.get_gnum()
            final_member = copy.copy(self.blow_list)
            # self.hit_listに記載がない(つまり-1)場合、その位置をfinal_positionに追加し、final_memberから消す
            for p, num in enumerate(self.hit_list):
                if num < 0:
                    final_position.append(p)
                else:
                    final_member.pop(final_member.index(num))
            ginfo.append({"gnum": gnum, "leng": len(final_member), "hit": 0, "blow": len(
                final_member), "final_member": final_member, "position": final_position})
            # グループ情報をninfoに登録
            for i in final_member:
                ninfo[i]["gnum"] = gnum

        else:
            print("error:phaseがおかしいです。")
            

        # 共通の更新事項
        # ハズレ数の更新
        winfo["noob"] = sum([i == 9 for i in [j["cond"] for j in ninfo]])
        # hit発生時の処理(全ての数字の位置情報を更新)
        if new_hit_checker == 1:
            for p in range(5):
                if self.hit_list[p] != -1:
                    for i in range(16):
                        ninfo[i][p] = 2
        new_hit_checker = 0
        # ターン数の更新
        winfo["turn"] += 1

        # ninfo,ginfoは辞書表記だと見づらいのでprintするときはlist化
        nlist = ([list(ninfo[j].values()) for j in range(16)])
        glist = ([list(ginfo[p].values()) for p in range(len(ginfo))])
        # 終盤だけ辞書表記で表示する場合は↓を有効化
        # if winfo["phase"] == 4:
        #     print(ninfo)
        #     print(ginfo)
        # else:
        if self.print_mode == "on":
            print(nlist)
            print(glist)
            print(winfo)
            print(self.hit_list)
            print(self.blow_list)
        return ninfo, ginfo, hist, winfo


    def get_gnum(self):
        """
        新たなグループナンバーgnumを得る関数
        """
        if self.wholeinfo["phase"] >= 4:
            gnum_boost = 50
        elif self.wholeinfo["phase"] < 4:
            gnum_boost = 0
        else:
            print("error code 494")
        self.gnum_count += 1
        return self.gnum_count + gnum_boost

    def define_answer(self):
        """
        """
        # if type(defined_answer) == str and len(defined_answer) == 5:
        #     self.ans_str = defined_answer
        #     return defined_answer
        # else:
        digit_kari = 0
        count = 0
        check = 0
        while count < 5:
            if count == 0:
                self.ans_list[count] = random.randint(0, 15)
                count += 1
            else:
                digit_kari = random.randint(0, 15)
                for j in range(count):
                    if self.ans_list[j] == digit_kari:
                        check = -1
                if check == 0:
                    self.ans_list[count] = digit_kari
                    count += 1
                else:
                    check = 0
        for i in range(5):
            self.ans_str += str(hex(self.ans_list[i]))[2]
        print("answer:"+self.ans_str)  # あらかじめ答えを知りたいときのみ有効化する

    def ending(self):
        # それぞれのステージにかかったターン数を計算
        try:
            used_turn = []
            for i in range(len(self.game_record) - 1):
                if self.game_record[i] != 3 and self.game_record[i + 1] == 3:
                    used_turn.append(i + 1)
                elif self.game_record[i] != 4 and self.game_record[i + 1] == 4:
                    used_turn.append(i + 1)
            # ズレを補正
            used_turn[0] += 2
            used_turn[1] -= 2
            used_turn.append(len(self.game_record) - sum(used_turn))
            if self.print_mode == "on":
                print()
                print("ANSWER: "+self.ans_str)
                print("CONGRATULATIONS!!!!")
                print("　＊　 　　　+　　　　巛 ヽ")
                print("　　　　　　　　　　　　〒　!　　　+　　　　。　　　　　+　　　　。")
                print("　 　　　　+　　　　。　 | 　|")
                print("　　　＊　 　　　+　　 /　/　　　イヤッッホォォォオオォオウ！")
                print("　　　　　　 ∧＿∧ /　/")
                print("　　　　　　（´∀｀　/　/　+　　　　。　　　　　+　　　　。　　　＊")
                print("　　　　　　,-　　　　　ｆ")
                print("　　　　　 / ｭﾍ　　　　| ＊　 　　　+　　　　。　　　　　+　　　。　+")
                print("　　　　　〈＿｝ ）　　　|")
                print("　　　　　　　 /　　　　! +　　　　。　　　　　+　　　　+　　　　　＊")
                print("　　　　　　 ./　　,ﾍ　 |")
                print("　ｶﾞﾀﾝ　||| j　　/　|　 | |||")
                print("――――――――――――")
                print("You have solved at " +
                    str(self.wholeinfo["turn"]-1) + " turns!")
                print("      Early phase: "+str(used_turn[0]) + " turns")
                print("      Middle phase:"+str(used_turn[1]) + " turns")
                print("      FINAL phase: "+str(used_turn[2]) + " turns")
                print("                     T H A N K   Y O U   F O R   P L A Y I N G ! ! !")
            # 別ファイルにゲームデータを書き込み
            path_w = 'self.game_record.txt'
            s = "\n["+self.ans_str + ", " + \
                str(sum(used_turn))+", " + str(used_turn)+"]"
            with open(path_w, mode='a') as f:
                f.write(s)
        except:
            pass

    def run(self):
        if self.print_mode == "off":
            print("Autoplay is on progress...")
        while True:
            try:
                room = random.randint(8400, 8800)
                drun = SendReceive(room_id=room)
                drun.enter_room()
                d2run = SendReceive(room_id=room, player_name="D2")
                d2run.enter_room()
                break
            except KeyError:
                pass
        drun.get_room()
        drun.get_table()
        drun.post_hidden(ans="1a2b3")
        # 指定する場合はdefine_answer()のカッコ内に入力。ランダムでよい場合は""と入力
        self.define_answer()
        d2run.post_hidden(ans=self.ans_str)
        drun.get_table()
        # 368af

        while True:
            # drun.post_guess("12345")
            try:
                drun.post_guess(self.fugaku(
                    self.numberinfo, self.groupinfo, self.history, self.wholeinfo))
            except:
                drun.post_guess(random.sample(5))
            result = drun.get_table()['table'][-1]
            self.history.append(result)
            # 情報のアップデート
            self.numberinfo, self.groupinfo, self.history, self.wholeinfo = self.info_update(
                self.numberinfo, self.groupinfo, self.history, self.wholeinfo)

            if self.print_mode == "on":
                for tt in range(len(self.history)):
                    print(self.history[tt])
            self.game_record.append(self.wholeinfo["phase"])
            """クリア判定"""
            if self.history[-1]["hit"] == 5:
                self.ending()
                """ここで終了"""
                return self.history

            if self.print_mode == "on":
                print()
                print("--------------------------------------------")
                print("You are in "+self.phase_list[self.wholeinfo["phase"]])
                print("TURN" + str(self.wholeinfo["turn"]))
            elif self.print_mode == "off":
                if self.wholeinfo["turn"] % 3 == 0:
                    print("TURN" + str(self.wholeinfo["turn"]))

            # 文字の入力
            # guess2 = input("player1 guess ->")
            """ショートカット
            中盤まで：3
            終盤まで：4
            最後まで：5"""
            if self.wholeinfo["phase"] < 5:
                guess2 = 12345
            else:
                guess2 = input("player1 guess ->")
            if guess2 == "":
                guess2 = 12345
            d2run.post_guess(guess2)
            drun.get_table()
            # self.ramの消去
            self.ram = []
