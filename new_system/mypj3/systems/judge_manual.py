# number_guess2.py
import random
from typing import List, Tuple, Optional
# 入力は16^5-1までの「10進の数字」で（「0x3e3e3」等の形は不可。必ず10進に直す）


class JudgeManual():
    """手入力モード
    ans,guess:x桁のstr
    """

    def __init__(self, ans, guess, length, max_ans):
        """コンストラクタ
        以下略
        """
        self.ans = ans
        self.min_ans = 0x0
        self.max_ans = max_ans
        self.length = length
        # self.stage = 0
        self.guess = guess
        self.hit = 0
        self.blow = 0
        # self.guess_list = self.make_list(self.guess, self.length)
        # self.history = []

    def run(self):
        """
        """
        self.judgement()
        # self.stage += 1
        # self.history.append([self.guess, self.hit, self.blow])
        return self.hit, self.blow  # , self.history, self.stage

    def judgement(self):
        # hit数とblow数を判定
        for i in range(5):
            if self.ans[i] == self.guess[i]:
                self.hit += 1
            else:
                for j in range(5):
                    if self.ans[i] == self.guess[j]:
                        self.blow += 1
                        break


def judgement(ans, guess, length, max_ans):
    # hit数とblow数を判定
    for i in range(5):
        if self.ans[i] == self.guess[i]:
            self.hit += 1
        else:
            for j in range(5):
                if self.ans[i] == self.guess[j]:
                    self.blow += 1
                    break

    # def make_list(self, target, length):
    #     """
    #     """
    #     target_list = []
    #     if type(target) == "str":
    #         for i in range(length):
    #             target_list[i] = int(target[i])
    #         return target_list
    #     # elif type(target) == "int":
    #     #     target_16str = str(hex(target))
    #     else:
    #         print("error from make_list()")
    #         return "false"

    # def judgement_list(self):
    #     # hit数とblow数を判定
    #     for i in range(5):
    #         if self.ans[i] == self.guess_list[i]:
    #             self.hit += 1
    #         else:
    #             for j in range(5):
    #                 if self.ans[i] == self.guess_list[j]:
    #                     self.blow += 1
    #                     break

    # # def _show_result(self) -> None:
    # #     """
    # #     """

    # #     # if self.stage <= self.max_stage - 1:  # この-1は必要なはず
    # #     #     print("{}回で正解".format(self.stage))
    # #     # else:
    # #     #     print("正解は{}".format(self.ans))

    # #     print('----------------')
    # #     print("show history")
    # #     for i, x in enumerate(self.history):
    # #         print("{}回目：{}".format(i+1, x))

    # # def _get_history(self) -> Tuple[int, List[int]]:
    # #     """
    # #     """
    # #     return self.stage, self.history

    # # def make_list(self, target, length):
    # #     """
    # #     """
    # #     target_list = []
    # #     if type(target) == "str":
    # #         for i in range(length):
    # #             target_list[i] = int(target[i])
    # #         return target_list
    # #     # elif type(target) == "int":
    # #     #     target_16str = str(hex(target))
    # #     else:
    # #         print("error from make_list()")
    # #         return "false"

    # #     #    try:
    # #     #         no10 = int(input_line16, 16)
    # #     #         no16str = str(hex(no10))
    # #     #         no16_len = len(no16str)-2
    # #     #         for i in range(no16_len):
    # #     #             no16[i + (5-no16_len)] = int(no16str[i+2], 16)
    # #     #         print("入力は{}".format(input_line16))
    # #     #         print(no16)
    # #     #         return no16
    # #     #     except ValueError:
    # #     #         print("16進5桁の数字ではありませんでした")

    # # def _define_answer(self) -> List[int]:
    # #     """
    # #     1桁ずつ、0~15までの乱数を引いて決めていく
    # #     count桁目の乱数(digit_kari)を引いた時、count-1桁目までの数字と重複がないかをチェック。
    # #     重複がなければ、引いた乱数(digit_kari)をans16[count]に保存。
    # #     重複してたらその桁の乱数を引き直す
    # #     """
    # #     ans16 = [0, 0, 0, 0, 0]
    # #     digit_kari = 0
    # #     count = 0
    # #     check = 0
    # #     while count < 5:
    # #         if count == 0:
    # #             ans16[count] = random.randint(self.min_ans, self.max_ans)
    # #             count += 1
    # #         else:
    # #             digit_kari = random.randint(self.min_ans, self.max_ans)
    # #             for j in range(count):
    # #                 if ans16[j] == digit_kari:
    # #                     check = -1
    # #             if check == 0:
    # #                 ans16[count] = digit_kari
    # #                 count += 1
    # #             else:
    # #                 check = 0
    # #     print(ans16)
    # #     # print(ans16) #あらかじめ答えを知りたいとき
    # #     return ans16
