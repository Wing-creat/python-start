"""Explore how wind changes estimated cold-weather feels-like temperature."""

import os
from math import isfinite
from pathlib import Path


def calculate_wind_chill(temperature_c: float, wind_kmh: float) -> float:
    """Return wind chill in Celsius for air <= 10 C and wind >= 5 km/h.

    Metric wind chill formula: https://www.climat.weather.gc.ca/glossary_e.html
    Wind means standard weather-station wind measured at 10 metres height.
    """
    if not isfinite(temperature_c) or not isfinite(wind_kmh):
        raise ValueError("Temperature and wind speed must be finite.")
    if temperature_c > 10 or wind_kmh < 5:
        raise ValueError("Use air temperature <= 10 C and wind speed >= 5 km/h.")

    wind_factor = wind_kmh ** 0.16
    return (13.12 + 0.6215 * temperature_c - 11.37 * wind_factor
            + 0.3965 * temperature_c * wind_factor)


def main() -> None:
    # Change this illustrative temperature to explore another cold evening.
    temperature_c = 5.0
    wind_speeds = list(range(5, 41))
    wind_chills = [calculate_wind_chill(temperature_c, wind) for wind in wind_speeds]

    print("Wind Chill Study (illustrative, not live weather)")
    print(f"Actual air temperature: {temperature_c:.1f} C")
    for wind in (5, 10, 20, 40):
        chill = calculate_wind_chill(temperature_c, wind)
        print(f"Wind {wind:2d} km/h -> wind chill {chill:5.1f} C")

    os.environ.setdefault("MPLCONFIGDIR", ".matplotlib_cache")
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    figure, axis = plt.subplots(figsize=(8, 5))
    axis.plot(wind_speeds, wind_chills, label="Estimated wind chill")
    axis.axhline(temperature_c, color="gray", linestyle="--", label="Actual air temperature")
    axis.set(title="A Cold Evening: Wind and Feels-Like Temperature",
             xlabel="Wind speed (km/h)", ylabel="Temperature (°C)")
    axis.grid(alpha=0.25)
    axis.legend()
    figure.tight_layout()
    output_path = Path("assets/wind_chill.png")
    output_path.parent.mkdir(exist_ok=True)
    figure.savefig(output_path, dpi=150)
    plt.close(figure)
    print(f"Plot saved to {output_path}")


if __name__ == "__main__":
    main()
