# plot_monte_carlo.py
import random
import matplotlib.pyplot as plt

def visualize_monte_carlo(num_samples: int = 2000):
    """
    Visualizes the Monte Carlo Pi estimation using a scatter plot.
    """
    inside_x, inside_y = [], []
    outside_x, outside_y = [], []
    
    for _ in range(num_samples):
        x, y = random.random(), random.random()
        if x**2 + y**2 <= 1.0:
            inside_x.append(x)
            inside_y.append(y)
        else:
            outside_x.append(x)
            outside_y.append(y)
            
    # Plotting logic
    plt.figure(figsize=(6, 6))
    plt.scatter(inside_x, inside_y, color='blue', s=3, label='Inside Quarter-Circle')
    plt.scatter(outside_x, outside_y, color='red', s=3, label='Outside Quarter-Circle')
    
    plt.title(f"Monte Carlo Pi Estimation ({num_samples} samples)")
    plt.xlabel("X axis")
    plt.ylabel("Y axis")
    plt.legend(loc="upper right")
    plt.grid(True, linestyle='--', alpha=0.5)
    
    # Save the plot
    plt.savefig("monte_carlo_visualization.png", dpi=300)
    print(f"✅ Monte Carlo visualization ({num_samples} points) saved as 'monte_carlo_visualization.png'!")

if __name__ == "__main__":
    print("--- 🎲 Initializing Monte Carlo Scatter Plot ---")
    visualize_monte_carlo()