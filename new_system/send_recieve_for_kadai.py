import requests
from typing import Dict, Optional

# URL = "https://damp-earth-70561.herokuapp.com"
# player_id_D = "d2b8e778-20f3-4744-920b-6eb67eacc901"
# player_id_D2 = "6a9bbf53-df31-4e02-a585-e2173085606e"
# headers={"Content-Type": "application/json"}
session = requests.Session()


class SendReceive():

    def __init__(
            self,
            url: str = "https://damp-earth-70561.herokuapp.com",
            player_id: str = "e9eab746-bc3b-4200-884b-b3b8e7f5dac0",
            player_name: str = "D",
            room_id: Optional[int] = None,
            headers: Dict[str, str] = {"Content-Type": "application/json"}) -> None:

        self.url = url
        self.player_name = player_name
        if self.player_name == "D":
            self.player_id = player_id
        else:
            self.player_id = "6a9bbf53-df31-4e02-a585-e2173085606e"
        self.room_id = room_id
        self.headers = headers

    # すべての部屋情報の取得

    def get_all_room(self):
        url_get_all_room = self.url + "/rooms"
        result_all_room = session.get(url_get_all_room)
        print(result_all_room.status_code)
        print(result_all_room.json())

    # 対戦部屋へユーザを登録

    def enter_room(self):
        url_enter_romm = self.url + "/rooms"
        post_data_enter = {
            "player_id": self.player_id,
            "room_id": self.room_id
        }
        result_enter = session.post(
            url_enter_romm, headers=self.headers, json=post_data_enter)
        print(result_enter.status_code)
        print(result_enter.json())
        self.room_id = result_enter.json()["id"]

    # 指定した部屋情報の取得

    def get_room(self):
        url_get_room = self.url + "/rooms/" + str(self.room_id)
        result_room = session.get(url_get_room)
        print(result_room.status_code)
        print(result_room.json())

    # 対戦情報テーブル(現在のターン, hit&blowの履歴, 勝敗の判定)を取得する

    def get_table(self):
        url_get_table = self.url + "/rooms/" + \
            str(self.room_id) + "/players/" + self.player_name + "/table"
        result_table = session.get(url_get_table)
        print(result_table.status_code)
        print(result_table.json())
        return result_table.json()

    # 相手に当てさせる数字を登録する
    def post_hidden(self, ans: str):
        url_post_hidden = self.url + "/rooms/" + \
            str(self.room_id) + "/players/" + self.player_name + "/hidden"
        post_data_hidden = {
            "player_id": self.player_id,
            "hidden_number": ans
        }
        result_hidden = session.post(
            url_post_hidden, headers=self.headers, json=post_data_hidden)
        print(result_hidden.status_code)
        print(result_hidden.json())
        return result_hidden.json()

    # 推測した数字を登録する
    def post_guess(self, guess: str):
        url_post_guess = self.url + "/rooms/" + \
            str(self.room_id) + "/players/" + \
            self.player_name + "/table/guesses"
        post_data_guess = {
            "player_id": self.player_id,
            "guess": guess
        }
        result_guess = session.post(
            url_post_guess, headers=self.headers, json=post_data_guess)
        # print(result_guess.status_code)
        # print(result_guess.json())
        return result_guess.json()

    # def fugaku(self):


