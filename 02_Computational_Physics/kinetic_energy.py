# kinetic_energy.py

print("--- ⚡ Kinetic Energy Calculator ---")

# Define a reusable function to calculate kinetic energy
# This acts like a custom machine: input mass and velocity, output energy
def calculate_ke(mass, velocity):
    # Core physics formula: KE = 0.5 * m * v^2
    energy = 0.5 * mass * (velocity ** 2)
    return energy  # The 'return' keyword sends the result back

try:
    # Prompt the user for input parameters
    m = float(input("Enter the mass of the object (in kg): "))
    v = float(input("Enter the velocity of the object (in m/s): "))
except ValueError:
    print("Error: Invalid input. Please enter numerical values.")
    exit()

# Call the function and store the returned value
result = calculate_ke(m, v)

print("-" * 35)
print(f"Mass           : {m} kg")
print(f"Velocity       : {v} m/s")
print(f"Kinetic Energy : {result:.2f} Joules")
print("-" * 35)