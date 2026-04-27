# monte_carlo_pi.py
import random

def estimate_pi(num_samples: int) -> float:
    """
    Estimates the value of Pi using the Monte Carlo method.
    
    Args:
        num_samples (int): The number of random points to generate.
        
    Returns:
        float: The estimated value of Pi.
    """
    inside_circle = 0
    
    for _ in range(num_samples):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        # Check if the point is inside the quarter-circle
        if x**2 + y**2 <= 1.0:
            inside_circle += 1
            
    return (inside_circle / num_samples) * 4

if __name__ == "__main__":
    print("--- 🎲 Monte Carlo Pi Estimator ---")
    samples = 1000000
    pi_estimate = estimate_pi(samples)
    print(f"Points Used: {samples:,}")
    print(f"Estimated Pi: {pi_estimate:.6f}")