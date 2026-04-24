# aero_drag.py

def calculate_drag():
    print("--- ✈️ Aerodynamic Drag Calculator ---")
    print("Formula: F_d = 0.5 * rho * v^2 * C_d * A")
    
    try:
        # Standard air density at sea level and 15°C is approx 1.225 kg/m^3
        rho = 1.225 
        
        v = float(input("Enter vehicle velocity (m/s): "))
        c_d = float(input("Enter drag coefficient (C_d, e.g., 0.3 for a sports car): "))
        area = float(input("Enter frontal cross-sectional area (m^2): "))
        
        # Calculate drag force in Newtons
        drag_force = 0.5 * rho * (v ** 2) * c_d * area
        
        print("-" * 40)
        print(f"Velocity        : {v} m/s")
        print(f"Drag Coefficient: {c_d}")
        print(f"Frontal Area    : {area} m^2")
        print(f"Total Drag Force: {drag_force:.2f} Newtons")
        print("-" * 40)
    except ValueError:
        print("Error: Please enter valid numerical values.")

if __name__ == "__main__":
    calculate_drag()