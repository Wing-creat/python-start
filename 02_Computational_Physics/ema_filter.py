# ema_filter.py

def apply_ema_filter(current_value: float, previous_ema: float, alpha: float) -> float:
    """
    Applies an Exponential Moving Average (EMA) filter to a data stream.
    Formula: Y[n] = alpha * X[n] + (1 - alpha) * Y[n-1]
    
    Args:
        current_value (float): The new raw sensor reading.
        previous_ema (float): The filtered value from the previous step.
        alpha (float): Smoothing factor (0 < alpha <= 1). 
                       Smaller alpha means smoother but slower response.
    """
    return (alpha * current_value) + (1.0 - alpha) * previous_ema

if __name__ == "__main__":
    print("=== 📡 Robotics Signal Processing: EMA Filter Simulation ===\n")
    
    # Simulation Parameters
    smoothing_alpha = 0.2  # High smoothing
    raw_data_stream = [10.2, 10.5, 9.8, 15.0, 10.1, 10.3] # 15.0 is a potential outlier/noise
    
    print(f"Filter Configuration: Alpha = {smoothing_alpha}")
    print(f"Raw Input: {raw_data_stream}\n")
    
    filtered_output = []
    current_ema = raw_data_stream[0] # Initialize EMA with the first reading
    
    for val in raw_data_stream:
        current_ema = apply_ema_filter(val, current_ema, smoothing_alpha)
        filtered_output.append(round(current_ema, 2))
        print(f"Input: {val:<6} | Filtered: {current_ema:.2f}")
        
    print("\nResult: High-frequency noise suppressed successfully.")
    print("==========================================================")