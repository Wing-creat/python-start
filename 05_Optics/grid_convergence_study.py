"""Check whether a defocus result stabilizes as the grid is refined."""

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


OUTPUT_PATH = "assets/fourier_optics_grid_convergence.png"


def calculate_defocus_grid_convergence(
    grid_sizes: np.ndarray,
    physical_size: float,
    aperture_radius: float,
    defocus_waves: float,
) -> np.ndarray:
    """Return the relative peak intensity calculated on each grid size."""
    sizes = np.asarray(grid_sizes)
    if sizes.ndim != 1 or sizes.size == 0:
        raise ValueError("Grid sizes must be a non-empty 1D array.")
    if not np.issubdtype(sizes.dtype, np.integer):
        raise ValueError("Grid sizes must contain integers.")

    relative_peaks = []
    for grid_size in sizes:
        x_grid, y_grid = create_coordinate_grid(int(grid_size), physical_size)
        aperture = create_circular_aperture(
            x_grid,
            y_grid,
            aperture_radius,
        )
        peak = calculate_defocus_sensitivity(
            aperture,
            x_grid,
            y_grid,
            aperture_radius,
            np.array([defocus_waves]),
        )[0]
        relative_peaks.append(peak)

    return np.asarray(relative_peaks)


def save_grid_convergence_plot(
    grid_sizes: np.ndarray,
    relative_peaks: np.ndarray,
    defocus_waves: float,
    output_path: str = OUTPUT_PATH,
) -> None:
    """Save relative peak intensity as a function of grid size."""
    sizes = np.asarray(grid_sizes)
    peaks = np.asarray(relative_peaks)
    if sizes.ndim != 1 or sizes.size == 0 or sizes.shape != peaks.shape:
        raise ValueError("Grid sizes and peaks must be matching 1D arrays.")
    if not np.all(np.isfinite(sizes)) or not np.all(np.isfinite(peaks)):
        raise ValueError("Plot values must be finite.")

    figure, axis = plt.subplots(figsize=(7, 4.5), layout="constrained")
    axis.plot(sizes, peaks, marker="o", markersize=5, color="#2563eb")
    axis.set_title(f"Grid Convergence at {defocus_waves:.1f} Waves of Defocus")
    axis.set_xlabel("Grid size (samples per side)")
    axis.set_ylabel("Peak intensity relative to ideal")
    axis.set_xticks(sizes)
    axis.grid(alpha=0.3)

    output_directory = os.path.dirname(output_path)
    if output_directory:
        os.makedirs(output_directory, exist_ok=True)
    figure.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(figure)


if __name__ == "__main__":
    grid_sizes = np.array([33, 65, 129, 257, 513])
    physical_size = 2.0
    aperture_radius = 0.35
    defocus_waves = 0.5

    relative_peaks = calculate_defocus_grid_convergence(
        grid_sizes,
        physical_size,
        aperture_radius,
        defocus_waves,
    )
    save_grid_convergence_plot(
        grid_sizes,
        relative_peaks,
        defocus_waves,
    )

    print("--- Fourier-Optics Grid-Convergence Study ---")
    print(f"Defocus: {defocus_waves:.1f} waves at the aperture edge")
    for grid_size, relative_peak in zip(grid_sizes, relative_peaks):
        print(f"{grid_size:>3} x {grid_size:<3}: {relative_peak:.6f}")
    final_change = abs(relative_peaks[-1] - relative_peaks[-2])
    print(f"Change from the final refinement: {final_change:.6f}")
    print(f"Plot saved to {OUTPUT_PATH}")
