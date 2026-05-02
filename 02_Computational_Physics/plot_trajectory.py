# plot_trajectory.py
import math
import matplotlib.pyplot as plt

def plot_kinematics(v0: float, angle_degrees: float, gravity: float = 9.81):
    """
    Simulates and visualizes a 2D projectile trajectory using matplotlib.
    """
    angle_radians = math.radians(angle_degrees)
    time_of_flight = (2 * v0 * math.sin(angle_radians)) / gravity
    
    # Generate data points for the trajectory
    times = [t * (time_of_flight / 100) for t in range(101)]
    x_vals = [v0 * math.cos(angle_radians) * t for t in times]
    y_vals = [v0 * math.sin(angle_radians) * t - 0.5 * gravity * (t**2) for t in times]
    
    # Plotting logic
    plt.figure(figsize=(10, 5))
    plt.plot(x_vals, y_vals, label=f'v0 = {v0} m/s, θ = {angle_degrees}°', color='blue', linewidth=2)
    
    plt.title("2D Projectile Motion Trajectory")
    plt.xlabel("Horizontal Distance (m)")
    plt.ylabel("Vertical Height (m)")
    plt.axhline(0, color='black', linewidth=1.5)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    # Save the plot as an image instead of just showing it
    plt.savefig("trajectory_visualization.png", dpi=300)
    print("✅ Trajectory successfully plotted and saved as 'trajectory_visualization.png'!")

if __name__ == "__main__":
    print("--- 🚀 Initializing Trajectory Visualization ---")
    plot_kinematics(velocity=50.0, angle=45.0)