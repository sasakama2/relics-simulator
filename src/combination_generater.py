from . import DB_manager

def get_choices_by_effects(character_id, effect_ids, db_manager_instance: DB_manager):
    vessels = {}
    universal_vessels = []
    relics = []
    universal_id = 9

    # 利用可能な献器とそのスロット情報を取得
    universal_vessels = db_manager_instance.fetch_character_vessels(universal_id)
    vessels_list = db_manager_instance.fetch_character_vessels(character_id)
    for vessel in vessels_list:
        slots = db_manager_instance.fetch_vessel_slots(vessel['vessel_id'])
        vessels[vessel['vessel_id']] = slots
    for vessel in universal_vessels:
        slots = db_manager_instance.fetch_vessel_slots(vessel['vessel_id'])
        vessels[vessel['vessel_id']] = slots
    
    # 指定された効果IDに基づいて遺物を取得
    for effect_id in effect_ids:
        matched_relics = db_manager_instance.fetch_relics_by_effect(effect_id)
        relics.extend(matched_relics)
    
    return vessels, relics

def calculate_total_combinations(vessels, relics):
    relic_id_set = []
    relic_id_sets = []
    total_combinations = 0
    for vessel_id, slots in vessels.items():
        normal_slots = slots[0]
        deep_slots = slots[1]
        num_normal_slots = len(normal_slots)
        num_deep_slots = len(deep_slots)

        # 各スロットに対して、利用可能な遺物の数を計算
        normal_slot_combinations = 1
        for slot in normal_slots:
            count = sum(1 for relic in relics if relic['relic_type'] == "通常" and relic['color'] == slot['color'])
            normal_slot_combinations *= count if count > 0 else 1

        deep_slot_combinations = 1
        for slot in deep_slots:
            count = sum(1 for relic in relics if relic['relic_type'] == "深層" and relic['color'] == slot['color'])
            deep_slot_combinations *= count if count > 0 else 1

        total_combinations += normal_slot_combinations * deep_slot_combinations

    return total_combinations