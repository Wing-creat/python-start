"""Compare two simple filters on noisy distance-sensor readings."""

import os
import random

os.environ.setdefault("MPLCONFIGDIR", os.path.join(os.getcwd(), ".matplotlib_cache"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from ema_filter import apply_ema_filter
from sensor_data import moving_average_filter, simulate_ultrasonic_reading


OUTPUT_PATH = "assets/sensor_filter_comparison.png"


def apply_ema_to_readings(readings: list, alpha: float) -> list:
    """Apply the EMA formula to a complete list of readings."""
    if not readings:
        return []

    filtered_readings = [readings[0]]
    current_ema = readings[0]

    for reading in readings[1:]:
        current_ema = apply_ema_filter(reading, current_ema, alpha)
        filtered_readings.append(round(current_ema, 2))

    return filtered_readings


def mean_absolute_error(measured_values: list, true_values: list) -> float:
    """Return the average absolute difference from the true values."""
    if not measured_values or len(measured_values) != len(true_values):
        raise ValueError("Value lists must be non-empty and have equal lengths.")

    total_error = sum(
        abs(measured - true)
        for measured, true in zip(measured_values, true_values)
    )
    return total_error / len(true_values)


def run_filter_comparison(seed: int = 7) -> dict:
    """Generate noisy readings, apply both filters, and save a plot."""
    random.seed(seed)

    # The simulated robot moves to three different distances from a wall.
    true_distances = [5.0] * 30 + [8.0] * 30 + [6.5] * 30
    raw_readings = [
        simulate_ultrasonic_reading(distance, noise_level=0.8)
        for distance in true_distances
    ]
    moving_average = moving_average_filter(raw_readings, window_size=5)
    exponential_average = apply_ema_to_readings(raw_readings, alpha=0.35)

    errors = {
        "Raw sensor": mean_absolute_error(raw_readings, true_distances),
        "Moving average": mean_absolute_error(moving_average, true_distances),
        "EMA": mean_absolute_error(exponential_average, true_distances),
    }

    sample_numbers = list(range(1, len(true_distances) + 1))
    plt.figure(figsize=(11, 6))
    plt.plot(
        sample_numbers,
        true_distances,
        color="#111827",
        linestyle="--",
        linewidth=2.2,
        label="True distance",
    )
    plt.scatter(
        sample_numbers,
        raw_readings,
        color="#9ca3af",
        s=18,
        alpha=0.65,
        label="Raw sensor",
    )
    plt.plot(
        sample_numbers,
        moving_average,
        color="#2563eb",
        linewidth=2.0,
        label="Moving average (window = 5)",
    )
    plt.plot(
        sample_numbers,
        exponential_average,
        color="#ea580c",
        linewidth=2.0,
        label="EMA (alpha = 0.35)",
    )

    plt.title("Noisy Distance Sensor: Simple Filter Comparison")
    plt.xlabel("Reading number")
    plt.ylabel("Distance (m)")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend()

    os.makedirs("assets", exist_ok=True)
    plt.savefig(OUTPUT_PATH, dpi=300, bbox_inches="tight")
    plt.close()

    print("--- Sensor Filter Comparison ---")
    print("Mean absolute error (lower is better):")
    for filter_name, error in errors.items():
        print(f"  {filter_name:<16}: {error:.3f} m")
    print("\nFilters reduce noise, but they respond more slowly when distance changes.")
    print(f"Plot saved to {OUTPUT_PATH}")

    return {
        "true_distances": true_distances,
        "raw_readings": raw_readings,
        "moving_average": moving_average,
        "exponential_average": exponential_average,
        "errors": errors,
    }


if __name__ == "__main__":
    run_filter_comparison()
