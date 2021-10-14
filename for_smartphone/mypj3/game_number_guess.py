import random
from typing import List, Tuple, Optional


class NumberGuess:
    def __init__(self, min_ans: int = 0, max_ans: int = 9, max_stage: int = 5, ans: Optional[int] = None) -> None:
        """コンストラクタ
        以下略
        """
        self.min_ans = min_ans
        self.max_ans = max_ans
        self.max_stage = max_stage  # 使ってない
        self.stage = 0  # stageの偶奇でプレイヤーを識別　「○回目で正解」はstage//2に変更する
        self.history: List[int] = []  # 偶数番目(0含む)がPlayerA、奇数番目がPlayerBの記録となる
        self.right = self.max_ans
        self.left = self.min_ans
        self.player = ["human", "human"]
        self.ans = [0, 0, 0, 0, 0]

    def make_1ans(self, demand):
        if demand == 1:
            self.ans == [0, 1, 2, 3, 5]
        else:
            nums = list(range(16))
            self.ans = random.sample(nums, 5)

    def judge_guess(self, guess: List[int]):
        h = 0
        b = 0
        for i in range(len(guess)):
            if guess[i] == self.ans[i]:
                h += 1  # hがヒットの数
            else:
                if guess[i] in self.ans:
                    b += 1  # bがブローの数
        return h, b
