# sensor_data.py
import random
from typing import List

def simulate_ultrasonic_reading(true_distance: float, noise_level: float = 0.5) -> float:
    """
    Simulates a raw ultrasonic sensor reading with random environmental noise.
    """
    noise = random.uniform(-noise_level, noise_level)
    return round(true_distance + noise, 2)

def moving_average_filter(data_stream: List[float], window_size: int = 3) -> List[float]:
    """
    Applies a simple moving average (SMA) filter to smooth out sensor spikes,
    a standard technique in robotics perception systems.
    """
    smoothed_data = []
    for i in range(len(data_stream)):
        # Get the current window of data
        start_idx = max(0, i - window_size + 1)
        window = data_stream[start_idx : i + 1]
        
        # Calculate the average of the window
        window_avg = sum(window) / len(window)
        smoothed_data.append(round(window_avg, 2))
        
    return smoothed_data

if __name__ == "__main__":
    print("--- 🤖 Robotics Sensor Noise Filtering Simulation ---")
    
    # 1. Simulate a robot standing exactly 5.0 meters from a wall
    actual_distance = 5.0
    raw_sensor_data = [simulate_ultrasonic_reading(actual_distance) for _ in range(10)]
    
    print(f"Target Distance: {actual_distance}m")
    print(f"Raw Sensor Array (Noisy): {raw_sensor_data}")
    
    # 2. Apply the moving average filter to clean the data
    cleaned_data = moving_average_filter(raw_sensor_data, window_size=3)
    
    print(f"Filtered Array (Smooth):  {cleaned_data}")
    print("-" * 55)
    print("✅ Noise filtering successfully applied to data stream.")