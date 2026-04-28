# spring_energy.py

def calculate_elastic_energy(k: float, x: float) -> float:
    """
    Calculates the elastic potential energy stored in a spring.
    Uses Hooke's Law integration: U = 1/2 * k * x^2
    
    Args:
        k (float): Spring constant in Newtons per meter (N/m).
        x (float): Displacement from equilibrium in meters (m).
        
    Returns:
        float: Elastic potential energy in Joules (J).
    """
    return 0.5 * k * (x ** 2)

if __name__ == "__main__":
    print("--- ⚙️ Elastic Potential Energy Calculator ---")
    spring_constant = 150.0  # N/m
    displacement = 0.2       # m
    
    energy = calculate_elastic_energy(spring_constant, displacement)
    
    print("-" * 35)
    print(f"Spring Constant (k): {spring_constant} N/m")
    print(f"Displacement (x)   : {displacement} m")
    print(f"Stored Energy (U)  : {energy:.2f} Joules")
    print("-" * 35)