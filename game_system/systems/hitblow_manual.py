import judge_manual
# hitblow判定のみ
# guessがおかしい（数字被りなど）かどうかの判定は、事前に行う必要がある


class HitblowManual():

    def run():
        """数当てゲームのメイン
            """
        answer = input("input answer ->")

        runner = judge_manual.JudgeManual(answer, "12345", 5, 16)
        hit, blow = runner.run()
        return hit, blow


#     # 直接入力したときだけ適用できるようにするためのif文（importではできない）
# if __name__ == "__main__":
#     run()
