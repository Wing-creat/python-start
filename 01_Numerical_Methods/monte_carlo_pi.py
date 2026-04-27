# monte_carlo_pi.py
import random
import math

def estimate_pi(num_samples: int) -> float:
    """
    Estimates the value of Pi using the Monte Carlo method.
    """
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
    
    # Testing different sample magnitudes
    sample_sizes = [1000, 10000, 100000, 1000000]
    
    for size in sample_sizes:
        pi_estimate = estimate_pi(size)
        error = abs(pi_estimate - math.pi) / math.pi * 100
        print(f"{size:<12,} | {pi_estimate:<15.6f} | {error:<10.4f}%")

if __name__ == "__main__":
    print("--- 🎲 Monte Carlo Pi: Convergence & Error Analysis ---")
    print(f"True Pi Reference: {math.pi:.6f}\n")
    
    run_simulation_study()
    
    print("\n[Engineering Insight]: As sample size increases, the error percentage ")
    print("generally decreases, demonstrating the Law of Large Numbers.")