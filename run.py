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
print("＿人人人人人人人＿")
print("＞ HIT AND BLOW ＜")
print("￣Y^Y^Y^Y^Y^Y^Y^￣")
name = input("            Press ENTER...")

#三浦専用
if name == "developer":
    pw = input("password ->")
    if pw == "1234":
        print("【DEVELOPER'S MODE】")
        print("version list: \n 0:Backup \n 1:失敗作 \n 2:Hit and Blow")
    else:
        print("GAME OVER")
        exit()

#ショートカット
elif name == "ss":
    from mypj3 import number_guess3
    from mypj3 import mypj3
    checknumber = 1

    def run() -> None:
        """数当てゲームのメイン
        """
        mypj3.main()

#正規ルート
else:
    print("version list: \n  1:動画に沿って作成したゲームプログラム \n  2:Hit and Blow \n  3:BATTLE(Hit and Blow)")


while checknumber == 0:

    version = input("choose version ->")
    if version == "3":
        checknumber += 1

        print("game mode list: \n  0:CPU \n  1:Player \n  2:Player VS CPU \n  3:Player VS Player")
        gmode = input("choose game mode ->")
        if int(gmode) == 3: #numberguess内でもこれを使用したい。どうすればよい？
            from mypj3 import number_guess3
            from mypj3 import mypj3

            def run() -> None:
                """数当てゲームのメイン
                """
                mypj3.main()
        else:
            print("未実装です")
            exit()



    if version == "2":
        checknumber += 1
        print("game mode list: \n  0:CPU \n  1:Player \n  2:Player VS CPU \n  3:Player VS Player")
        gmode = input("choose game mode ->")
        if gmode == "1":
            from mypj2 import number_guess2
            from mypj2 import mypj2
            def run() -> None:
                """数当てゲームのメイン
                """
                mypj2.main()
        else:
            print("未実装です")
            exit()



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
