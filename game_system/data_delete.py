
# from system import mypjg
from systems import initialize

def run() -> None:
    """数当てゲームのメイン
    """
    delete = initialize.Initialize()
    delete.confirm()
    

run()