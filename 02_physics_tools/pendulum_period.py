# pendulum_period.py
import math  # Import Python's advanced math module for square roots and Pi

print("--- ⏱️ Simple Pendulum Period Calculator ---")

try:
    # Prompt the user for the pendulum's string length
    length = float(input("Enter pendulum length (in meters): "))
except ValueError:
    print("Error: Please enter a valid number.")
    exit()

# Earth's average gravitational acceleration in m/s^2
gravity = 9.81 

# Core physics formula: T = 2 * pi * sqrt(L/g)
period = 2 * math.pi * math.sqrt(length / gravity)

print("-" * 35)
print(f"Pendulum Length : {length} meters")
print(f"Earth's Gravity : {gravity} m/s^2")
# Format the output to 2 decimal places for a precise dashboard look
print(f"Oscillation Period : {period:.2f} seconds")
print("-" * 35)