"""Compare the escape velocities of several Solar System bodies."""

import math
import os

os.environ.setdefault("MPLCONFIGDIR", os.path.join(os.getcwd(), ".matplotlib_cache"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


GRAVITATIONAL_CONSTANT = 6.67430e-11
OUTPUT_PATH = "assets/escape_velocity.png"

# Approximate masses and mean radii in SI units.
SOLAR_SYSTEM_BODIES = {
    "Moon": {"mass_kg": 7.342e22, "radius_m": 1.7374e6},
    "Mars": {"mass_kg": 6.4171e23, "radius_m": 3.3895e6},
    "Earth": {"mass_kg": 5.9722e24, "radius_m": 6.371e6},
    "Neptune": {"mass_kg": 1.02413e26, "radius_m": 2.4622e7},
    "Jupiter": {"mass_kg": 1.89813e27, "radius_m": 6.9911e7},
}


def calculate_escape_velocity_km_s(mass_kg: float, radius_m: float) -> float:
    """Return ideal escape velocity at the surface in kilometers per second."""
    if mass_kg <= 0:
        raise ValueError("Mass must be positive.")
    if radius_m <= 0:
        raise ValueError("Radius must be positive.")

    velocity_m_per_s = math.sqrt(
        2 * GRAVITATIONAL_CONSTANT * mass_kg / radius_m
    )
    return velocity_m_per_s / 1000


def calculate_body_escape_velocities(bodies: dict = SOLAR_SYSTEM_BODIES) -> dict:
    """Return escape velocities for a dictionary of celestial bodies."""
    if not bodies:
        raise ValueError("At least one celestial body is required.")

    escape_velocities = {}
    for name, properties in bodies.items():
        escape_velocities[name] = calculate_escape_velocity_km_s(
            properties["mass_kg"],
            properties["radius_m"],
        )

    return escape_velocities


def save_escape_velocity_plot(
    escape_velocities: dict,
    output_path: str = OUTPUT_PATH,
) -> None:
    """Save a horizontal bar chart of escape velocity by body."""
    if not escape_velocities:
        raise ValueError("At least one escape velocity is required.")

    names = list(escape_velocities.keys())
    velocities = list(escape_velocities.values())
    colors = ["#94a3b8", "#dc6b3f", "#2563eb", "#3b82a0", "#d69e2e"]

    figure, axis = plt.subplots(figsize=(10, 6))
    bars = axis.barh(names, velocities, color=colors[: len(names)])

    for bar, velocity in zip(bars, velocities):
        axis.text(
            velocity + max(velocities) * 0.015,
            bar.get_y() + bar.get_height() / 2,
            f"{velocity:.2f} km/s",
            va="center",
        )

    axis.set_title("Escape Velocity Across the Solar System")
    axis.set_xlabel("Escape Velocity (km/s)")
    axis.set_xlim(0, max(velocities) * 1.18)
    axis.grid(axis="x", linestyle="--", alpha=0.4)
    axis.set_axisbelow(True)

    figure.tight_layout()
    output_directory = os.path.dirname(output_path)
    if output_directory:
        os.makedirs(output_directory, exist_ok=True)
    figure.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(figure)


if __name__ == "__main__":
    results = calculate_body_escape_velocities()
    save_escape_velocity_plot(results)

    print("--- Escape Velocity Across the Solar System ---")
    print(f"{'Body':<10} | {'Escape Velocity':>18}")
    print("-" * 32)
    for body_name, velocity in results.items():
        print(f"{body_name:<10} | {velocity:>13.2f} km/s")

    print(
        "\nThese are ideal surface values that ignore atmosphere "
        "and planetary rotation."
    )
    print(f"Plot saved to {OUTPUT_PATH}")
