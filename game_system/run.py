# from system import mypjg
from systems import battle
checknumber = 1


def run() -> None:
    """数当てゲームのメイン
    """
    dungeon_num = input("choose dungeon number ->")
    vs = battle.Battle(int(dungeon_num))
    vs.main()
    

run()