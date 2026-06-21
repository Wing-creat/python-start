# boss_combat_log.py

def track_combat():
    print("--- 🗡️ Elden Ring Combat Damage Log ---")
    boss_name = "Malenia, Blade of Miquella"

    # Damage values for each hit in a short combo.
    damage_hits = [450, 520, 380, 610, 490]

    total_damage = 0

    print(f"Target: {boss_name}")
    print("-" * 35)

    for hit_count, damage in enumerate(damage_hits, start=1):
        total_damage += damage
        print(f"Hit {hit_count}: Dealt {damage} damage.")

    print("-" * 35)
    print(f"Total Hits   : {len(damage_hits)}")
    print(f"Total Damage : {total_damage}")

    if total_damage > 2000:
        print("Status: Stance Broken! Critical hit opportunity!")
    else:
        print("Status: Boss is still standing. Keep fighting, Tarnished!")


if __name__ == "__main__":
    track_combat()
