# monte_carlo_pi.py
import random

def estimate_pi(num_darts):
    print(f"--- 🎯 Throwing {num_darts} random darts... ---")
    hits_inside_circle = 0
    
    # Throw darts one by one using a loop
    for _ in range(num_darts):
        # Generate random x and y coordinates between -1.0 and 1.0
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        
        # Check if the dart landed inside the circle using Pythagorean theorem (x^2 + y^2 <= r^2)
        if x**2 + y**2 <= 1.0:
            hits_inside_circle += 1
            
    # Calculate estimated Pi based on the ratio of hits
    estimated_pi = 4 * (hits_inside_circle / num_darts)
    return estimated_pi

if __name__ == "__main__":
    darts = 1000000  # Let's throw 1 MILLION darts!
    pi_result = estimate_pi(darts)
    
    print("-" * 35)
    print(f"Estimated Pi : {pi_result}")
    print(f"Actual Pi    : 3.1415926535...")
    print("-" * 35)