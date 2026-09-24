"""Check whether a defocus result stabilizes as the grid is refined."""

import numpy as np

from fourier_optics import (
    calculate_defocus_sensitivity,
    create_circular_aperture,
    create_coordinate_grid,
)


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
