# ema_filter.py

def apply_ema_filter(current_value: float, previous_ema: float, alpha: float) -> float:
    """Return one step of an exponential moving average filter."""
    if not 0 < alpha <= 1:
        raise ValueError("alpha must be greater than 0 and less than or equal to 1.")

    return alpha * current_value + (1 - alpha) * previous_ema

if __name__ == "__main__":
    alpha = 0.2
    readings = [10.2, 10.5, 9.8, 15.0, 10.1, 10.3]
    ema = readings[0]

    print("EMA Filter Example")
    print(f"alpha = {alpha}\n")

    for reading in readings:
        ema = apply_ema_filter(reading, ema, alpha)
        print(f"reading: {reading:<4} -> ema: {ema:.2f}")
