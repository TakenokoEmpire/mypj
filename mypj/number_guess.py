import random
from typing import List, Tuple, Optional
# 動画の3-1-38まで反映、3-1-39から未着手


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
        while self.stage < self.max_stage:
            print("残り{}回".format(self.max_stage - self.stage))
            no = self._get_your_guess()
            self.history.append(no)
            self.stage += 1

            if no > self.ans:
                print("--もっと小さいよ")
            elif no < self.ans:
                print("--もっと大きいよ")
            else:
                print('正解')
                break

    def _play_game_auto_linear(self) -> None:
        no = (self.min_ans + self.max_ans) // 2
        while self.stage < self.max_stage:
            print("残り{}回".format(self.max_stage - self.stage))
            self.history.append(no)
            self.stage += 1

            if no > self.ans:
                print("--もっと小さいよ")
                no -= 1
            elif no < self.ans:
                print("--もっと大きいよ")
                no += 1
            else:
                print('--正解')
                break

    def _play_game_auto_binary(self) -> None:
        while self.stage < self.max_stage:
            mid = self.right + ((self.left - self.right) // 2)
            no = mid
            print("残り{}回".format(self.max_stage - self.stage))

            self.history.append(no)
            self.stage += 1

            if no > self.ans:
                print("--もっと小さいよ")
                self.right = mid - 1
            elif no < self.ans:
                print("--もっと大きいよ")
                self.left = mid + 1
            else:
                print('正解')
                break

    def _get_your_guess(self) -> int:
        while True:
            input_line = input("数字を入力してください->")
            input_str = input_line.split()[0]
            if input_str.isdecimal():
                no = int(input_str)
                print("入力は{}".format(no))
                return no
            else:
                print("数字ではありませんでした")

    def _show_result(self) -> None:
        if self.stage <= self.max_stage - 1:  # この-1は必要なはず
            print("{}回で正解".format(self.stage))
        else:
            print("正解は{}".format(self.ans))

        print('----------------')
        print("show history")
        for i, x in enumerate(self.history):
            print("{}回目：{}".format(i+1, x))

    def _get_history(self) -> Tuple[int, List[int]]:
        return self.stage, self.history

    def _define_answer(self) -> int:
        return random.randint(self.min_ans, self.max_ans)
