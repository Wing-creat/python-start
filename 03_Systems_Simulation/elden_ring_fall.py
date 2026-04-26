# elden_ring_fall.py

print("--- 💍 Elden Ring Fall Survival Calculator ---")
print("Welcome, Tarnished. Let's test your gravity resistance.")
print("-" * 40)

# Prompt the user (the Tarnished) to input the expected fall height
try:
    height = float(input("Enter the fall height (in meters): "))
except ValueError:
    print("Foolish Tarnished! Enter a valid number.")
    exit()

# Core game engine logic: Evaluate survival based on strict height thresholds
if height < 16:
    print(f"\nResult: You fell {height} meters.")
    print("Status: Rolled safely! 0 damage taken. Keep exploring.")
    
elif height >= 16 and height < 20:
    # Heavy damage zone: between 16m and 19.99m
    print(f"\nResult: You fell {height} meters.")
    print("Status: CRUNCH! You broke your legs and took heavy damage! Drink a Flask!")
    
else: 
    # Fatal fall threshold: 20 meters or greater
    print(f"\nResult: You fell {height} meters...")
    print("\n   Y O U   D I E D   ")
    print("Gravity remains the hardest boss in the Lands Between.")