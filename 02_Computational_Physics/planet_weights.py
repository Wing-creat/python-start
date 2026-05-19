# planet_weights.py

def calculate_offworld_weight(mass_kg: float) -> dict:
    """
    Calculates the weight of an object on various celestial bodies.
    Formula: W = m * g (Weight = mass * gravity)
    
    Args:
        mass_kg (float): The mass of the object in kilograms.
        
    Returns:
        dict: A dictionary containing the weight (in Newtons) on different planets.
    """
    if mass_kg < 0:
        raise ValueError("Error: Mass cannot be negative in classical physics.")
        
    # Standard surface gravity (m/s^2)
    surface_gravity = {
        "Earth": 9.81,
        "Moon": 1.62,
        "Mars": 3.71,
        "Jupiter": 24.79
    }
    
    weights = {}
    for planet, g in surface_gravity.items():
        # W = m * g
        weights[planet] = round(mass_kg * g, 2)
        
    return weights

if __name__ == "__main__":
    print("=== 🚀 Aerospace Engineering: Celestial Weight Calculator ===\n")
    
    # Let's test with a standard mass (e.g., a 75kg astronaut or rover)
    test_mass = 85.0 
    
    print(f"Target Mass: {test_mass} kg\n")
    
    try:
        results = calculate_offworld_weight(test_mass)
        for body, weight in results.items():
            print(f"  |- Weight on {body:<7}: {weight:>7} N")
    except ValueError as e:
        print(f"Simulation failed: {e}")
        
    print("\n=============================================================")
    print("Status: Gravitational calculations executed successfully.")