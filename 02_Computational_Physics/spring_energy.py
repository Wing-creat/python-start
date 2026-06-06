# spring_energy.py

def calculate_spring_energy(spring_constant_n_m: float, displacement_m: float) -> float:
    """
    Calculates the elastic potential energy stored in a spring based on Hooke's Law.

    Formula: E_p = 1/2 * k * x^2
    """
    if spring_constant_n_m <= 0:
        raise ValueError("Error: Spring constant (k) must be strictly positive.")
        
    # The displacement can be negative (compression) or positive (extension)
    # The energy stored will always be positive because of the square (x^2)
    energy_joules = 0.5 * spring_constant_n_m * (displacement_m ** 2)
    return energy_joules

if __name__ == "__main__":
    print("=== Spring Energy Calculator ===\n")
    
    # A few simple examples with different spring stiffness values.
    spring_tests = [
        {"type": "Clicky Pen Spring", "k": 100.0, "x": 0.01},           # 1 cm compression
        {"type": "Mountain Bike Shock", "k": 40000.0, "x": 0.05},       # 5 cm compression
        {"type": "Vehicle Suspension Spring", "k": 120000.0, "x": 0.15}, # 15 cm compression
    ]
    
    for test in spring_tests:
        try:
            energy = calculate_spring_energy(test["k"], test["x"])
            print(f"Mechanical System: {test['type']}")
            print(f"  |- Spring Constant (k): {test['k']} N/m")
            print(f"  |- Displacement (x):    {test['x']} m")
            print(f"  => Stored Energy:       {energy:,.2f} Joules\n")
        except ValueError as e:
            print(f"Simulation failed for {test['type']}: {e}\n")
            
    print("==============================================================")
    print("Status: Spring energy calculations complete.")
