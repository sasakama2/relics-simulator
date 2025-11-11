# db_manager.py が同じディレクトリにあることを想定
from DB_manager import DBManager 
import pathlib

SCRIPT_DIR = pathlib.Path(__file__).parent.absolute()

# スクリプトディレクトリから見て、一つ上に戻り、dbフォルダに入り、ファイルを指定
DB_PATH = SCRIPT_DIR.parent.parent / 'db' / 'static_data.db'

# DBManagerのインスタンス化
db_manager = DBManager(db_name=str(DB_PATH))

# 3. データを挿入
type = "通常"
effects = [
    2,
    9,
    4,
]
demerits = []
color = "赤"

db_manager.insert_relic(relic_type=type, effects=effects, demerits=demerits, color=color)

type = "深層"
effects = [
    8,
    4,
]
demerits = [6]
color = "青"
db_manager.insert_relic(relic_type=type, effects=effects, demerits=demerits, color=color)

# 6. 接続を閉じる
db_manager.close()