# thermal_expansion.py

def calculate_expansion():
    print("--- 🌡️ Linear Thermal Expansion Calculator ---")
    print("Formula: dL = alpha * L0 * dT")
    
    try:
        length = float(input("Enter original length (m): "))
        temp_change = float(input("Enter temperature change (Celsius): "))
        # Standard alpha for structural steel is approx 0.000012
        alpha = float(input("Enter linear expansion coefficient (e.g., 0.000012 for steel): "))
        
        delta_l = alpha * length * temp_change
        new_length = length + delta_l
        
        print("-" * 40)
        print(f"Original Length : {length} m")
        print(f"Expansion       : {delta_l:.6f} m")
        print(f"New Length      : {new_length:.6f} m")
        print("-" * 40)
    except ValueError:
        print("Error: Please enter valid numerical values.")

if __name__ == "__main__":
    calculate_expansion()