# boss_combat_log.py

def track_combat():
    print("--- 🗡️ Elden Ring Combat Damage Log ---")
    boss_name = "Malenia, Blade of Miquella"
    
    # A list of damage values for each hit in a combo
    # In real engineering, this could be a list of sensor readings
    damage_hits = [450, 520, 380, 610, 490]
    
    total_damage = 0
    hit_count = 0

    print(f"Target: {boss_name}")
    print("-" * 35)

    # Use a for-loop to iterate through each damage value in the list
    for damage in damage_hits:
        hit_count += 1
        total_damage += damage
        print(f"Hit {hit_count}: Dealt {damage} damage.")

    # Final summary of the combat engagement
    print("-" * 35)
    print(f"Total Hits   : {hit_count}")
    print(f"Total Damage : {total_damage}")
    
    if total_damage > 2000:
        print("Status: Stance Broken! Critical hit opportunity!")
    else:
        print("Status: Boss is still standing. Keep fighting, Tarnished!")

if __name__ == "__main__":
    track_combat()