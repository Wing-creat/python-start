# free_fall.py

def calculate_free_fall(time_seconds: float, gravity: float = 9.81) -> dict:
    """
    Calculates the kinematics of an object in free fall within a vacuum.
    
    Args:
        time_seconds (float): Duration of the fall in seconds. Must be non-negative.
        gravity (float): Gravitational acceleration (default: Earth 9.81 m/s^2).
        
    Returns:
        dict: Contains final velocity (m/s) and total displacement (m).
        
    Raises:
        ValueError: If time_seconds is negative or gravity is not positive.
    """
    if time_seconds < 0:
        raise ValueError("Error: Time cannot be negative in classical kinematics.")
    if gravity <= 0:
        raise ValueError("Error: Gravity must be positive.")
        
    velocity = gravity * time_seconds
    displacement = 0.5 * gravity * (time_seconds ** 2)
    
    return {
        "time_s": time_seconds,
        "velocity_m_s": round(velocity, 2),
        "displacement_m": round(displacement, 2)
    }

if __name__ == "__main__":
    print("=== Free Fall Calculator ===\n")
    
    test_scenarios = [1.0, 3.0, 10.0]
    
    for t in test_scenarios:
        try:
            results = calculate_free_fall(t)
            print(f"Simulation: {results['time_s']} seconds of free fall")
            print(f"  |- Final Speed:   {results['velocity_m_s']} m/s")
            print(f"  |- Distance Fell: {results['displacement_m']} meters\n")
        except ValueError as e:
            print(f"Simulation failed: {e}\n")
            
    print("===============================================")
    print("Status: Free fall calculations complete.")
