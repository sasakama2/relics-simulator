import sqlite3
from typing import List, Tuple, Optional
import pathlib, csv

class DBManager:
    """
    SQLiteデータベースの接続と基本的な操作を管理するクラス。
    """
    def __init__(self, db_name: str = 'equipment.db'):
        """
        データベースファイル名を設定し、接続を確立する。
        """
        self.db_name = db_name
        self.conn: Optional[sqlite3.Connection] = None
        self.cursor: Optional[sqlite3.Cursor] = None
        self._connect()

    def _connect(self):
        """
        データベースに接続し、カーソルを作成する。
        """
        try:
            # データベースファイルが存在しない場合は新規作成される
            self.conn = sqlite3.connect(self.db_name)
            # 取得したデータをカラム名でアクセスできるようにする (辞書形式)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"データベース接続エラー: {e}")
            self.conn = None
            self.cursor = None

    def close(self):
        """
        データベース接続を閉じる。
        """
        if self.conn:
            self.conn.close()
            print("データベース接続を閉じました。")

    def create_tables(self):
        """
        必要な初期のテーブルを作成する。
        """
        if not self.cursor:
            print("データベースに接続されていません。")
            return

        self.cursor.execute("PRAGMA foreign_keys = ON;")

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
            self.cursor.executescript(query)
            self.conn.commit()
            print("テーブル 'equipment' の作成または確認が完了しました。")
        except sqlite3.Error as e:
            print(f"テーブル作成エラー: {e}")

    def init_tables(self):
        """
        既存のテーブルを削除し、新たにテーブルを作成する（デバッグ用）。
        """
        self.delete_tables()
        self.create_tables()
        SCRIPT_DIR = pathlib.Path(__file__).parent.absolute()

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
                self.cursor.execute(
                    "INSERT INTO characters (character_name) VALUES (?)", (char,))
                self.conn.commit()
            except sqlite3.IntegrityError:
                print(f"キャラクター '{char}' は既に存在します。スキップします。")
                

        file_path = SCRIPT_DIR.parent / 'tmp' / 'effect_list.txt'
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
        effects = file_content.split(" ")


        for effect in effects:
            try:
                self.cursor.execute(
                    "INSERT INTO effects (effect_text) VALUES (?)", (effect,))
                self.conn.commit()
            except sqlite3.IntegrityError:
                print(f"エフェクト '{effect}' は既に存在します。スキップします。")

        file_path = SCRIPT_DIR.parent / 'tmp' / 'deep_effect_list.txt'
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
        effects = file_content.split(" ")


        for effect in effects:
            try:
                self.cursor.execute(
                    "INSERT INTO effects (effect_text) VALUES (?)", (effect,))
                self.conn.commit()
            except sqlite3.IntegrityError:
                print(f"エフェクト '{effect}' は既に存在します。スキップします。")

        file_path = SCRIPT_DIR.parent / 'tmp' / 'demerit_list.txt'
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()  
        demerits = file_content.split(" ")
        for demerit in demerits:
            try:
                self.cursor.execute(
                    "INSERT INTO demerits (demerit_text) VALUES (?)", (demerit,))
                self.conn.commit()
            except sqlite3.IntegrityError:
                print(f"デメリット '{demerit}' は既に存在します。スキップします。")

        path = SCRIPT_DIR.parent / 'tmp' / 'Vessel.csv'
        with open(path, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)  # ヘッダー行をスキップ

            character_map = {}
            self.cursor.execute("SELECT character_id, character_name FROM characters;")
            for char_id, char_name in self.cursor.fetchall():
                character_map[char_name] = char_id

            for row in reader:
                char_name = row[0].strip()
                vessel_name = row[1].strip()
                normal_slots_colors = [row[2].strip(), row[3].strip(), row[4].strip()]
                deep_slots_colors = [row[5].strip(), row[6].strip(), row[7].strip()]
                acquisition = row[8].strip()

                self.cursor.execute(
                    "INSERT INTO vessel (vessel_name, character_id) VALUES (?, ?);",
                    (vessel_name, character_map[char_name])
                )

                vessel_id = self.cursor.lastrowid
                for index, color in enumerate(normal_slots_colors):
                    self.cursor.execute(
                        "INSERT INTO normal_slots (vessel_id, slot_index, color) VALUES (?, ?, ?);",
                        (vessel_id, index + 1, color)
                    )
                for index, color in enumerate(deep_slots_colors):
                    self.cursor.execute(
                        "INSERT INTO deep_slots (vessel_id, slot_index, color) VALUES (?, ?, ?);",
                        (vessel_id, index + 1, color)
                    )
                self.conn.commit()
                print(f"Vessel '{vessel_name}' のデータが正常に挿入されました。")
    
    def delete_tables(self):
        """
        既存のテーブルを削除する（デバッグ用）。
        """
        if not self.cursor:
            print("データベースに接続されていません。")
            return

        query = """
        DROP TABLE IF EXISTS relic_demerits_link;
        DROP TABLE IF EXISTS relic_effects_link;
        DROP TABLE IF EXISTS relics;
        DROP TABLE IF EXISTS deep_slots;
        DROP TABLE IF EXISTS normal_slots;
        DROP TABLE IF EXISTS vessel;
        DROP TABLE IF EXISTS characters;
        DROP TABLE IF EXISTS demerits;
        DROP TABLE IF EXISTS effects;
        """
        try:
            self.cursor.executescript(query)
            self.conn.commit()
            print("全てのテーブルを削除しました。")
        except sqlite3.Error as e:
            print(f"テーブル削除エラー: {e}")
    
    def __insert_relic(self, relic_type: str, color: str) -> int:
        """
        relicsテーブルに新しいレリックを挿入する。

        :param relic_type: レリックのタイプ
        :param color: レリックの色
        :return: 挿入されたレリックのID
        """
        if not self.cursor:
            print("データベースに接続されていません。")
            return -1

        try:
            self.cursor.execute(
                "INSERT INTO relics (relic_type, color) VALUES (?, ?);",
                (relic_type, color)
            )
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"レリック挿入エラー: {e}")
            return -1
    
    def __link_effect_to_relic(self, relic_id: int, effect_id: int, index_in_relic: int) -> bool:
        """
        relic_effects_linkテーブルにレリックと効果のリンクを挿入する。

        :param relic_id: レリックのID
        :param effect_id: 効果のID
        :param index_in_relic: レリック内での効果のインデックス
        :return: 挿入成功ならTrue、失敗ならFalse
        """
        if not self.cursor:
            print("データベースに接続されていません。")
            return False
        
        query = """
        INSERT INTO relic_effects_link (relic_id, effect_id, index_in_relic) VALUES (?, ?, ?);
        """

        try:
            self.cursor.execute(
                query,
                (relic_id, effect_id, index_in_relic)
            )
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"レリック効果リンク挿入エラー: {e}")
            return False

    def __link_demerit_to_relic(self, relic_id: int, demerit_id: int, index_in_relic: int) -> bool:
        """
        relic_demerits_linkテーブルにレリックとデメリットのリンクを挿入する。

        :param relic_id: レリックのID
        :param demerit_id: デメリットのID
        :param index_in_relic: レリック内でのデメリットのインデックス
        :return: 挿入成功ならTrue、失敗ならFalse
        """
        if not self.cursor:
            print("データベースに接続されていません。")
            return False

        query = """
        INSERT INTO relic_demerits_link (relic_id, demerit_id, index_in_relic) VALUES (?, ?, ?);
        """

        try:
            self.cursor.execute(
                query,
                (relic_id, demerit_id, index_in_relic)
            )
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"レリックデメリットリンク挿入エラー: {e}")
            return False

    def insert_relic(self, relic_type: str, color: str, effects , demerits ):
        """
        relicsテーブルに新しいレリックを挿入する。

        :param relic_type: レリックのタイプ
        :param color: レリックの色
        :return: 挿入されたレリックのID
        """
        if not self.cursor:
            print("データベースに接続されていません。")
            return -1
        
        relic_id = self.__insert_relic(relic_type, color)
        if relic_id == -1:
            return -1
        for index, effect_id in enumerate(effects):
            self.__link_effect_to_relic(relic_id, effect_id, index)
        for index, demerit_id in enumerate(demerits):
            self.__link_demerit_to_relic(relic_id, demerit_id, index)
        return 