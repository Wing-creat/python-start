# weapon_database.py

def manage_weapons():
    print("--- 🏺 Grand Library Weapon Database ---")

    # A dictionary where keys are weapon names and values are stats dictionaries
    # This is a common way to store configuration data in engineering
    weapons = {
        "Moonveil": {
            "type": "Katana",
            "physical_atk": 73,
            "magic_atk": 87,
            "weight": 5.5
        },
        "Rivers of Blood": {
            "type": "Katana",
            "physical_atk": 76,
            "fire_atk": 76,
            "weight": 6.5
        },
        "Dark Moon Greatsword": {
            "type": "Greatsword",
            "physical_atk": 82,
            "magic_atk": 98,
            "weight": 10.0
        }
    }

    print("Current Weapons in Database:", list(weapons.keys()))
    print("-" * 35)

    # User input to search for a weapon
    query = input("Enter weapon name to see stats: ")

    # Checking if the key exists in our 'chest'
    if query in weapons:
        stats = weapons[query]
        print(f"\n[Stats for {query}]")
        # Iterating through the inner dictionary
        for key, value in stats.items():
            print(f"- {key.replace('_', ' ').title()}: {value}")
    else:
        print(f"\nError: Weapon '{query}' not found in the Grand Library.")

if __name__ == "__main__":
    manage_weapons()