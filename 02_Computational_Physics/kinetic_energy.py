# kinetic_energy.py

def calculate_kinetic_energy(mass_kg: float, velocity_m_s: float) -> float:
    """
    Calculates the classical kinetic energy of a moving object.
    Formula: K = 1/2 * m * v^2
    """
    if mass_kg < 0:
        raise ValueError("Error: Mass cannot be negative.")
        
    # Constant: Speed of light in a vacuum (m/s)
    SPEED_OF_LIGHT = 299792458.0  
    
    if velocity_m_s > SPEED_OF_LIGHT:
        raise ValueError("Error: Velocity cannot exceed the speed of light in a vacuum.")
    elif velocity_m_s > 0.1 * SPEED_OF_LIGHT:
        # Trigger relativistic warning if velocity exceeds 10% of c
        print("  [!] System Warning: Velocity exceeds 10% of c. Classical mechanics may be inaccurate (Relativistic effects required).")
        
    energy_joules = 0.5 * mass_kg * (velocity_m_s ** 2)
    return energy_joules

if __name__ == "__main__":
    print("=== ⚡ Physics Engine: Kinetic Energy Calculator ===\n")
    
    # Test three distinct physics scenarios
    scenarios = [
        {"name": "Heavy Bowling Ball", "mass": 5.0, "vel": 8.0},
        {"name": "Highway SUV", "mass": 2000.0, "vel": 35.0},
        {"name": "Hypersonic Railgun Projectile", "mass": 10.0, "vel": 2500.0}
    ]
    
    for s in scenarios:
        try:
            ke = calculate_kinetic_energy(s["mass"], s["vel"])
            print(f"Object: {s['name']}")
            print(f"  |- Mass:  {s['mass']} kg")
            print(f"  |- Speed: {s['vel']} m/s")
            # Elegant formatting with comma separators for large numbers
            print(f"  => Kinetic Energy: {ke:,.2f} Joules\n")
        except ValueError as e:
            print(f"Simulation failed for {s['name']}: {e}\n")
            
    print("==================================================")
    print("Status: Energy calculations executed successfully.")