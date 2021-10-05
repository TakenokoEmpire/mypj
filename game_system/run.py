# from system import mypjg
from systems import boss
checknumber = 1


def run() -> None:
    """数当てゲームのメイン
    """
    dungeon_type = input("choose dungeon type [boss/normal] ->")
    dungeon_num = input("choose dungeon number ->")
    vs = boss.Battle(dungeon_type, int(dungeon_num))
    vs.main()


run()
