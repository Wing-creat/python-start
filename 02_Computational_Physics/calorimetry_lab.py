"""Model a simple calorimetry experiment using conservation of energy."""

import os
from math import isfinite
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", os.path.join(os.getcwd(), ".matplotlib_cache"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


WATER_SPECIFIC_HEAT_J_G_C = 4.184
OUTPUT_PATH = "assets/calorimetry_lab.png"
METAL_SPECIFIC_HEATS_J_G_C = {
    "Aluminum": 0.897,
    "Iron": 0.449,
    "Copper": 0.385,
}


def _require_positive(value: float, name: str) -> None:
    """Require a finite, positive physical quantity."""
    if not isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be finite and positive.")


def _require_finite_temperature(temperature_c: float) -> None:
    """Require a finite temperature value."""
    if not isfinite(temperature_c):
        raise ValueError("Temperature must be finite.")


def calculate_equilibrium_temperature(
    metal_mass_g: float,
    metal_specific_heat_j_g_c: float,
    metal_initial_temperature_c: float,
    water_mass_g: float,
    water_initial_temperature_c: float,
    water_specific_heat_j_g_c: float = WATER_SPECIFIC_HEAT_J_G_C,
) -> float:
    """Return the shared final temperature from an ideal energy balance."""
    _require_positive(metal_mass_g, "Metal mass")
    _require_positive(metal_specific_heat_j_g_c, "Metal specific heat")
    _require_positive(water_mass_g, "Water mass")
    _require_positive(water_specific_heat_j_g_c, "Water specific heat")
    _require_finite_temperature(metal_initial_temperature_c)
    _require_finite_temperature(water_initial_temperature_c)

    metal_heat_capacity_j_c = metal_mass_g * metal_specific_heat_j_g_c
    water_heat_capacity_j_c = water_mass_g * water_specific_heat_j_g_c

    return (
        metal_heat_capacity_j_c * metal_initial_temperature_c
        + water_heat_capacity_j_c * water_initial_temperature_c
    ) / (metal_heat_capacity_j_c + water_heat_capacity_j_c)


def calculate_heat_transfer(
    mass_g: float,
    specific_heat_j_g_c: float,
    initial_temperature_c: float,
    final_temperature_c: float,
) -> float:
    """Return signed heat transfer using Q = m c (T_final - T_initial)."""
    _require_positive(mass_g, "Mass")
    _require_positive(specific_heat_j_g_c, "Specific heat")
    _require_finite_temperature(initial_temperature_c)
    _require_finite_temperature(final_temperature_c)

    return mass_g * specific_heat_j_g_c * (
        final_temperature_c - initial_temperature_c
    )


def save_calorimetry_plot(
    metal_masses_g: list[float],
    temperatures_by_material: dict[str, list[float]],
    output_path: str = OUTPUT_PATH,
) -> None:
    """Save equilibrium temperature curves for several hot metals."""
    figure, axis = plt.subplots(figsize=(8, 5), layout="constrained")

    for material, temperatures_c in temperatures_by_material.items():
        axis.plot(
            metal_masses_g,
            temperatures_c,
            linewidth=2,
            label=material,
        )

    axis.set_title("Hot Metal Placed in 100 g of Water")
    axis.set_xlabel("Metal mass (g)")
    axis.set_ylabel("Equilibrium temperature (°C)")
    axis.grid(alpha=0.3)
    axis.legend(title="Metal at 100 °C")

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=180)
    plt.close(figure)


def main() -> None:
    """Run the three-metal calorimetry comparison."""
    water_mass_g = 100.0
    water_initial_temperature_c = 20.0
    example_metal_mass_g = 100.0
    metal_initial_temperature_c = 100.0

    metal_masses_g = [float(mass_g) for mass_g in range(20, 301, 10)]
    temperatures_by_material = {
        material: [
            calculate_equilibrium_temperature(
                metal_mass_g,
                specific_heat,
                metal_initial_temperature_c,
                water_mass_g,
                water_initial_temperature_c,
            )
            for metal_mass_g in metal_masses_g
        ]
        for material, specific_heat in METAL_SPECIFIC_HEATS_J_G_C.items()
    }
    save_calorimetry_plot(metal_masses_g, temperatures_by_material)

    print("--- Simple Calorimetry Lab ---")
    print("100 g metal at 100 °C placed in 100 g water at 20 °C")
    print("Material | Final temp | Metal Q | Water Q | Balance")

    for material, specific_heat in METAL_SPECIFIC_HEATS_J_G_C.items():
        final_temperature_c = calculate_equilibrium_temperature(
            example_metal_mass_g,
            specific_heat,
            metal_initial_temperature_c,
            water_mass_g,
            water_initial_temperature_c,
        )
        metal_heat_j = calculate_heat_transfer(
            example_metal_mass_g,
            specific_heat,
            metal_initial_temperature_c,
            final_temperature_c,
        )
        water_heat_j = calculate_heat_transfer(
            water_mass_g,
            WATER_SPECIFIC_HEAT_J_G_C,
            water_initial_temperature_c,
            final_temperature_c,
        )
        balance_j = metal_heat_j + water_heat_j

        print(
            f"{material:8} | {final_temperature_c:8.2f} °C | "
            f"{metal_heat_j:7.1f} J | {water_heat_j:7.1f} J | "
            f"{balance_j:+.2e} J"
        )

    print("Negative Q means the metal loses heat; positive Q means water gains heat.")
    print("Assumption: no heat is lost to the cup or surrounding air.")
    print(f"Plot saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