"""試し
drun = SendReceive(room_id=4001)
drun.enter_room()
    200
    {'id': 4001, 'state': 1, 'player1': 'D', 'player2': None}
d2run = SendReceive(room_id=4001, player_name="D2")
d2run.enter_room()
    200
    {'id': 4001, 'state': 2, 'player1': 'D', 'player2': 'D2'}
drun.get_room()
    200
    {'id': 4001, 'state': 2, 'player1': 'D', 'player2': 'D2'}
drun.get_table()
    200
    {'room_id': 4001, 'state': 2, 'now_player': None, 'table': None, 'opponent_table': None, 'winner': 
    None, 'game_end_count': None}
drun.post_hidden(ans="12345")
    200
    {'selecting': True}
d2run.post_hidden(ans="02abd")
    200
    {'selecting': False}
drun.get_table()
    200
    {'room_id': 4001, 'state': 2, 'now_player': 'D', 'table': [], 'opponent_table': [], 'winner': None, 'game_end_count': None}
drun.post_guess("12345")
    200
    {'room_id': 4001, 'now_player': 'D2', 'guesses': ['12345']}
drun.get_table()
    200
    {'room_id': 4001, 'state': 2, 'now_player': 'D2', 'table': [{'guess': '12345', 'hit': 1, 'blow': 0}], 'opponent_table': [], 'winner': None, 'game_end_count': None}
d2run.post_guess("123ab")
    200
    {'room_id': 4001, 'now_player': 'D', 'guesses': ['123ab']}
drun.get_table()
    200
    , 'opponent_table': [{'guess': '123ab', 'hit': 3, 'blow': 0}], 'winner': None, 'game_end_count': 1}
drun.post_guess("12345")
    200
    {'room_id': 4001, 'now_player': 'D2', 'guesses': ['12345', '12345']}
drun.get_table()
    200
    {'room_id': 4001, 'state': 2, 'now_player': 'D2', 'table': [{'guess': '12345', 'hit': 1, 'blow': 0}, {'guess': '12345', 'hit': 1, 'blow': 0}], 'opponent_table': [{'guess': '123ab', 'hit': 3, 'blow': 0}], 'winner': None, 'game_end_count': None}
d2run.post_guess("12345")
    200
    {'room_id': 4001, 'now_player': 'D', 'guesses': ['123ab', '12345']}
drun.get_table()
    200
    {'room_id': 4001, 'state': 3, 'now_player': 'D', 'table': [{'guess': '12345', 'hit': 1, 'blow': 0}, {'guess': '12345', 'hit': 1, 'blow': 0}], 'opponent_table': [{'guess': '123ab', 'hit': 3, 'blow': 
    0}, {'guess': '12345', 'hit': 5, 'blow': 0}], 'winner': 'D2', 'game_end_count': 2}
d2run.get_table()
    200
    {'room_id': 4001, 'state': 3, 'now_player': 'D', 'table': [{'guess': '123ab', 'hit': 3, 'blow': 0}, 
    {'guess': '12345', 'hit': 5, 'blow': 0}], 'opponent_table': [{'guess': '12345', 'hit': 1, 'blow': 0}, {'guess': '12345', 'hit': 1, 'blow': 0}], 'winner': 'D2', 'game_end_count': 2}
drun.post_guess("11111")
    400
    {'detail': 'format error 11111'}
drun.post_guess("02abd")
    200
    {'room_id': 4001, 'now_player': 'D2', 'guesses': ['12345', '12345', '02abd']}
drun.get_table()
    200
    {'room_id': 4001, 'state': 3, 'now_player': 'D2', 'table': [{'guess': '12345', 'hit': 1, 'blow': 0}, {'guess': '12345', 'hit': 1, 'blow': 0}, {'guess': '02abd', 'hit': 5, 'blow': 0}], 'opponent_table': [{'guess': '123ab', 'hit': 3, 'blow': 0}, {'guess': '12345', 'hit': 5, 'blow': 0}], 'winner': None, 'game_end_count': None}
drun.post_hidden("02abd")
    400
    {'detail': 'you can not select hidden'}
drun.get_table()
    200
    {'room_id': 4001, 'state': 3, 'now_player': 'D2', 'table': [{'guess': '12345', 'hit': 1, 'blow': 0}, {'guess': '12345', 'hit': 1, 'blow': 0}, {'guess': '02abd', 'hit': 5, 'blow': 0}], 'opponent_table': [{'guess': '123ab', 'hit': 3, 'blow': 0}, {'guess': '12345', 'hit': 5, 'blow': 0}], 'winner': None, 'game_end_count': None}
"""
