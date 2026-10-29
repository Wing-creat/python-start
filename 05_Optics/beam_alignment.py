"""Measure far-field beam position for a simple optical-alignment study."""

import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", os.path.join(os.getcwd(), ".matplotlib_cache"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

import numpy as np

from fourier_optics import (
    calculate_far_field_intensity,
    create_circular_aperture,
    create_coordinate_grid,
    create_tilted_field,
)


OUTPUT_PATH = "assets/beam_tilt_calibration.png"


def measure_horizontal_centroid(
    intensity: np.ndarray,
    detector_half_width: int = 30,
) -> float:
    """Return the horizontal intensity centroid in detector-pixel offsets."""
    intensity_array = np.asarray(intensity)
    if intensity_array.ndim != 2 or intensity_array.size == 0:
        raise ValueError("Intensity must be a non-empty 2D array.")
    if not np.all(np.isfinite(intensity_array)):
        raise ValueError("Intensity values must be finite.")
    if np.any(intensity_array < 0):
        raise ValueError("Intensity values cannot be negative.")
    if isinstance(detector_half_width, bool) or not isinstance(
        detector_half_width,
        int,
    ):
        raise ValueError("Detector half-width must be an integer.")
    if detector_half_width < 0:
        raise ValueError("Detector half-width cannot be negative.")

    window_size = 2 * detector_half_width + 1
    if window_size > min(intensity_array.shape):
        raise ValueError("Detector window must fit inside the intensity array.")

    center_row = intensity_array.shape[0] // 2
    center_column = intensity_array.shape[1] // 2
    row_slice = slice(
        center_row - detector_half_width,
        center_row + detector_half_width + 1,
    )
    column_slice = slice(
        center_column - detector_half_width,
        center_column + detector_half_width + 1,
    )
    detector_window = intensity_array[row_slice, column_slice]
    total_intensity = float(np.sum(detector_window))
    if total_intensity <= 0:
        raise ValueError("Detector window must contain positive intensity.")

    horizontal_profile = np.sum(detector_window, axis=0)
    pixel_offsets = np.arange(-detector_half_width, detector_half_width + 1)
    return float(np.sum(pixel_offsets * horizontal_profile) / total_intensity)


def simulate_beam_positions(
    tilt_values: np.ndarray,
    grid_size: int = 257,
    physical_size: float = 2.0,
    aperture_radius: float = 0.35,
    detector_half_width: int = 30,
) -> np.ndarray:
    """Return measured beam positions for several horizontal wavefront tilts."""
    tilt_array = np.asarray(tilt_values, dtype=float)
    if tilt_array.ndim != 1 or tilt_array.size == 0:
        raise ValueError("Tilt values must be a non-empty 1D array.")
    if not np.all(np.isfinite(tilt_array)):
        raise ValueError("Tilt values must be finite.")

    x_grid, y_grid = create_coordinate_grid(grid_size, physical_size)
    aperture = create_circular_aperture(
        x_grid,
        y_grid,
        aperture_radius,
    )
    beam_positions = []

    for tilt_waves in tilt_array:
        tilted_field = create_tilted_field(
            aperture,
            x_grid,
            y_grid,
            aperture_radius,
            float(tilt_waves),
        )
        intensity = calculate_far_field_intensity(tilted_field)
        beam_positions.append(
            measure_horizontal_centroid(intensity, detector_half_width)
        )

    return np.asarray(beam_positions)


def fit_tilt_calibration(
    tilt_values: np.ndarray,
    beam_positions: np.ndarray,
) -> tuple[float, float]:
    """Fit beam position = slope * tilt + intercept."""
    tilt_array = np.asarray(tilt_values, dtype=float)
    position_array = np.asarray(beam_positions, dtype=float)
    if tilt_array.ndim != 1 or position_array.ndim != 1:
        raise ValueError("Calibration values must be 1D arrays.")
    if tilt_array.size < 2 or tilt_array.shape != position_array.shape:
        raise ValueError("Calibration arrays must have matching lengths of at least 2.")
    if not np.all(np.isfinite(tilt_array)) or not np.all(
        np.isfinite(position_array)
    ):
        raise ValueError("Calibration values must be finite.")
    if np.all(tilt_array == tilt_array[0]):
        raise ValueError("Calibration requires at least two different tilt values.")

    slope, intercept = np.polyfit(tilt_array, position_array, deg=1)
    return float(slope), float(intercept)


def save_calibration_plot(
    tilt_values: np.ndarray,
    beam_positions: np.ndarray,
    slope: float,
    intercept: float,
    output_path: str = OUTPUT_PATH,
) -> None:
    """Save measured beam positions and their noise-free calibration line."""
    tilt_array = np.asarray(tilt_values, dtype=float)
    position_array = np.asarray(beam_positions, dtype=float)
    fitted_positions = slope * tilt_array + intercept

    figure, axis = plt.subplots(figsize=(7, 4.5), layout="constrained")
    axis.plot(
        tilt_array,
        position_array,
        "o",
        color="#2563eb",
        label="FFT centroid measurement",
    )
    axis.plot(
        tilt_array,
        fitted_positions,
        color="#dc2626",
        label=f"Linear fit: {slope:.3f} pixels/wave",
    )
    axis.axhline(0.0, color="black", linewidth=0.8, alpha=0.5)
    axis.set_title("Noise-Free Beam Tilt Calibration")
    axis.set_xlabel("Wavefront tilt across aperture (waves)")
    axis.set_ylabel("Horizontal beam position (detector pixels)")
    axis.grid(alpha=0.3)
    axis.legend()

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=180)
    plt.close(figure)


def main() -> None:
    """Run the Day One noise-free beam-position calibration."""
    tilt_values = np.linspace(-2.0, 2.0, 17)
    beam_positions = simulate_beam_positions(tilt_values)
    slope, intercept = fit_tilt_calibration(tilt_values, beam_positions)
    save_calibration_plot(
        tilt_values,
        beam_positions,
        slope,
        intercept,
    )

    zero_tilt_index = int(np.argmin(np.abs(tilt_values)))
    print("--- Active Optical Alignment: Day One ---")
    print(f"Calibration slope: {slope:.4f} detector pixels per wave")
    print(f"Calibration intercept: {intercept:.4e} detector pixels")
    print(
        "Zero-tilt position: "
        f"{beam_positions[zero_tilt_index]:.4e} detector pixels"
    )
    print("Noise and feedback control: not included in this baseline")
    print(f"Plot saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
