# aero_drag.py

def calculate_drag_force(density_kg_m3: float, velocity_m_s: float, drag_coeff: float, area_m2: float) -> float:
    """
    Calculates the aerodynamic drag force exerted on a moving body in a fluid.
    
    Formula: F_d = 1/2 * rho * v^2 * C_d * A
    
    Args:
        density_kg_m3 (float): Fluid density (e.g., air is approx 1.225 kg/m^3 at sea level).
        velocity_m_s (float): Velocity of the object relative to the fluid.
        drag_coeff (float): Dimensionless drag coefficient (C_d).
        area_m2 (float): Reference area (typically cross-sectional area).
        
    Returns:
        float: Drag force in Newtons (N).
        
    Raises:
        ValueError: If physical constraints (negative area, density, or Cd) are violated.
    """
    if density_kg_m3 < 0 or drag_coeff < 0 or area_m2 < 0:
        raise ValueError("Error: Density, drag coefficient, and area must be non-negative.")
        
    drag_force = 0.5 * density_kg_m3 * (velocity_m_s ** 2) * drag_coeff * area_m2
    return drag_force

if __name__ == "__main__":
    print("=== 🌪️ Fluid Dynamics: Aerodynamic Drag Simulation ===\n")
    
    # Standard air density at sea level at 15°C
    AIR_DENSITY = 1.225 
    
    # Engineering test scenarios
    vehicles = [
        {
            "type": "Standard Sedan (Cruising)",
            "velocity": 30.0,  # ~108 km/h
            "cd": 0.30,        # Optimized for fuel efficiency
            "area": 2.2
        },
        {
            "type": "Formula 1 Car (High Speed)",
            "velocity": 85.0,  # ~306 km/h
            "cd": 0.85,        # High drag due to intense downforce requirements
            "area": 1.5
        },
        {
            "type": "Heavy Freight Truck",
            "velocity": 25.0,  # ~90 km/h
            "cd": 0.80,        # Boxy shape, poor aerodynamics
            "area": 10.0
        }
    ]
    
    print(f"Environmental Air Density: {AIR_DENSITY} kg/m^3\n")
    
    for v in vehicles:
        try:
            force = calculate_drag_force(AIR_DENSITY, v["velocity"], v["cd"], v["area"])
            print(f"Vehicle: {v['type']}")
            print(f"  |- Speed: {v['velocity']} m/s")
            print(f"  |- C_d:   {v['cd']}")
            print(f"  |- Area:  {v['area']} m^2")
            print(f"  => Aerodynamic Drag Force: {force:.2f} Newtons\n")
        except ValueError as e:
            print(f"Simulation failed for {v['type']}: {e}")
            
    print("==========================================================")
    print("Status: Aerodynamic calculations executed successfully.")