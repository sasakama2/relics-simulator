from src import DBManager
import pathlib

SCRIPT_DIR = pathlib.Path(__file__).parent.absolute()

# スクリプトディレクトリから見て、一つ上に戻り、dbフォルダに入り、ファイルを指定
DB_PATH = SCRIPT_DIR.parent / 'db' / 'static_data.db'

# DBManagerのインスタンス化
db_manager = DBManager(db_name=DB_PATH)

db_manager.init_tables()