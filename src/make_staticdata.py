from DB_manager import DBManager
import pathlib
import sqlite3
import csv


SCRIPT_DIR = pathlib.Path(__file__).parent.absolute()

DB_PATH = SCRIPT_DIR.parent / 'db' / 'static_data.db'

# DBManagerのインスタンス化
db_manager = DBManager(db_name=DB_PATH)


if not db_manager.cursor:
    print("データベースに接続されていません。")
    exit(1)

query = """
DROP TABLE IF EXISTS effects;
DROP TABLE IF EXISTS demerits;
DROP TABLE IF EXISTS characters;
DROP TABLE IF EXISTS vessel;
DROP TABLE IF EXISTS normal_slots;
DROP TABLE IF EXISTS deep_slots;
DROP TABLE IF EXISTS relics;
DROP TABLE IF EXISTS relic_effects_link;
DROP TABLE IF EXISTS relic_demerits_link;
"""
try:
    db_manager.cursor.executescript(query)
    db_manager.conn.commit()
    print("既存のテーブルを削除しました。")
except sqlite3.Error as e:
    print(f"テーブル削除エラー: {e}")

db_manager.cursor.execute("PRAGMA foreign_keys = ON;")

query = """
-- 1. effectテーブルの作成
CREATE TABLE IF NOT EXISTS effects (
    effect_id INTEGER PRIMARY KEY AUTOINCREMENT,
    effect_text TEXT NOT NULL UNIQUE
);
-- 2. demeritテーブルの作成
CREATE TABLE IF NOT EXISTS demerits (
    demerit_id INTEGER PRIMARY KEY AUTOINCREMENT,
    demerit_text TEXT NOT NULL UNIQUE
);
-- 3. charactersテーブルの作成
CREATE TABLE IF NOT EXISTS characters (
    character_id INTEGER PRIMARY KEY AUTOINCREMENT,
    character_name TEXT NOT NULL UNIQUE
);
-- 4. vesselテーブルの作成
CREATE TABLE IF NOT EXISTS vessel (
    vessel_id INTEGER PRIMARY KEY AUTOINCREMENT,
    vessel_name TEXT NOT NULL UNIQUE,
    character_id INTEGER NOT NULL,
    FOREIGN KEY (character_id) REFERENCES characters (character_id)
);
-- 5. normal_slotsテーブルの作成
CREATE TABLE IF NOT EXISTS normal_slots (
    slot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    vessel_id INTEGER NOT NULL,
    slot_index INTEGER NOT NULL,
    color TEXT NOT NULL,
    FOREIGN KEY (vessel_id) REFERENCES vessel (vessel_id)
);
-- 6. deep_slotsテーブルの作成
CREATE TABLE IF NOT EXISTS deep_slots (
    slot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    vessel_id INTEGER NOT NULL,
    slot_index INTEGER NOT NULL,
    color TEXT NOT NULL,
    FOREIGN KEY (vessel_id) REFERENCES vessel (vessel_id)
);
-- 7.relicsテーブルの作成
CREATE TABLE IF NOT EXISTS relics (
    relic_id INTEGER PRIMARY KEY AUTOINCREMENT,
    relic_type TEXT NOT NULL,
    color TEXT NOT NULL
);
-- 8.relic_effects_linkテーブルの作成
CREATE TABLE IF NOT EXISTS relic_effects_link (
    link_id INTEGER PRIMARY KEY AUTOINCREMENT,
    relic_id INTEGER NOT NULL,
    effect_id INTEGER NOT NULL,
    index_in_relic INTEGER NOT NULL,
    FOREIGN KEY (relic_id) REFERENCES relics (relic_id),
    FOREIGN KEY (effect_id) REFERENCES effects (effect_id)
);
-- 9.relic_demerits_linkテーブルの作成
CREATE TABLE IF NOT EXISTS relic_demerits_link (
    link_id INTEGER PRIMARY KEY AUTOINCREMENT,
    relic_id INTEGER NOT NULL,
    demerit_id INTEGER NOT NULL,
    index_in_relic INTEGER NOT NULL,
    FOREIGN KEY (relic_id) REFERENCES relics (relic_id),
    FOREIGN KEY (demerit_id) REFERENCES demerits (demerit_id)
);
"""
try:
    db_manager.cursor.executescript(query)
    db_manager.conn.commit()
    print("テーブル 'effect' の作成または確認が完了しました。")
