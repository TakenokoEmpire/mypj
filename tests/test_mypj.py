import pytest
from mypj.mypj import main
from mypj.number_guess import NumberGuess


def test_main() -> None:
    """
    main()関数のテスト
    分割統治法で解いたときの回数をチェックする
    """
    runner = NumberGuess(min_ans=0, max_ans=99, max_stage=100)
    stage, history = runner.run("binary")

    # assert stage == 5
