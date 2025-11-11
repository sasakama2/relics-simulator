from src import DBManager
import pathlib

SCRIPT_DIR = pathlib.Path(__file__).parent.absolute()

# スクリプトディレクトリから見て、一つ上に戻り、dbフォルダに入り、ファイルを指定
DB_PATH = SCRIPT_DIR.parent / 'db' / 'static_data.db'

# DBManagerのインスタンス化
db_manager = DBManager(db_name=DB_PATH)

character_id = 1
vessels = db_manager.fetch_character_vessels(character_id)
for vessel in vessels:
    print(f"Vessel ID: {vessel['vessel_id']}, Vessel Name: {vessel['vessel_name']}")
    slots = db_manager.fetch_vessel_slots(vessel['vessel_id'])
    print("通常スロット:")
    for slot in slots[0]:
        print(f"  Slot ID: {slot['slot_index']}, Color: {slot['color']}")
    print("深層スロット:")
    for slot in slots[1]:
        print(f"  Slot ID: {slot['slot_index']}, Color: {slot['color']}")

db_manager.close()