"""Calibrate a simple spectrometer from detector pixels to wavelength."""

import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", os.path.join(os.getcwd(), ".matplotlib_cache"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


OUTPUT_PATH = "assets/spectrometer_calibration.png"


def _as_finite_1d_array(values: np.ndarray, name: str) -> np.ndarray:
    """Return values as a non-empty, finite one-dimensional float array."""
    array = np.asarray(values, dtype=float)
    if array.ndim != 1 or array.size == 0:
        raise ValueError(f"{name} must be a non-empty 1D array.")
    if not np.all(np.isfinite(array)):
        raise ValueError(f"{name} must contain only finite values.")
    return array


def fit_wavelength_calibration(
    pixel_positions: np.ndarray,
    known_wavelengths_nm: np.ndarray,
) -> tuple[float, float]:
    """Fit wavelength_nm = slope * pixel + intercept."""
    pixel_array = _as_finite_1d_array(pixel_positions, "Pixel positions")
    wavelength_array = _as_finite_1d_array(
        known_wavelengths_nm,
        "Known wavelengths",
    )
    if pixel_array.size < 2 or pixel_array.shape != wavelength_array.shape:
        raise ValueError("Calibration arrays must have matching lengths of at least 2.")
    if np.all(pixel_array == pixel_array[0]):
        raise ValueError("Calibration requires at least two different pixel positions.")

    slope, intercept = np.polyfit(pixel_array, wavelength_array, deg=1)
    return float(slope), float(intercept)


def predict_wavelengths(
    pixel_positions: np.ndarray,
    slope_nm_per_pixel: float,
    intercept_nm: float,
) -> np.ndarray:
    """Convert detector pixel positions to fitted wavelengths in nanometers."""
    pixel_array = _as_finite_1d_array(pixel_positions, "Pixel positions")
    if not np.isfinite(slope_nm_per_pixel) or not np.isfinite(intercept_nm):
        raise ValueError("Calibration slope and intercept must be finite.")
    return slope_nm_per_pixel * pixel_array + intercept_nm


def calculate_residuals_and_rmse(
    known_wavelengths_nm: np.ndarray,
    fitted_wavelengths_nm: np.ndarray,
) -> tuple[np.ndarray, float]:
    """Return signed residuals and root-mean-square error in nanometers."""
    known_array = _as_finite_1d_array(
        known_wavelengths_nm,
        "Known wavelengths",
    )
    fitted_array = _as_finite_1d_array(
        fitted_wavelengths_nm,
        "Fitted wavelengths",
    )
    if known_array.shape != fitted_array.shape:
        raise ValueError("Known and fitted wavelengths must have matching lengths.")

    residuals_nm = known_array - fitted_array
    rmse_nm = float(np.sqrt(np.mean(residuals_nm**2)))
    return residuals_nm, rmse_nm


def save_calibration_plot(
    pixel_positions: np.ndarray,
    known_wavelengths_nm: np.ndarray,
    fitted_wavelengths_nm: np.ndarray,
    residuals_nm: np.ndarray,
    output_path: str = OUTPUT_PATH,
) -> None:
    """Save the wavelength calibration and its signed residuals."""
    pixel_array = _as_finite_1d_array(pixel_positions, "Pixel positions")
    known_array = _as_finite_1d_array(
        known_wavelengths_nm,
        "Known wavelengths",
    )
    fitted_array = _as_finite_1d_array(
        fitted_wavelengths_nm,
        "Fitted wavelengths",
    )
    residual_array = _as_finite_1d_array(residuals_nm, "Residuals")
    if not (
        pixel_array.shape
        == known_array.shape
        == fitted_array.shape
        == residual_array.shape
    ):
        raise ValueError("All plot arrays must have matching lengths.")

    order = np.argsort(pixel_array)
    figure, (calibration_axis, residual_axis) = plt.subplots(
        2,
        1,
        figsize=(8, 7),
        sharex=True,
        layout="constrained",
        gridspec_kw={"height_ratios": [3, 1]},
    )

    calibration_axis.scatter(
        pixel_array,
        known_array,
        color="#2563eb",
        label="Reference lines",
        zorder=3,
    )
    calibration_axis.plot(
        pixel_array[order],
        fitted_array[order],
        color="#dc2626",
        label="Linear calibration",
    )
    for pixel, wavelength_nm in zip(pixel_array, known_array):
        if pixel > 900:
            x_offset = -6
            y_offset = 7 if wavelength_nm > 578 else -14
            horizontal_alignment = "right"
        else:
            x_offset = 5
            y_offset = 6
            horizontal_alignment = "left"
        calibration_axis.annotate(
            f"{wavelength_nm:.1f} nm",
            (pixel, wavelength_nm),
            xytext=(x_offset, y_offset),
            textcoords="offset points",
            fontsize=8,
            ha=horizontal_alignment,
        )

    calibration_axis.set_title("Example Spectrometer Wavelength Calibration")
    calibration_axis.set_ylabel("Known wavelength (nm)")
    calibration_axis.grid(alpha=0.3)
    calibration_axis.legend()

    residual_axis.axhline(0.0, color="black", linewidth=1.0)
    residual_axis.scatter(pixel_array, residual_array, color="#16a34a")
    residual_axis.set_xlabel("Detector position (pixel)")
    residual_axis.set_ylabel("Residual (nm)")
    residual_axis.grid(alpha=0.3)

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=180)
    plt.close(figure)


def main() -> None:
    """Run the teaching example with five reference spectral lines."""
    pixel_positions = np.array([259.0, 383.0, 824.0, 948.0, 957.0])
    known_wavelengths_nm = np.array([404.7, 435.8, 546.1, 577.0, 579.1])
    unknown_pixel = 716.0

    slope, intercept = fit_wavelength_calibration(
        pixel_positions,
        known_wavelengths_nm,
    )
    fitted_wavelengths_nm = predict_wavelengths(
        pixel_positions,
        slope,
        intercept,
    )
    residuals_nm, rmse_nm = calculate_residuals_and_rmse(
        known_wavelengths_nm,
        fitted_wavelengths_nm,
    )
    unknown_wavelength_nm = predict_wavelengths(
        np.array([unknown_pixel]),
        slope,
        intercept,
    )[0]

    save_calibration_plot(
        pixel_positions,
        known_wavelengths_nm,
        fitted_wavelengths_nm,
        residuals_nm,
    )

    print("--- Spectrometer Wavelength Calibration ---")
    print("Teaching example data: not measurements collected by the student")
    print(
        "Calibration equation: wavelength_nm = "
        f"{slope:.6f} * pixel + {intercept:.6f}"
    )
    print(f"Calibration RMSE: {rmse_nm:.4f} nm")
    print(f"Maximum absolute residual: {np.max(np.abs(residuals_nm)):.4f} nm")
    print(
        f"Example unknown peak: pixel {unknown_pixel:.0f} -> "
        f"{unknown_wavelength_nm:.2f} nm"
    )
    print(f"Plot saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
