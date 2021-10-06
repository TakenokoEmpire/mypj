from systems import initialize
from systems import town
from systems import battle


def run():
    print("1:街")
    print("2:ダンジョン")
    print("9:データ削除")
    choice = input("どこ行く？->")
    if choice == "1":
        rest = town.Town("normal", 0)
        rest.main()

    if choice == "2":
        dungeon_type = input("choose dungeon type [boss/normal] ->")
        dungeon_num = input("choose dungeon number ->")
        vs = battle.Battle(dungeon_type, int(dungeon_num))
        vs.main()

    if choice == "9":
        delete = initialize.Initialize()
        delete.confirm()


run()
