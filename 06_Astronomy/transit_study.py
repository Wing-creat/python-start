"""Generate and plot a simple synthetic exoplanet transit light curve."""

import os

os.environ.setdefault("MPLCONFIGDIR", os.path.join(os.getcwd(), ".matplotlib_cache"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from exoplanet_transit import calculate_flux_at_time


OUTPUT_PATH = "assets/exoplanet_transit_light_curve.png"
COMPARISON_OUTPUT_PATH = "assets/exoplanet_transit_parameter_comparison.png"


def generate_light_curve(
    times: list[float],
    star_radius: float = 1.0,
    planet_radius: float = 0.1,
    transit_speed: float = 0.5,
    impact_parameter: float = 0.0,
) -> list[float]:
    """Return normalized stellar flux for each observation time."""
    if not times:
        raise ValueError("At least one observation time is required.")

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
    if len(times) != len(fluxes):
        raise ValueError("Times and fluxes must contain the same number of values.")

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


def save_parameter_comparison(
    times: list[float],
    output_path: str = COMPARISON_OUTPUT_PATH,
) -> None:
    """Save light curves comparing planet size and transit path."""
    figure, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)

    planet_radii = [0.05, 0.10, 0.15]
    impact_parameters = [0.0, 0.6, 1.0]
    colors = ["#16a34a", "#2563eb", "#dc2626"]

    for planet_radius, color in zip(planet_radii, colors):
        fluxes = generate_light_curve(times, planet_radius=planet_radius)
        axes[0].plot(
            times,
            fluxes,
            color=color,
            label=f"Planet radius = {planet_radius:.2f}",
        )

    for impact_parameter, color in zip(impact_parameters, colors):
        fluxes = generate_light_curve(
            times,
            impact_parameter=impact_parameter,
        )
        axes[1].plot(
            times,
            fluxes,
            color=color,
            label=f"Impact parameter = {impact_parameter:.1f}",
        )

    axes[0].set_title("Changing Planet Size")
    axes[1].set_title("Changing Transit Path")
    axes[0].set_ylabel("Normalized stellar flux")

    for axis in axes:
        axis.set_xlabel("Time from mid-transit")
        axis.set_ylim(0.975, 1.002)
        axis.grid(alpha=0.25)
        axis.legend()

    figure.suptitle("How Transit Parameters Change the Light Curve")
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
    save_parameter_comparison(observation_times)

    print("Synthetic transit parameters:")
    print("  Star radius: 1.0")
    print("  Planet radius: 0.1")
    print("  Transit speed: 0.5")
    print(f"Plot saved to {OUTPUT_PATH}")
    print(f"Comparison saved to {COMPARISON_OUTPUT_PATH}")
