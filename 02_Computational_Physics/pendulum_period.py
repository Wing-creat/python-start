# pendulum_period.py
import math

def calculate_pendulum_period(length_m: float, gravity_m_s2: float = 9.81) -> float:
    """
    Calculates the period of a simple ideal pendulum.
    Formula: T = 2 * pi * sqrt(L / g)
    
    Args:
        length_m (float): Length of the pendulum string in meters.
        gravity_m_s2 (float): Local acceleration due to gravity (must be > 0).
        
    Returns:
        float: The time period of one full swing (oscillation) in seconds.
    """
    if length_m < 0:
        raise ValueError("Error: Pendulum length cannot be negative.")
    if gravity_m_s2 <= 0:
        raise ValueError("Error: Gravity must be strictly positive to maintain oscillation.")
        
    period_seconds = 2 * math.pi * math.sqrt(length_m / gravity_m_s2)
    return period_seconds

if __name__ == "__main__":
    print("=== ⏱️ Physics Engine: Simple Pendulum Simulator ===\n")
    
    # Standard pendulum length (1 meter)
    test_length = 1.0
    print(f"Pendulum Length: {test_length} meter(s)\n")
    
    # Testing across different celestial environments
    environments = [
        {"body": "Earth", "g": 9.81},
        {"body": "Moon",  "g": 1.62},
        {"body": "Jupiter", "g": 24.79}
    ]
    
    for env in environments:
        try:
            period = calculate_pendulum_period(test_length, env["g"])
            print(f"Environment: {env['body']}")
            print(f"  |- Local Gravity: {env['g']} m/s^2")
            print(f"  => Swing Period:  {period:.3f} seconds\n")
        except ValueError as e:
            print(f"Simulation failed for {env['body']}: {e}\n")
            
    print("==================================================")
    print("Status: Kinematic oscillation calculated successfully.")