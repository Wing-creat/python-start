# projectile_sim.py
import math

def simulate_projectile():
    print("--- 🏹 Projectile Motion Simulator ---")
    
    try:
        # Get user inputs for launch parameters
        v0 = float(input("Enter initial velocity (m/s): "))
        angle_deg = float(input("Enter launch angle (degrees): "))
    except ValueError:
        print("Error: Please enter numerical values.")
        return

    # Constants
    g = 9.81  # Gravity in m/s^2
    time_step = 0.1
    
    # Convert angle to radians for math functions
    angle_rad = math.radians(angle_deg)
    
    # Initial velocity components
    vx = v0 * math.cos(angle_rad)
    vy = v0 * math.sin(angle_rad)
    
    t = 0.0
    print("-" * 45)
    print(f"{'Time (s)':<10} | {'X (m)':<15} | {'Y (m)':<15}")
    print("-" * 45)

    # Simulation loop
    while True:
        # Calculate positions using kinematic equations
        # x = v0_x * t
        # y = v0_y * t - 0.5 * g * t^2
        x = vx * t
        y = (vy * t) - (0.5 * g * t**2)
        
        # Stop simulation if the object hits the ground
        if y < 0 and t > 0:
            break
            
        print(f"{t:<10.1f} | {x:<15.2f} | {y:<15.2f}")
        t += time_step

    print("-" * 45)
    print("Simulation complete. The object has hit the ground.")

if __name__ == "__main__":
    simulate_projectile()