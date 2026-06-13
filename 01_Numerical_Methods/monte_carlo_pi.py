# monte_carlo_pi.py
import random
import math

def estimate_pi(num_samples: int) -> float:
    """
    Estimates the value of Pi using the Monte Carlo method.
    """
    if num_samples <= 0:
        raise ValueError("Error: Number of samples must be positive.")

    inside_circle = 0
    for _ in range(num_samples):
        x, y = random.random(), random.random()
        if x**2 + y**2 <= 1.0:
            inside_circle += 1
    return (inside_circle / num_samples) * 4

def run_simulation_study():
    """
    Runs multiple simulations to demonstrate error convergence.
    """
    print(f"{'Samples':<12} | {'Estimated Pi':<15} | {'Error (%)':<10}")
    print("-" * 45)
    
    sample_sizes = [1000, 10000, 100000, 1000000]
    
    for size in sample_sizes:
        try:
            pi_estimate = estimate_pi(size)
            error = abs(pi_estimate - math.pi) / math.pi * 100
            print(f"{size:<12,} | {pi_estimate:<15.6f} | {error:<10.4f}%")
        except ValueError as e:
            print(f"{size:<12,} | Calculation failed: {e}")

if __name__ == "__main__":
    print("--- Monte Carlo Pi Estimation ---")
    print(f"True Pi Reference: {math.pi:.6f}\n")
    
    run_simulation_study()
    
    print("\nLarger sample sizes usually give estimates closer to pi.")
