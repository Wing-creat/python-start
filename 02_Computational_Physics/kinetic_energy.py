# kinetic_energy.py

# Speed of light in a vacuum (m/s). Used only for a basic sanity check.
SPEED_OF_LIGHT = 299792458.0

def calculate_kinetic_energy(mass_kg: float, velocity_m_s: float) -> float:
    """
    Calculates the classical kinetic energy of a moving object.

    Formula: K = 1/2 * m * v^2
    """
    if mass_kg < 0:
        raise ValueError("Error: Mass cannot be negative.")
        
    speed = abs(velocity_m_s)
    
    if speed > SPEED_OF_LIGHT:
        raise ValueError("Error: Velocity cannot exceed the speed of light in a vacuum.")
    elif speed > 0.1 * SPEED_OF_LIGHT:
        print("  [!] Warning: Speed is above 10% of c, so classical kinetic energy may be inaccurate.")
        
    energy_joules = 0.5 * mass_kg * (velocity_m_s ** 2)
    return energy_joules

if __name__ == "__main__":
    print("=== Kinetic Energy Calculator ===\n")
    
    # A few everyday and engineering-style examples.
    scenarios = [
        {"name": "Heavy Bowling Ball", "mass": 5.0, "vel": 8.0},
        {"name": "Highway SUV", "mass": 2000.0, "vel": 35.0},
        {"name": "Fast Test Projectile", "mass": 10.0, "vel": 2500.0},
    ]
    
    for s in scenarios:
        try:
            ke = calculate_kinetic_energy(s["mass"], s["vel"])
            print(f"Object: {s['name']}")
            print(f"  |- Mass:  {s['mass']} kg")
            print(f"  |- Speed: {s['vel']} m/s")
            print(f"  => Kinetic Energy: {ke:,.2f} Joules\n")
        except ValueError as e:
            print(f"Simulation failed for {s['name']}: {e}\n")
            
    print("==================================================")
    print("Status: Energy calculations executed successfully.")
