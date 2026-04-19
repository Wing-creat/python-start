# planet_weights.py

def calculate_weight():
    # 这一行就是程序“开口说话”要数据的地方
    mass = float(input("Enter your mass in kg: "))
    
    planets = {
        "Earth": 9.81,
        "Mars": 3.71,
        "Jupiter": 24.79,
        "Saturn": 10.44
    }
    
    print(f"\nResults for a {mass} kg object:")
    print("-" * 30)
    
    for planet, gravity in planets.items():
        weight = mass * gravity
        print(f"{planet:10}: {weight:.2f} Newtons")

if __name__ == "__main__":
    calculate_weight()