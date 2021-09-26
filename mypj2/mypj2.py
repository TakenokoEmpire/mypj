# coding: UTF-8
"""(ry

"""
import argparse
from . import number_guess2



def get_parser() -> argparse.Namespace:
    """コマンドライン引数を解析したものを持つ
    """

    parser = argparse.ArgumentParser(description="数当てゲーム")

    parser.add_argument('--min_ans', default=0x0)
    parser.add_argument('--max_ans', default=0xf)
    parser.add_argument('--max_stage', default=1000)
    parser.add_argument('--ans', default=None)
    parser.add_argument('--mode', default="manual")

    args = parser.parse_args()
    return args


def main() -> None:
    """数当てゲームのメイン
    """
    args = get_parser()
    min_ans = int(args.min_ans)
    max_ans = int(args.max_ans)
    max_stage = int(args.max_stage)
    mode = args.mode

    if args.ans is not None:
        ans = int(args.ans)
        runner = number_guess2.NumberGuess(
            min_ans=min_ans, max_ans=max_ans, max_stage=max_stage, ans=ans)
    else:
        runner = number_guess2.NumberGuess(
            min_ans=min_ans, max_ans=max_ans, max_stage=max_stage)
    stage, history = runner.run(mode=mode)

    """ここで、ansを決める"""
