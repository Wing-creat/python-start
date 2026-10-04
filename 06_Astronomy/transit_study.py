"""Generate and plot a simple synthetic exoplanet transit light curve."""

import os

os.environ.setdefault("MPLCONFIGDIR", os.path.join(os.getcwd(), ".matplotlib_cache"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from exoplanet_transit import calculate_flux_at_time


OUTPUT_PATH = "assets/exoplanet_transit_light_curve.png"


def generate_light_curve(
    times: list[float],
    star_radius: float = 1.0,
    planet_radius: float = 0.1,
    transit_speed: float = 0.5,
    impact_parameter: float = 0.0,
) -> list[float]:
    """Return normalized stellar flux for each observation time."""
    return [
        calculate_flux_at_time(
            time,
            star_radius,
            planet_radius,
            transit_speed,
            impact_parameter,
        )
        for time in times
    ]


def save_transit_light_curve(
    times: list[float],
    fluxes: list[float],
    output_path: str = OUTPUT_PATH,
) -> None:
    """Save a plot of normalized stellar flux over time."""
    figure, axis = plt.subplots(figsize=(9, 5.5))
    axis.plot(times, fluxes, color="#2563eb", linewidth=2)
    axis.axhline(1.0, color="#64748b", linestyle="--", linewidth=1)

    axis.set_title("Synthetic Exoplanet Transit Light Curve")
    axis.set_xlabel("Time from mid-transit")
    axis.set_ylabel("Normalized stellar flux")
    axis.set_ylim(0.985, 1.002)
    axis.grid(alpha=0.25)

    figure.tight_layout()
    output_directory = os.path.dirname(output_path)
    if output_directory:
        os.makedirs(output_directory, exist_ok=True)
    figure.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(figure)


if __name__ == "__main__":
    observation_times = [-3.0 + index * 0.02 for index in range(301)]
    observed_fluxes = generate_light_curve(observation_times)
    save_transit_light_curve(observation_times, observed_fluxes)

    print("Synthetic transit parameters:")
    print("  Star radius: 1.0")
    print("  Planet radius: 0.1")
    print("  Transit speed: 0.5")
    print(f"Plot saved to {OUTPUT_PATH}")
