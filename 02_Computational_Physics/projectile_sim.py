# projectile_sim.py
import math

def calculate_trajectory(v0: float, angle_degrees: float, gravity: float = 9.81):
    """
    Calculates key kinematics metrics of a 2D projectile trajectory.
    """
    angle_radians = math.radians(angle_degrees)
    
    # Physics formulas for ideal trajectory
    time_of_flight = (2 * v0 * math.sin(angle_radians)) / gravity
    max_height = (v0**2 * (math.sin(angle_radians))**2) / (2 * gravity)
    max_range = (v0**2 * math.sin(2 * angle_radians)) / gravity
    
    return time_of_flight, max_height, max_range

if __name__ == "__main__":
    print("--- 🚀 2D Projectile Simulator (Core Math) ---")
    velocity = 50.0  # Initial velocity in m/s
    angle = 45.0     # Launch angle in degrees
    
    t, h, r = calculate_trajectory(velocity, angle)
    
    print("-" * 30)
    print(f"Initial Velocity : {velocity} m/s")
    print(f"Launch Angle     : {angle} degrees")
    print(f"Time of Flight   : {t:.2f} s")
    print(f"Max Height       : {h:.2f} m")
    print(f"Max Range        : {r:.2f} m")
    print("-" * 30)