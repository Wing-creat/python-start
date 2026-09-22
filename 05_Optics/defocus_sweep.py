"""Measure how defocus changes the peak of a diffraction pattern."""

import os

os.environ.setdefault("MPLCONFIGDIR", os.path.join(os.getcwd(), ".matplotlib_cache"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from fourier_optics import (
    calculate_defocus_sensitivity,
    create_circular_aperture,
    create_coordinate_grid,
)


OUTPUT_PATH = "assets/defocus_sensitivity_sweep.png"


def save_defocus_sensitivity_plot(
    defocus_values: np.ndarray,
    relative_peaks: np.ndarray,
    output_path: str = OUTPUT_PATH,
) -> None:
    """Save relative peak intensity as a function of defocus."""
    values = np.asarray(defocus_values)
    peaks = np.asarray(relative_peaks)
    if values.ndim != 1 or values.size == 0 or values.shape != peaks.shape:
        raise ValueError("Defocus values and peaks must be matching 1D arrays.")
    if not np.all(np.isfinite(values)) or not np.all(np.isfinite(peaks)):
        raise ValueError("Plot values must be finite.")

    figure, axis = plt.subplots(figsize=(7, 4.5), layout="constrained")
    axis.plot(values, peaks, marker="o", markersize=4, color="#2563eb")
    axis.set_title("Peak Intensity Sensitivity to Defocus")
    axis.set_xlabel("Defocus at aperture edge (waves)")
    axis.set_ylabel("Peak intensity relative to ideal")
    axis.set_xlim(values[0], values[-1])
    axis.set_ylim(0.0, 1.05)
    axis.grid(alpha=0.3)

    output_directory = os.path.dirname(output_path)
    if output_directory:
        os.makedirs(output_directory, exist_ok=True)
    figure.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(figure)


if __name__ == "__main__":
    grid_size = 257
    physical_size = 2.0
    aperture_radius = 0.35
    defocus_values = np.linspace(0.0, 1.0, 21)

    x_grid, y_grid = create_coordinate_grid(grid_size, physical_size)
    aperture = create_circular_aperture(x_grid, y_grid, aperture_radius)
    relative_peaks = calculate_defocus_sensitivity(
        aperture,
        x_grid,
        y_grid,
        aperture_radius,
        defocus_values,
    )
    save_defocus_sensitivity_plot(defocus_values, relative_peaks)

    print("--- Defocus Sensitivity Sweep ---")
    print(
        f"Defocus range: {defocus_values[0]:.1f} "
        f"to {defocus_values[-1]:.1f} waves"
    )
    print(f"Number of samples: {defocus_values.size}")
    print(f"Peak at zero defocus: {relative_peaks[0]:.3f}")
    print(f"Peak at 0.5 waves: {relative_peaks[10]:.3f}")
    print(f"Peak at 1.0 wave: {relative_peaks[-1]:.3f}")
    print(f"Plot saved to {OUTPUT_PATH}")
