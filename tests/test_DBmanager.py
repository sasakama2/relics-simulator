from my_project.DB_manager import DBManager 
import pathlib

SCRIPT_DIR = pathlib.Path(__file__).parent.absolute()

# スクリプトディレクトリから見て、一つ上に戻り、dbフォルダに入り、ファイルを指定
DB_PATH = SCRIPT_DIR.parent / 'db' / 'static_data.db'

# DBManagerのインスタンス化
db_manager = DBManager(db_name=str(DB_PATH))


def test_insert_relic():
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

def test_fetch_vessels():
    for character_id in range(1,10):
        vessels = db_manager.fetch_character_vessels(character_id)
        assert isinstance(vessels, list), "Fetched vessels should be a list."
        for vessel in vessels:
            assert 'vessel_id' in vessel and 'vessel_name' in vessel, "Vessel should have 'vessel_id' and 'vessel_name'."

def test_init_tables():
    db_manager._connect()
    db_manager.init_tables()

def test_fetch_relics_by_effect():
    id = 4
    relics = db_manager.fetch_relics_by_effect(effect_id=id)
    assert isinstance(relics, list), "Fetched relics should be a list."
    for relic in relics:
        assert 'relic_id' in relic and 'relic_type' in relic, "Relic should have 'relic_id' and 'relic_type'."

def test_search_effect_by_term():
    term = "上昇"
    effects = db_manager.search_effect_by_term(term)
    assert isinstance(effects, list), "Searched effects should be a list."


# 6. 接続を閉じる
db_manager.close()