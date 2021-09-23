# number_guess2.py
import random
from typing import List, Tuple, Optional
# 入力は16^5-1までの「10進の数字」で（「0x3e3e3」等の形は不可。必ず10進に直す）


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
        self.max_stage = max_stage
        self.stage = 0
        self.history: List[int] = []
        self.right = self.max_ans
        self.left = self.min_ans

        if ans is not None:
            self.ans = ans
        else:
            self.ans = self._define_answer()

    def run(self, mode="manual") -> Tuple[int, List[int]]:
        """
        """
        if mode == "linear":
            self._play_game_auto_linear()
        elif mode == "binary":
            self._play_game_auto_binary()
        else:
            self._play_game_manual()
        self._show_result()
        self._get_history()
        return self._get_history()

    def _play_game_manual(self) -> None:
        """手入力で遊ぶモード
        16進5桁に対応
        :rtype: None
        :return: なし
        """
        while self.stage < self.max_stage:
            print("残り{}回".format(self.max_stage - self.stage))
            no = self._get_your_guess()
            self.history.append(no)
            self.stage += 1
            hit = 0
            blow = 0

            # hit数とblow数を判定
            for i in range(5):
                if self.ans[i] == no[i]:
                    hit += 1
                else:
                    for j in range(5):
                        if self.ans[i] == no[j]:
                            blow += 1
                            break

            # 正誤判定
            if no != self.ans:
                print('[hit,blow] = '), print([hit, blow])
            else:
                print('正解')
                print(self.ans)
                break



    # def _play_game_auto_linear(self) -> None:
    #     no = (self.min_ans + self.max_ans) // 2
    #     while self.stage < self.max_stage:
    #         print("残り{}回".format(self.max_stage - self.stage))
    #         self.history.append(no)
    #         self.stage += 1

    #         if no > self.ans:
    #             print("--もっと小さいよ")
    #             no -= 1
    #         elif no < self.ans:
    #             print("--もっと大きいよ")
    #             no += 1
    #         else:
    #             print('--正解')
    #             break

    # def _play_game_auto_binary(self) -> None:
    #     while self.stage < self.max_stage:
    #         mid = self.right + ((self.left - self.right) // 2)
    #         no = mid
    #         print("残り{}回".format(self.max_stage - self.stage))

    #         self.history.append(no)
    #         self.stage += 1

    #         if no > self.ans:
    #             print("--もっと小さいよ")
    #             self.right = mid - 1
    #         elif no < self.ans:
    #             print("--もっと大きいよ")
    #             self.left = mid + 1
    #         else:
    #             print('正解')
    #             break

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
        if self.stage <= self.max_stage - 1:  # この-1は必要なはず
            print("{}回で正解".format(self.stage))
        else:
            print("正解は{}".format(self.ans))

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
        # print(ans16) #あらかじめ答えを知りたいとき
        return ans16
