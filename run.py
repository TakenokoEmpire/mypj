from mypj import number_guess
from mypj import mypj


def run() -> None:
    """数当てゲームのメイン
    """
    mypj.main()

    # 直接入力したときだけ適用できるようにするためのif文（importではできない）
if __name__ == "__main__":
    run()