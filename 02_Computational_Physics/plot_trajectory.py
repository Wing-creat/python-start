# plot_trajectory.py
import math
import os
import matplotlib.pyplot as plt
from typing import List

def plot_multiple_trajectories(v0: float, angles: List[float], gravity: float = 9.81):
    """
    Visualizes multiple 2D projectile trajectories to compare launch angles.

    Saves the output directly to the assets folder.
    """
    plt.figure(figsize=(10, 6))
    
    # Use a small color palette so each launch angle is easy to compare.
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    for i, angle_degrees in enumerate(angles):
        angle_radians = math.radians(angle_degrees)
        time_of_flight = (2 * v0 * math.sin(angle_radians)) / gravity
        
        # Generate 100 data points for smooth curves
        times = [t * (time_of_flight / 100) for t in range(101)]
        x_vals = [v0 * math.cos(angle_radians) * t for t in times]
        y_vals = [v0 * math.sin(angle_radians) * t - 0.5 * gravity * (t**2) for t in times]
        
        max_range = max(x_vals)
        max_height = max(y_vals)
        
        plt.plot(x_vals, y_vals, 
                 label=f'{angle_degrees}° (Range: {max_range:.1f}m, Height: {max_height:.1f}m)', 
                 color=colors[i % len(colors)], linewidth=2.5, alpha=0.8)
    
    # Chart formatting
    plt.title(f"Projectile Kinematics: Launch Angle Comparison (v0 = {v0} m/s)", fontsize=14, pad=15)
    plt.xlabel("Horizontal Distance (m)", fontsize=12)
    plt.ylabel("Vertical Height (m)", fontsize=12)
    plt.axhline(0, color='black', linewidth=1.5)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(loc="upper right", framealpha=0.9)
    
    os.makedirs("assets", exist_ok=True)

    plt.savefig("assets/trajectory_visualization.png", dpi=300, bbox_inches='tight')
    print("Multi-angle trajectory plot saved to assets/trajectory_visualization.png")

if __name__ == "__main__":
    print("--- Projectile Trajectory Visualization ---")
    test_angles = [30.0, 45.0, 60.0, 75.0]
    plot_multiple_trajectories(v0=50.0, angles=test_angles)
