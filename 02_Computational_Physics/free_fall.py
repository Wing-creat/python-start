# free_fall.py

def calculate_free_fall(time_seconds: float, gravity: float = 9.81) -> dict:
    """
    Calculates the final velocity and total displacement of an object in free fall.
    Assumes standard Earth gravity and a vacuum environment (no air resistance).
    """
    # Kinematics equations
    velocity = gravity * time_seconds
    displacement = 0.5 * gravity * (time_seconds ** 2)
    
    return {
        "time_s": time_seconds,
        "velocity_m_s": round(velocity, 2),
        "displacement_m": round(displacement, 2)
    }

if __name__ == "__main__":
    print("--- 🌍 Physics Engine: Free Fall Simulation ---")
    test_time = 5.0
    results = calculate_free_fall(test_time)
    
    print(f"After {results['time_s']} seconds of free fall:")
    print(f"  -> Speed: {results['velocity_m_s']} m/s")
    print(f"  -> Dropped Distance: {results['displacement_m']} meters")
    print("-" * 47)