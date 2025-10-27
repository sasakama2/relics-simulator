# db_manager.py が同じディレクトリにあることを想定
from DB_manager import DBManager
import pathlib

SCRIPT_DIR = pathlib.Path(__file__).parent.absolute()

# スクリプトディレクトリから見て、一つ上に戻り、dbフォルダに入り、ファイルを指定
DB_PATH = SCRIPT_DIR.parent / 'db' / 'simulator_data.db'

# DBManagerのインスタンス化
db_manager = DBManager(db_name=DB_PATH)

# 2. テーブルを作成
db_manager.create_equipment_table()

# 3. データを挿入
db_manager.insert_equipment("伝説の剣", 150, 5)
db_manager.insert_equipment("木の盾", 5, 20)
db_manager.insert_equipment("伝説の剣", 150, 5) # 既に存在するため警告が出る

# 4. 特定の装備を検索
sword = db_manager.get_equipment_by_name("伝説の剣")
if sword:
    # row_factory = sqlite3.Row のおかげでカラム名でアクセス可能
    print(f"\n--- 検索結果 ---")
    print(f"名前: {sword['name']}, 攻撃力: {sword['attack']}, 防御力: {sword['defense']}")

# 5. 全ての装備を取得
all_equipment = db_manager.get_all_equipment()
print(f"\n--- 全装備リスト ---")
for eq in all_equipment:
    print(f"ID: {eq['id']}, 名前: {eq['name']}, 攻撃力: {eq['attack']}")

# 6. 接続を閉じる
db_manager.close()