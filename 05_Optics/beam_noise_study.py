"""Study how detector-position noise changes repeated beam measurements."""

import math
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", os.path.join(os.getcwd(), ".matplotlib_cache"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

import numpy as np

from beam_alignment import simulate_beam_positions


OUTPUT_PATH = "assets/beam_noise_distributions.png"

def simulate_noisy_measurements(
    true_position: float,
    noise_standard_deviation: float,
    number_of_measurements: int = 500,
    random_seed: int = 42,
) -> np.ndarray:
    """Return repeated beam-position readings with Gaussian noise."""
    if not math.isfinite(true_position):
        raise ValueError("True position must be finite.")
    if (
        not math.isfinite(noise_standard_deviation)
        or noise_standard_deviation < 0
    ):
        raise ValueError("Noise standard deviation must be finite and non-negative.")
    if isinstance(number_of_measurements, bool) or not isinstance(
        number_of_measurements,
        int,
    ):
        raise ValueError("Number of measurements must be an integer.")
    if number_of_measurements <= 0:
        raise ValueError("Number of measurements must be positive.")
    if isinstance(random_seed, bool) or not isinstance(random_seed, int):
        raise ValueError("Random seed must be an integer.")
    if random_seed < 0:
        raise ValueError("Random seed cannot be negative.")

    random_generator = np.random.default_rng(random_seed)
    measurement_noise = random_generator.normal(
        loc=0.0,
        scale=noise_standard_deviation,
        size=number_of_measurements,
    )
    return true_position + measurement_noise


def save_noise_distribution_plot(
    measurements_by_noise: dict[float, np.ndarray],
    true_position: float,
    output_path: str = OUTPUT_PATH,
) -> None:
    """Save repeated beam measurements for several detector-noise levels."""
    noise_levels = list(measurements_by_noise)
    maximum_noise = max(noise_levels)
    histogram_edges = np.linspace(
        true_position - 4 * maximum_noise,
        true_position + 4 * maximum_noise,
        31,
    )
    colors = ("#2563eb", "#f59e0b", "#dc2626")

    figure, axes = plt.subplots(
        1,
        len(noise_levels),
        figsize=(12, 4),
        sharex=True,
        sharey=True,
        squeeze=False,
        layout="constrained",
    )
    for axis, color, noise_level in zip(
        axes[0],
        colors,
        noise_levels,
    ):
        measurements = measurements_by_noise[noise_level]
        axis.hist(
            measurements,
            bins=histogram_edges,
            color=color,
            alpha=0.8,
            edgecolor="white",
        )
        axis.axvline(
            true_position,
            color="black",
            linestyle="--",
            label="True position",
        )
        axis.set_title(f"Noise σ = {noise_level:.2f} pixel")
        axis.set_xlabel("Measured position (detector pixels)")
        axis.grid(axis="y", alpha=0.25)

    axes[0, 0].set_ylabel("Number of measurements")
    axes[0, 0].legend()
    figure.suptitle("Repeated Beam-Position Measurements with Gaussian Noise")

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=180)
    plt.close(figure)


def main() -> None:
    """Run the Day Two detector-noise comparison."""
    tilt_waves = 1.0
    number_of_measurements = 500
    random_seed = 42
    noise_levels = (0.05, 0.20, 0.50)

    true_position = float(simulate_beam_positions(np.array([tilt_waves]))[0])
    measurements_by_noise = {
        noise_level: simulate_noisy_measurements(
            true_position,
            noise_level,
            number_of_measurements,
            random_seed,
        )
        for noise_level in noise_levels
    }
    save_noise_distribution_plot(measurements_by_noise, true_position)

    print("--- Active Optical Alignment: Day Two ---")
    print(f"Wavefront tilt: {tilt_waves:.1f} wave")
    print(f"True beam position: {true_position:.4f} detector pixels")
    print(f"Measurements per noise level: {number_of_measurements}")
    print("Input noise σ | Measured mean | Measured sample σ")
    for noise_level, measurements in measurements_by_noise.items():
        print(
            f"{noise_level:13.2f} | "
            f"{np.mean(measurements):13.4f} | "
            f"{np.std(measurements, ddof=1):17.4f}"
        )
    print("Noise model: Gaussian uncertainty added to the measured centroid")
    print("Feedback control: not included yet")
    print(f"Plot saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
