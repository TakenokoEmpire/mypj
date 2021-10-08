# number_guess3.py
import random
import numpy as np
from typing import List, Tuple, Optional
# 入力は16^5-1までの「10進の数字」で（「0x3e3e3」等の形は不可。必ず10進に直す）

# 動画ではmanualとautoでplay_gameが別れていたが、これを「ansとnoを入れたらhitとblowが出てくる関数」に統合。
# コンピュータによるnoの推測は、別の部分で行う。



class NumberGuess:
    """数当てゲーム
    **手入力で遊ぶモード、線形探索で解くモード、分割統治で解くモード**

    :param int min_ans: 出題範囲の上限値
    :param int max_ans: (ry 3-1-31参照
    :param int max_stage:
    :param int ans:
    :param int stage:
    :param List[int] history:
    :param int right:
    :param int left:
    """

    def __init__(self, min_ans: int = 0, max_ans: int = 9, max_stage: int = 5, ans: Optional[int] = None) -> None:
        """コンストラクタ
        以下略
        """
        self.min_ans = min_ans
        self.max_ans = max_ans
        self.max_stage = max_stage #使ってない
        self.stage = 0 #stageの偶奇でプレイヤーを識別　「○回目で正解」はstage//2に変更する
        self.history: List[int] = [] #偶数番目(0含む)がPlayerA、奇数番目がPlayerBの記録となる
        self.right = self.max_ans
        self.left = self.min_ans
        self.player = ["human","human"]
        self.ans = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]

        # if gmode == 2:
        #     self.player = ["human","com"]
        # elif gmode == 3:
        #     self.player = ["human","human"] 

        if ans is not None:
            self.ans = ans
        #答えを決める方法を指定。複数プレイヤーに対応した。
        #対戦相手（自分ではない）がcomの場合は、自分の番号がランダムで決まり、そうでない場合は自分の番号は相手(人)が指定する。
        #プレイヤー識別に「2で割った余り」を使っている箇所があるため、3人以上にする場合は注意
        else:
            print("player_0: " + self.player[0])
            print("player_1: " + self.player[1])
            for id in range(2):
                if self.player[(id + 1) % 2] == "human":
                    self.ans[id] = self._define_answer() #ここは要変更。getyourguess使うとよさそう
                elif self.player[(id + 1) % 2] == "com":
                    self.ans[id] = self._define_answer()

    def run(self, mode="manual") -> Tuple[int, List[int]]:
        """
        """
        judgement = 0
        while True:
            
            print("player_" + str(self.stage % 2) + "の番です")
            
            #playerの属性によってオートかマニュアルか変更するようにしたい。対Comでは難易度によって違うアルゴリズムを指定するようにしてもよいかも？
            if mode == "linear":
                judgement = self._play_game_auto_linear()
            elif mode == "binary":
                judgement = self._play_game_auto_binary()
            else:
                judgement = self._play_game_manual()
            print(judgement)
            self.stage += 1

            if judgement == 1:
                break
            else:
                continue
        self._show_result()
        self._get_history()
        return self._get_history()

    def _play_game_manual(self) -> int:
        """手入力で遊ぶモード
        関数起動するたびに、入力＋正誤判定1回のみ行うように改変
        （従来は、一度この関数を起動したらwhileで正解にたどり着くまでループしていた）
        制御はrun関数で行う。
        hitとblowをhistoryに残すようにすれば、「前回のHit数2以上で特殊スキル起動」みたいなことができるかも？
        """
        print("残り{}回".format(self.max_stage - self.stage))
        no = self._get_your_guess()
        self.history.append(no)

        # hit数とblow数を判定
        hit = 0
        blow = 0
        for i in range(5):
            if self.ans[self.stage%2][i] == no[i]:
                hit += 1
            else:
                for j in range(5):
                    if self.ans[self.stage%2][i] == no[j]:
                        blow += 1
                        break

        # 正誤判定
        if no != self.ans[self.stage%2]:
            print('[hit,blow] = '), print([hit, blow])
            return 0
        else:
            print('正解')
            print(self.ans)
            return 1


#16進5桁に対応させる。出力はリスト
#no16:空箱　no16str:noを16進数にした文字列　no16_len:noの16進の桁数(例:no = 0x002f3 の場合は3になる)
    def _get_your_guess(self) -> int:
        """
        """
        while True:
            no16 = [0,0,0,0,0]
            input_line16 = input("16進5桁で数字を入力してください->")
            try:
                no10 = int(input_line16, 16)
                no16str = str(hex(no10))
                no16_len = len(no16str)-2
                for i in range(no16_len):
                    no16[i + (5-no16_len)] = int(no16str[i+2], 16)
                print("入力は{}".format(input_line16))
                return no16
            except ValueError:
                print("16進5桁の数字ではありませんでした")

    def _show_result(self) -> None:
        """
        """
        print("{}回で正解".format((self.stage+1)//2))

        # if self.stage <= self.max_stage - 1:  # この-1は必要なはず
        #     print("{}回で正解".format(self.stage))
        # else:
        #     print("正解は{}".format(self.ans))

        print('----------------')
        print("show history")
        for i, x in enumerate(self.history):
            print("{}回目：{}".format(i+1, x))

    def _get_history(self) -> Tuple[int, List[int]]:
        """
        """
        return self.stage, self.history

    def _define_answer(self) -> List[int]:
        """
        1桁ずつ、0~15までの乱数を引いて決めていく
        count桁目の乱数(digit_kari)を引いた時、count-1桁目までの数字と重複がないかをチェック。
        　重複がなければ、引いた乱数(digit_kari)をans16[count]に保存。
        　重複してたらその桁の乱数を引き直す。        
        """
        ans16 = [0, 0, 0, 0, 0]
        digit_kari = 0
        count = 0
        check = 0
        while count < 5:
            if count == 0:
                ans16[count] = random.randint(self.min_ans, self.max_ans)
                count += 1
            else:
                digit_kari = random.randint(self.min_ans, self.max_ans)
                for j in range(count):
                    if ans16[j] == digit_kari:
                        check = -1
                if check == 0:
                    ans16[count] = digit_kari
                    count += 1
                else:
                    check = 0
        #print(ans16) #あらかじめ答えを知りたいときのみ有効化する
        return ans16

    def make_1ans(self):
        nums = list(range(16))
        return random.sample(nums, 5)
    
    def judge_guess(self,guess:List[int],ans:List[int]):
        h = 0
        b = 0
        for i in range( len(guess) ):
            if guess[i] == ans[i]:
                h += 1 # hがヒットの数
            else:
                if guess[i] in ans:
                    b += 1 # bがブローの数
        return h,b


