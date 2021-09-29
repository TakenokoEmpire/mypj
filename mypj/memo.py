from send_receive import SendReceive
drun = SendReceive(room_id=4004)
d2run = SendReceive(room_id=4004, player_name="D2")

table_data = drun.get_table()
state = table_data["state"] #対戦状況
player = table_data["now_player"] #今のプレイヤー
judge_post = drun.post_guess(guess="012a4").status_code #予想の登録に成功したか否かの判断
table_data = drun.get_table() #対戦テーブルの情報の取得
table = table_data["table"][-1] #自分の最新の予想
hit = table["hit"] #hitの数
blow = table["blow"] #blowの数
winner = table_data["winner"] #勝者
turn = table_data["game_end_count"] #ゲーム終了までのターン数
opponent_table = table_data["opponent_table"] #相手の予想の履歴