"""Plot a hot drink approaching room temperature using Newton's cooling law."""

import os
from math import exp, isfinite

os.environ.setdefault("MPLCONFIGDIR", os.path.join(os.getcwd(), ".matplotlib_cache"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


OUTPUT_PATH = "assets/cooling_curve.png"


def calculate_temperature(
    time_min: float,
    initial_temperature_c: float = 80.0,
    room_temperature_c: float = 22.0,
    cooling_rate_per_min: float = 0.05,
) -> float:
    """Return temperature in Celsius at the given time in minutes."""
    values = (time_min, initial_temperature_c, room_temperature_c, cooling_rate_per_min)
    if not all(isfinite(value) for value in values):
        raise ValueError("Time, temperatures, and cooling rate must be finite.")
    if time_min < 0:
        raise ValueError("Time must be non-negative.")
    if cooling_rate_per_min <= 0:
        raise ValueError("Cooling rate must be positive.")

    temperature_difference = initial_temperature_c - room_temperature_c
    return room_temperature_c + temperature_difference * exp(-cooling_rate_per_min * time_min)


def save_cooling_plot(
    times_min: list[float],
    temperatures_c: list[float],
    room_temperature_c: float,
    output_path: str = OUTPUT_PATH,
) -> None:
    """Save the temperature curve with a room-temperature reference line."""
    figure, axis = plt.subplots(figsize=(9, 5))
    axis.plot(times_min, temperatures_c, color="#dc2626", label="Drink temperature")
    axis.axhline(room_temperature_c, color="#64748b", linestyle="--", label="Room temperature")
    axis.set_title("Hot Drink Cooling: Newton's Cooling Law")
    axis.set_xlabel("Time (min)")
    axis.set_ylabel("Temperature (°C)")
    axis.grid(alpha=0.25)
    axis.legend()
    figure.tight_layout()

    output_directory = os.path.dirname(output_path)
    if output_directory:
        os.makedirs(output_directory, exist_ok=True)
    figure.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(figure)


if __name__ == "__main__":
    # Illustrative parameters, not measurements from a real drink.
    initial_temperature_c = 80.0
    room_temperature_c = 22.0
    cooling_rate_per_min = 0.05
    times_min = list(range(61))
    temperatures_c = [
        calculate_temperature(time, initial_temperature_c, room_temperature_c, cooling_rate_per_min)
        for time in times_min
    ]
    save_cooling_plot(times_min, temperatures_c, room_temperature_c)

    print("--- Hot Drink Cooling (Illustrative Model) ---")
    print("Initial temperature: 80.0 °C; room temperature: 22.0 °C")
    print("Assumed cooling rate: 0.05 per minute")
    for time in (0, 20, 40, 60):
        print(f"After {time:2d} min: {temperatures_c[time]:.2f} °C")
    print(f"Plot saved to {OUTPUT_PATH}")
