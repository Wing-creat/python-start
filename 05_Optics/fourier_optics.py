"""Small numerical tools for an introductory Fourier-optics study."""

import math

import numpy as np


def create_coordinate_grid(
    grid_size: int,
    physical_size: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Return centered two-dimensional coordinate grids."""
    if isinstance(grid_size, bool) or not isinstance(grid_size, int):
        raise ValueError("Grid size must be an integer.")
    if grid_size < 9 or grid_size % 2 == 0:
        raise ValueError("Grid size must be an odd integer of at least 9.")
    if not math.isfinite(physical_size) or physical_size <= 0:
        raise ValueError("Physical size must be positive and finite.")

    coordinates = np.linspace(
        -physical_size / 2,
        physical_size / 2,
        grid_size,
    )
    return np.meshgrid(coordinates, coordinates)


def create_circular_aperture(
    x_grid: np.ndarray,
    y_grid: np.ndarray,
    radius: float,
) -> np.ndarray:
    """Return 1 inside a centered circular aperture and 0 outside it."""
    if x_grid.ndim != 2 or y_grid.ndim != 2 or x_grid.shape != y_grid.shape:
        raise ValueError("Coordinate grids must be matching 2D arrays.")
    if x_grid.size == 0 or not np.all(np.isfinite(x_grid)):
        raise ValueError("The x-coordinate grid must contain finite values.")
    if not np.all(np.isfinite(y_grid)):
        raise ValueError("The y-coordinate grid must contain finite values.")
    if not math.isfinite(radius) or radius <= 0:
        raise ValueError("Aperture radius must be positive and finite.")

    distance_from_center = np.sqrt(x_grid**2 + y_grid**2)
    return (distance_from_center <= radius).astype(float)


def calculate_far_field_intensity(aperture: np.ndarray) -> np.ndarray:
    """Return normalized Fraunhofer intensity for an aperture field."""
    aperture_array = np.asarray(aperture)
    if aperture_array.ndim != 2 or aperture_array.size == 0:
        raise ValueError("Aperture must be a non-empty 2D array.")
    if not np.all(np.isfinite(aperture_array)):
        raise ValueError("Aperture values must be finite.")
    if not np.any(np.abs(aperture_array) > 0):
        raise ValueError("Aperture must contain at least one non-zero value.")

    far_field_amplitude = np.fft.fftshift(
        np.fft.fft2(np.fft.ifftshift(aperture_array))
    )
    intensity = np.abs(far_field_amplitude) ** 2
    return intensity / np.max(intensity)
