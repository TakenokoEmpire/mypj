# from mypj import number_guess
# from mypj import mypj


# def run() -> None:
#     """数当てゲームのメイン
#     """
#     mypj.main()

#     # 直接入力したときだけ適用できるようにするためのif文（importではできない）
# if __name__ == "__main__":
#     run()

checknumber = 0

name = input("Push ENTER")
if name == "ggg":
    #個人用メモ
    print("version list: \n 0:Backup \n 1:失敗作 \n2:Hit and Blow")
else:
    print("version list: \n 1:動画に沿って作成したゲームプログラム \n 2:Hit and Blow")

while checknumber == 0:

    version = input("choose version ->")
    if version == "2":
        checknumber += 1
        from mypj2 import number_guess2
        from mypj2 import mypj2

        def run() -> None:
            """数当てゲームのメイン
            """
            mypj2.main()

    elif version == "1":
        checknumber += 1
        from mypj import number_guess
        from mypj import mypj
        def run() -> None:
            mypj.main()

    elif version == "0":
        checknumber += 1
        from mypj0 import number_guess0
        from mypj0 import mypj0
        def run() -> None:
            mypj0.main()

    else:
        print('1,2のいずれかを入力')

    # 直接入力したときだけ適用できるようにするためのif文（importではできない）
if __name__ == "__main__":
    run()
