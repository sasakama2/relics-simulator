from DB_manager import DBManager
import pathlib
import sqlite3


SCRIPT_DIR = pathlib.Path(__file__).parent.absolute()

DB_PATH = SCRIPT_DIR.parent / 'db' / 'static_data.db'

# DBManagerのインスタンス化
db_manager = DBManager(db_name=DB_PATH)

if not db_manager.cursor:
    print("データベースに接続されていません。")
    exit(1)
# 1. effectテーブルの作成
query = """
CREATE TABLE IF NOT EXISTS effect (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    effect TEXT NOT NULL UNIQUE
)
"""
try:
    db_manager.cursor.execute(query)
    db_manager.conn.commit()
    print("テーブル 'effect' の作成または確認が完了しました。")
except sqlite3.Error as e:
    print(f"テーブル作成エラー: {e}")
# 2. demeritテーブルの作成
query = """
CREATE TABLE IF NOT EXISTS demerit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    demerit TEXT NOT NULL UNIQUE
)
"""
db_manager.cursor.execute(query)
db_manager.conn.commit()
# 3. charactorテーブルの作成
query = """
CREATE TABLE IF NOT EXISTS charactor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    charactor TEXT NOT NULL UNIQUE
)
"""

charactors = [
    "追跡者",
    "守護者",
    "レディ",
    "隠者",
    "鉄の目",
    "無頼漢",
    "執行者",
    "復讐者"
]
db_manager.cursor.execute(query)
db_manager.conn.commit()
for char in charactors:
    try:
        db_manager.cursor.execute(
            "INSERT INTO charactor (charactor) VALUES (?)", (char,))
        db_manager.conn.commit()
    except sqlite3.IntegrityError:
        print(f"キャラクター '{char}' は既に存在します。スキップします。")
        
db_manager.close()