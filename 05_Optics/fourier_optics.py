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


def create_defocused_field(
    aperture: np.ndarray,
    x_grid: np.ndarray,
    y_grid: np.ndarray,
    aperture_radius: float,
    defocus_waves: float,
) -> np.ndarray:
    """Apply a simple quadratic defocus phase to an aperture field."""
    aperture_array = np.asarray(aperture)
    x_array = np.asarray(x_grid)
    y_array = np.asarray(y_grid)

    if aperture_array.ndim != 2 or aperture_array.size == 0:
        raise ValueError("Aperture must be a non-empty 2D array.")
    if x_array.ndim != 2 or y_array.ndim != 2:
        raise ValueError("Coordinate grids must be matching 2D arrays.")
    if (
        x_array.shape != aperture_array.shape
        or y_array.shape != aperture_array.shape
    ):
        raise ValueError("Aperture and coordinate grids must have matching shapes.")
    if not np.all(np.isfinite(aperture_array)):
        raise ValueError("Aperture values must be finite.")
    if not np.all(np.isfinite(x_array)) or not np.all(np.isfinite(y_array)):
        raise ValueError("Coordinate grids must contain finite values.")
    if not math.isfinite(aperture_radius) or aperture_radius <= 0:
        raise ValueError("Aperture radius must be positive and finite.")
    if not math.isfinite(defocus_waves):
        raise ValueError("Defocus must be finite.")

    normalized_radius_squared = (x_array**2 + y_array**2) / aperture_radius**2
    phase = 2 * np.pi * defocus_waves * normalized_radius_squared
    return aperture_array.astype(complex) * np.exp(1j * phase)


def calculate_far_field_intensity(
    optical_field: np.ndarray,
    normalize: bool = True,
) -> np.ndarray:
    """Return Fraunhofer intensity for an aperture field."""
    field_array = np.asarray(optical_field)
    if field_array.ndim != 2 or field_array.size == 0:
        raise ValueError("Optical field must be a non-empty 2D array.")
    if not np.all(np.isfinite(field_array)):
        raise ValueError("Optical field values must be finite.")
    if not np.any(np.abs(field_array) > 0):
        raise ValueError("Optical field must contain at least one non-zero value.")

    far_field_amplitude = np.fft.fftshift(
        np.fft.fft2(np.fft.ifftshift(field_array))
    )
    intensity = np.abs(far_field_amplitude) ** 2
    if normalize:
        return intensity / np.max(intensity)
    return intensity
