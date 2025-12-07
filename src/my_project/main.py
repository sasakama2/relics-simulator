# db_manager.py が同じディレクトリにあることを想定
from DB_manager import DBManager 
import pathlib
import time 

SCRIPT_DIR = pathlib.Path(__file__).parent.absolute()

# スクリプトディレクトリから見て、一つ上に戻り、dbフォルダに入り、ファイルを指定
DB_PATH = SCRIPT_DIR.parent.parent / 'db' / 'static_data.db'

# DBManagerのインスタンス化
db_manager = DBManager(db_name=str(DB_PATH))
current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print(f"[{current_time}]")
type = "通常"
effects = [
    0,
    9,
    4,
]
demerits = []
color = "赤"
try:
    db_manager.insert_relic(relic_type=type, effects=effects, demerits=demerits, color=color)
    print(f"[{current_time}] Inserted relic of type {type} with effects {effects} and color {color}.")
except Exception as e:
    print(f"[{current_time}] Error inserting relic: {e}")


# 6. 接続を閉じる
db_manager.close()