except sqlite3.Error as e:
    print(f"テーブル作成エラー: {e}")


characters = [
    "追跡者",
    "守護者",
    "レディ",
    "隠者",
    "鉄の目",
    "無頼漢",
    "執行者",
    "復讐者",
    "Universal",
]

for char in characters:
    try:
        db_manager.cursor.execute(
            "INSERT INTO characters (character_name) VALUES (?)", (char,))
        db_manager.conn.commit()
    except sqlite3.IntegrityError:
        print(f"キャラクター '{char}' は既に存在します。スキップします。")
        

file_path = SCRIPT_DIR.parent / 'tmp' / 'effect_list.txt'
with open(file_path, 'r', encoding='utf-8') as file:
    file_content = file.read()
effects = file_content.split(" ")


for effect in effects:
    try:
        db_manager.cursor.execute(
            "INSERT INTO effects (effect_text) VALUES (?)", (effect,))
        db_manager.conn.commit()
    except sqlite3.IntegrityError:
        print(f"エフェクト '{effect}' は既に存在します。スキップします。")

file_path = SCRIPT_DIR.parent / 'tmp' / 'deep_effect_list.txt'
with open(file_path, 'r', encoding='utf-8') as file:
    file_content = file.read()
effects = file_content.split(" ")


for effect in effects:
    try:
        db_manager.cursor.execute(
            "INSERT INTO effects (effect_text) VALUES (?)", (effect,))
        db_manager.conn.commit()
    except sqlite3.IntegrityError:
        print(f"エフェクト '{effect}' は既に存在します。スキップします。")

file_path = SCRIPT_DIR.parent / 'tmp' / 'demerit_list.txt'
with open(file_path, 'r', encoding='utf-8') as file:
    file_content = file.read()  
demerits = file_content.split(" ")
for demerit in demerits:
    try:
        db_manager.cursor.execute(
            "INSERT INTO demerits (demerit_text) VALUES (?)", (demerit,))
        db_manager.conn.commit()
    except sqlite3.IntegrityError:
        print(f"デメリット '{demerit}' は既に存在します。スキップします。")

path = SCRIPT_DIR.parent / 'tmp' / 'Vessel.csv'
with open(path, 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)  # ヘッダー行をスキップ

    character_map = {}
    db_manager.cursor.execute("SELECT character_id, character_name FROM characters;")
    for char_id, char_name in db_manager.cursor.fetchall():
        character_map[char_name] = char_id

    for row in reader:
        char_name = row[0].strip()
        vessel_name = row[1].strip()
        normal_slots_colors = [row[2].strip(), row[3].strip(), row[4].strip()]
        deep_slots_colors = [row[5].strip(), row[6].strip(), row[7].strip()]
        acquisition = row[8].strip()

        db_manager.cursor.execute(
            "INSERT INTO vessel (vessel_name, character_id) VALUES (?, ?);",
            (vessel_name, character_map[char_name])
        )

        vessel_id = db_manager.cursor.lastrowid
        for index, color in enumerate(normal_slots_colors):
            db_manager.cursor.execute(
                "INSERT INTO normal_slots (vessel_id, slot_index, color) VALUES (?, ?, ?);",
                (vessel_id, index + 1, color)
            )
        for index, color in enumerate(deep_slots_colors):
            db_manager.cursor.execute(
                "INSERT INTO deep_slots (vessel_id, slot_index, color) VALUES (?, ?, ?);",
                (vessel_id, index + 1, color)
            )
        db_manager.conn.commit()
        print(f"Vessel '{vessel_name}' のデータが正常に挿入されました。")

db_manager.close()