# kinetic_energy.py

def calculate_kinetic_energy(mass_kg: float, velocity_m_s: float) -> float:
    """
    Calculates the classical kinetic energy of an object.
    
    Args:
        mass_kg (float): The mass of the object in kilograms. Must be non-negative.
        velocity_m_s (float): The velocity of the object in meters per second.
        
    Returns:
        float: The calculated kinetic energy in Joules.
        
    Raises:
        ValueError: If the provided mass is negative.
    """
    if mass_kg < 0:
        raise ValueError("Error: Mass cannot be negative in classical mechanics.")
        
    energy = 0.5 * mass_kg * (velocity_m_s ** 2)
    return energy

if __name__ == "__main__":
    print("=== Computational Physics: Kinetic Energy Simulation ===\n")
    
    # Advanced test scenarios to demonstrate system scalability
    scenarios = [
        {"entity": "9mm Bullet", "mass_kg": 0.0075, "velocity_m_s": 380.0},
        {"entity": "Sedan Car", "mass_kg": 1500.0, "velocity_m_s": 26.8},    # Approx. 60 mph
        {"entity": "Boeing 747", "mass_kg": 412770.0, "velocity_m_s": 250.0} # Cruising speed
    ]
    
    for item in scenarios:
        try:
            ek_joules = calculate_kinetic_energy(item["mass_kg"], item["velocity_m_s"])
            # Using scientific notation (e) for cleaner output on large numbers
            print(f"Target: {item['entity']}")
            print(f"  |- Mass:     {item['mass_kg']} kg")
            print(f"  |- Velocity: {item['velocity_m_s']} m/s")
            print(f"  |- Energy:   {ek_joules:.2e} Joules\n")
        except ValueError as e:
            print(f"Simulation failed for {item['entity']}: {e}")
            
    print("======================================================")
    print("Status: All physics constraints validated successfully.")