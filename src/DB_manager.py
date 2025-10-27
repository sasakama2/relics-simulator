import sqlite3
from typing import List, Tuple, Optional

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

    def create_relic_table(self):
        """
        装備データを格納するためのテーブルを作成する。
        """
        if not self.cursor:
            print("データベースに接続されていません。")
            return

        # 装備名(TEXT UNIQUE), 攻撃力(INTEGER), 防御力(INTEGER) を持つテーブル
        query = """
        CREATE TABLE IF NOT EXISTS relic (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            attack INTEGER,
            defense INTEGER
        )
        """
        try:
            self.cursor.execute(query)
            self.conn.commit()
            print("テーブル 'equipment' の作成または確認が完了しました。")
        except sqlite3.Error as e:
            print(f"テーブル作成エラー: {e}")
    
    
    def insert_equipment(self, name: str, attack: int, defense: int):
        """
        新しい装備データをテーブルに挿入する。
        """
        if not self.cursor: return
        query = "INSERT INTO equipment (name, attack, defense) VALUES (?, ?, ?)"
        try:
            self.cursor.execute(query, (name, attack, defense))
            self.conn.commit()
            print(f"装備 '{name}' を挿入しました。")
        except sqlite3.IntegrityError:
            # UNIQUE制約違反 (装備名が既に存在する)
            print(f"警告: 装備 '{name}' は既に存在します。")
        except sqlite3.Error as e:
            print(f"データ挿入エラー: {e}")

    def get_all_equipment(self) -> List[sqlite3.Row]:
        """
        全ての装備データを取得する。
        """
        if not self.cursor: return []
        query = "SELECT * FROM equipment"
        try:
            self.cursor.execute(query)
            # fetchall() で結果を全てリストとして取得
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"データ取得エラー: {e}")
            return []

    def get_equipment_by_name(self, name: str) -> Optional[sqlite3.Row]:
        """
        指定した名前の装備データを一つ取得する。
        """
        if not self.cursor: return None
        query = "SELECT * FROM equipment WHERE name = ?"
        try:
            self.cursor.execute(query, (name,))
            # fetchone() で結果を一つだけ取得
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"データ取得エラー: {e}")
            return None