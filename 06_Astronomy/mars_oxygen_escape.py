"""Compare ideal Mars escape speed with thermal speeds of O2 molecules."""

import math
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", os.path.join(os.getcwd(), ".matplotlib_cache"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


GRAVITATIONAL_CONSTANT = 6.67430e-11  # m^3 / (kg s^2)
BOLTZMANN_CONSTANT = 1.380649e-23  # J / K
ATOMIC_MASS_UNIT_KG = 1.66053906660e-27
OXYGEN_MOLECULE_MASS_KG = 32.0 * ATOMIC_MASS_UNIT_KG
MARS_MASS_KG = 6.4171e23
MARS_RADIUS_M = 3.3895e6
OUTPUT_PATH = "assets/mars_oxygen_escape.png"


def _require_positive_finite(value: float, name: str) -> None:
    if not math.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be finite and positive.")


def escape_speed_km_s(planet_mass_kg: float, radius_m: float) -> float:
    """Return ideal escape speed at the supplied radius in km/s."""
    _require_positive_finite(planet_mass_kg, "Planet mass")
    _require_positive_finite(radius_m, "Radius")
    return math.sqrt(2 * GRAVITATIONAL_CONSTANT * planet_mass_kg / radius_m) / 1000


def oxygen_rms_speed_km_s(temperature_k: float) -> float:
    """Return root-mean-square thermal speed of molecular oxygen in km/s."""
    _require_positive_finite(temperature_k, "Temperature")
    return math.sqrt(
        3 * BOLTZMANN_CONSTANT * temperature_k / OXYGEN_MOLECULE_MASS_KG
    ) / 1000


def save_speed_comparison(
    temperatures_k: list[float], output_path: str = OUTPUT_PATH
) -> None:
    """Plot illustrative O2 thermal speeds against Mars surface escape speed."""
    if not temperatures_k or any(
        not math.isfinite(temperature) or temperature <= 0
        for temperature in temperatures_k
    ):
        raise ValueError("Temperatures must be a non-empty list of positive finite values.")

    thermal_speeds = [oxygen_rms_speed_km_s(temperature) for temperature in temperatures_k]
    escape_speed = escape_speed_km_s(MARS_MASS_KG, MARS_RADIUS_M)

    figure, axis = plt.subplots(figsize=(8, 5), layout="constrained")
    axis.plot(temperatures_k, thermal_speeds, color="#2563eb", linewidth=2,
              label="O2 root-mean-square speed")
    axis.axhline(escape_speed, color="#dc2626", linestyle="--",
                 label="Mars surface escape speed")
    axis.set_title("Mars Oxygen: Thermal Speed vs. Escape Speed")
    axis.set_xlabel("Assumed gas temperature (K)")
    axis.set_ylabel("Speed (km/s)")
    axis.set_ylim(bottom=0)
    axis.grid(alpha=0.3)
    axis.legend()

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=180)
    plt.close(figure)


def main() -> None:
    """Run a bounded speed-scale comparison, not an atmosphere-lifetime model."""
    temperatures_k = list(range(150, 601, 10))
    reference_temperature_k = 200.0  # illustrative, not a measured exobase temperature
    escape_speed = escape_speed_km_s(MARS_MASS_KG, MARS_RADIUS_M)
    thermal_speed = oxygen_rms_speed_km_s(reference_temperature_k)
    save_speed_comparison(temperatures_k)

    print("--- Mars Oxygen: Day 1 Speed Comparison ---")
    print(f"Ideal Mars surface escape speed: {escape_speed:.2f} km/s")
    print(f"O2 rms speed at assumed {reference_temperature_k:.0f} K: {thermal_speed:.3f} km/s")
    print(f"Speed ratio (escape / rms): {escape_speed / thermal_speed:.1f}")
    print("This compares typical speed scales, not an escape rate or retention time.")
    print("Real escape occurs in the upper atmosphere and includes non-thermal processes.")
    print(f"Plot saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
