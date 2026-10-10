"""Illustrate an IDEA open-top printed boat's payload-to-boat mass score."""

import os
from math import isfinite

os.environ.setdefault("MPLCONFIGDIR", os.path.join(os.getcwd(), ".matplotlib_cache"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


OUTPUT_PATH = "assets/buoyancy_score.png"


def _validate_masses(boat_mass: float, payload_mass: float) -> None:
    if not isfinite(boat_mass) or boat_mass <= 0:
        raise ValueError("Boat mass must be finite and positive.")
    if not isfinite(payload_mass) or payload_mass < 0:
        raise ValueError("Payload mass must be finite and non-negative.")


def calculate_buoyancy_score(boat_mass: float, payload_mass: float) -> float:
    """Return payload mass / boat mass, with both masses in the same units."""
    _validate_masses(boat_mass, payload_mass)
    return payload_mass / boat_mass


def calculate_displaced_water_mass(boat_mass: float, payload_mass: float) -> float:
    """Return required displaced-water mass for static floating equilibrium."""
    _validate_masses(boat_mass, payload_mass)
    return boat_mass + payload_mass


def save_buoyancy_plot(
    boat_mass: float,
    payload_mass: float,
    output_path: str = OUTPUT_PATH,
) -> None:
    """Compare masses relative to the boat, whose mass is one unit."""
    score = calculate_buoyancy_score(boat_mass, payload_mass)
    displaced_mass_ratio = calculate_displaced_water_mass(boat_mass, payload_mass) / boat_mass

    figure, axis = plt.subplots(figsize=(9, 5))
    bars = axis.bar(
        ["Boat", "Iron-ball payload", "Required displaced water"],
        [1.0, score, displaced_mass_ratio],
        color=["#64748b", "#2563eb", "#16a34a"],
    )
    axis.bar_label(bars, fmt="%.1f", padding=4)
    axis.set_title(f"IDEA Boat Project: Buoyancy Score = {score:.1f}")
    axis.set_ylabel("Mass / boat mass (boat = 1.0)")
    axis.set_ylim(0, max(1.0, displaced_mass_ratio) * 1.18)
    axis.grid(axis="y", alpha=0.25)
    axis.set_axisbelow(True)
    figure.tight_layout()

    output_directory = os.path.dirname(output_path)
    if output_directory:
        os.makedirs(output_directory, exist_ok=True)
    figure.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(figure)


if __name__ == "__main__":
    # Relative units illustrate the reported score; these are not measured grams.
    boat_mass = 1.0
    payload_mass = 27.8

    print("--- IDEA Project 1: Printed Boat ---")
    print("Assumed score definition: payload mass / boat mass")
    print(f"Buoyancy score: {calculate_buoyancy_score(boat_mass, payload_mass):.1f}")
    print("Masses are normalized to boat mass = 1.0.")
    print(f"Required displaced-water mass: {calculate_displaced_water_mass(boat_mass, payload_mass):.1f}")
    print("This is an equilibrium requirement, not a prediction of boat capacity.")
    save_buoyancy_plot(boat_mass, payload_mass)
    print(f"Plot saved to {OUTPUT_PATH}")
