# spring_energy.py

def calculate_elastic_potential_energy(spring_constant: float, displacement: float) -> float:
    """
    Calculates the elastic potential energy (U) stored in a compressed or stretched spring.
    Formula: U = 1/2 * k * x^2
    """
    energy = 0.5 * spring_constant * (displacement ** 2)
    return round(energy, 2)

if __name__ == "__main__":
    print("--- ⚙️ Physics Engine: Hooke's Law Simulation ---")
    k = 500.0  # Spring constant (N/m) - Typical for a stiff mechanical spring
    x = 0.15   # Displacement (meters) - Compressed by 15cm
    
    energy = calculate_elastic_potential_energy(k, x)
    
    print(f"Spring Constant (k): {k} N/m")
    print(f"Displacement (x): {x} m")
    print(f"Stored Potential Energy: {energy} Joules")
    print("-" * 50)