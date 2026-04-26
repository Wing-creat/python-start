# spring_energy.py

def calculate_spring_energy():
    print("--- 🪀 Hooke's Law & Spring Energy Lab ---")
    try:
        # k is the spring constant, x is the displacement
        k = float(input("Enter spring constant k (N/m): "))
        x = float(input("Enter displacement x (m): "))
        
        # Formula: E = 1/2 * k * x^2
        energy = 0.5 * k * (x ** 2)
        
        print("-" * 35)
        print(f"Spring Constant : {k} N/m")
        print(f"Displacement    : {x} m")
        print(f"Elastic Energy  : {energy:.2f} Joules")
        print("-" * 35)
    except ValueError:
        print("Error: Please enter valid numbers.")

if __name__ == "__main__":
    calculate_spring_energy()