"""Tests for the introductory spectrometer calibration study."""

import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OPTICS_DIRECTORY = PROJECT_ROOT / "05_Optics"
sys.path.insert(0, str(OPTICS_DIRECTORY))

from spectrometer_calibration import (
    calculate_residuals_and_rmse,
    fit_wavelength_calibration,
    predict_wavelengths,
    save_calibration_plot,
)


class SpectrometerCalibrationTests(unittest.TestCase):
    def test_linear_fit_recovers_a_known_calibration(self):
        pixel_positions = np.array([100.0, 200.0, 300.0])
        known_wavelengths_nm = np.array([400.0, 450.0, 500.0])

        slope, intercept = fit_wavelength_calibration(
            pixel_positions,
            known_wavelengths_nm,
        )

        self.assertAlmostEqual(slope, 0.5)
        self.assertAlmostEqual(intercept, 350.0)

    def test_prediction_converts_pixels_to_wavelengths(self):
        predicted_wavelengths_nm = predict_wavelengths(
            np.array([150.0, 250.0]),
            slope_nm_per_pixel=0.5,
            intercept_nm=350.0,
        )

        np.testing.assert_allclose(predicted_wavelengths_nm, [425.0, 475.0])

    def test_residuals_are_known_minus_fitted(self):
        residuals_nm, rmse_nm = calculate_residuals_and_rmse(
            known_wavelengths_nm=np.array([400.0, 451.0, 500.0]),
            fitted_wavelengths_nm=np.array([400.0, 450.0, 500.0]),
        )

        np.testing.assert_allclose(residuals_nm, [0.0, 1.0, 0.0])
        self.assertAlmostEqual(rmse_nm, np.sqrt(1.0 / 3.0))

    def test_invalid_calibration_arrays_are_rejected(self):
        invalid_pairs = (
            (np.array([100.0]), np.array([400.0])),
            (np.array([100.0, 200.0]), np.array([400.0])),
            (np.array([[100.0, 200.0]]), np.array([400.0, 450.0])),
            (np.array([100.0, float("nan")]), np.array([400.0, 450.0])),
            (np.array([100.0, 200.0]), np.array([400.0, float("inf")])),
            (np.array([100.0, 100.0]), np.array([400.0, 450.0])),
        )

        for pixel_positions, known_wavelengths_nm in invalid_pairs:
            with self.subTest(
                pixel_shape=pixel_positions.shape,
                wavelength_shape=known_wavelengths_nm.shape,
            ):
                with self.assertRaises(ValueError):
                    fit_wavelength_calibration(
                        pixel_positions,
                        known_wavelengths_nm,
                    )

    def test_non_finite_prediction_inputs_are_rejected(self):
        invalid_inputs = (
            (np.array([100.0, float("nan")]), 0.5, 350.0),
            (np.array([100.0]), float("inf"), 350.0),
            (np.array([100.0]), 0.5, float("nan")),
        )

        for pixel_positions, slope, intercept in invalid_inputs:
            with self.subTest(slope=slope, intercept=intercept):
                with self.assertRaises(ValueError):
                    predict_wavelengths(pixel_positions, slope, intercept)

    def test_invalid_residual_arrays_are_rejected(self):
        invalid_pairs = (
            (np.array([]), np.array([])),
            (np.array([400.0, 450.0]), np.array([400.0])),
            (np.array([[400.0, 450.0]]), np.array([400.0, 450.0])),
            (np.array([400.0, float("nan")]), np.array([400.0, 450.0])),
        )

        for known_wavelengths_nm, fitted_wavelengths_nm in invalid_pairs:
            with self.subTest(
                known_shape=known_wavelengths_nm.shape,
                fitted_shape=fitted_wavelengths_nm.shape,
            ):
                with self.assertRaises(ValueError):
                    calculate_residuals_and_rmse(
                        known_wavelengths_nm,
                        fitted_wavelengths_nm,
                    )

    def test_plot_creates_a_custom_output_directory(self):
        pixel_positions = np.array([100.0, 200.0, 300.0])
        known_wavelengths_nm = np.array([400.0, 451.0, 500.0])
        fitted_wavelengths_nm = np.array([400.0, 450.0, 500.0])
        residuals_nm = known_wavelengths_nm - fitted_wavelengths_nm

        with tempfile.TemporaryDirectory() as temporary_directory:
            output_path = (
                Path(temporary_directory)
                / "spectrometer"
                / "calibration.png"
            )
            save_calibration_plot(
                pixel_positions,
                known_wavelengths_nm,
                fitted_wavelengths_nm,
                residuals_nm,
                output_path=str(output_path),
            )

            self.assertTrue(output_path.is_file())


if __name__ == "__main__":
    unittest.main()
