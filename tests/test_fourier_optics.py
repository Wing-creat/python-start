"""Tests for the introductory Fourier-optics study."""

import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OPTICS_DIRECTORY = PROJECT_ROOT / "05_Optics"
sys.path.insert(0, str(OPTICS_DIRECTORY))

from fourier_optics import (
    calculate_defocus_sensitivity,
    calculate_far_field_intensity,
    create_circular_aperture,
    create_coordinate_grid,
    create_defocused_field,
)
from diffraction_study import save_diffraction_plot
from defocus_study import save_defocus_comparison


class FourierOpticsTests(unittest.TestCase):
    def test_coordinate_grids_have_requested_shape_and_center(self):
        x_grid, y_grid = create_coordinate_grid(101, 2.0)

        self.assertEqual(x_grid.shape, (101, 101))
        self.assertEqual(y_grid.shape, (101, 101))
        self.assertAlmostEqual(x_grid[50, 50], 0.0)
        self.assertAlmostEqual(y_grid[50, 50], 0.0)

    def test_circular_aperture_contains_center_but_not_corner(self):
        x_grid, y_grid = create_coordinate_grid(101, 2.0)
        aperture = create_circular_aperture(x_grid, y_grid, radius=0.35)

        self.assertEqual(aperture[50, 50], 1.0)
        self.assertEqual(aperture[0, 0], 0.0)
        self.assertTrue(np.array_equal(aperture, np.flipud(aperture)))
        self.assertTrue(np.array_equal(aperture, np.fliplr(aperture)))

    def test_invalid_grid_parameters_are_rejected(self):
        for grid_size in (True, 8, 100, 10.5):
            with self.subTest(grid_size=grid_size):
                with self.assertRaises(ValueError):
                    create_coordinate_grid(grid_size, 2.0)

        for physical_size in (0.0, -1.0, float("nan"), float("inf")):
            with self.subTest(physical_size=physical_size):
                with self.assertRaises(ValueError):
                    create_coordinate_grid(101, physical_size)

    def test_invalid_aperture_parameters_are_rejected(self):
        valid_grid = np.zeros((3, 3))

        for radius in (0.0, -1.0, float("nan"), float("inf")):
            with self.subTest(radius=radius):
                with self.assertRaises(ValueError):
                    create_circular_aperture(valid_grid, valid_grid, radius)

        with self.assertRaises(ValueError):
            create_circular_aperture(np.zeros((3, 3)), np.zeros((3, 2)), 1.0)
        with self.assertRaises(ValueError):
            create_circular_aperture(np.zeros(3), np.zeros(3), 1.0)
        with self.assertRaises(ValueError):
            create_circular_aperture(
                np.array([[0.0, float("nan")], [0.0, 0.0]]),
                np.zeros((2, 2)),
                1.0,
            )

    def test_far_field_intensity_is_normalized_and_centered(self):
        x_grid, y_grid = create_coordinate_grid(101, 2.0)
        aperture = create_circular_aperture(x_grid, y_grid, radius=0.35)
        intensity = calculate_far_field_intensity(aperture)

        self.assertEqual(intensity.shape, aperture.shape)
        self.assertTrue(np.all(np.isfinite(intensity)))
        self.assertTrue(np.all(intensity >= 0.0))
        self.assertAlmostEqual(float(np.max(intensity)), 1.0)
        self.assertEqual(
            np.unravel_index(np.argmax(intensity), intensity.shape),
            (50, 50),
        )

    def test_far_field_intensity_is_approximately_symmetric(self):
        x_grid, y_grid = create_coordinate_grid(101, 2.0)
        aperture = create_circular_aperture(x_grid, y_grid, radius=0.35)
        intensity = calculate_far_field_intensity(aperture)

        self.assertTrue(np.allclose(intensity, np.flipud(intensity), atol=1e-12))
        self.assertTrue(np.allclose(intensity, np.fliplr(intensity), atol=1e-12))

    def test_zero_defocus_matches_the_original_aperture(self):
        x_grid, y_grid = create_coordinate_grid(101, 2.0)
        aperture = create_circular_aperture(x_grid, y_grid, radius=0.35)

        field = create_defocused_field(
            aperture,
            x_grid,
            y_grid,
            aperture_radius=0.35,
            defocus_waves=0.0,
        )

        self.assertTrue(np.allclose(field, aperture))

    def test_defocus_changes_phase_but_preserves_aperture_amplitude(self):
        x_grid, y_grid = create_coordinate_grid(101, 2.0)
        aperture = create_circular_aperture(x_grid, y_grid, radius=0.35)

        field = create_defocused_field(
            aperture,
            x_grid,
            y_grid,
            aperture_radius=0.35,
            defocus_waves=0.5,
        )

        self.assertTrue(np.allclose(np.abs(field), aperture))
        self.assertFalse(np.allclose(field, aperture))

    def test_defocus_reduces_the_far_field_peak(self):
        x_grid, y_grid = create_coordinate_grid(101, 2.0)
        aperture = create_circular_aperture(x_grid, y_grid, radius=0.35)
        defocused_field = create_defocused_field(
            aperture,
            x_grid,
            y_grid,
            aperture_radius=0.35,
            defocus_waves=0.5,
        )

        ideal_intensity = calculate_far_field_intensity(aperture, normalize=False)
        defocused_intensity = calculate_far_field_intensity(
            defocused_field,
            normalize=False,
        )

        self.assertLess(np.max(defocused_intensity), np.max(ideal_intensity))

    def test_defocus_sensitivity_starts_at_the_ideal_peak(self):
        x_grid, y_grid = create_coordinate_grid(101, 2.0)
        aperture = create_circular_aperture(x_grid, y_grid, radius=0.35)

        relative_peaks = calculate_defocus_sensitivity(
            aperture,
            x_grid,
            y_grid,
            aperture_radius=0.35,
            defocus_values=np.array([0.0, 0.25, 0.5]),
        )

        self.assertEqual(relative_peaks.shape, (3,))
        self.assertAlmostEqual(relative_peaks[0], 1.0)

    def test_positive_and_negative_defocus_have_equal_sensitivity(self):
        x_grid, y_grid = create_coordinate_grid(101, 2.0)
        aperture = create_circular_aperture(x_grid, y_grid, radius=0.35)

        relative_peaks = calculate_defocus_sensitivity(
            aperture,
            x_grid,
            y_grid,
            aperture_radius=0.35,
            defocus_values=np.array([-0.5, 0.5]),
        )

        self.assertAlmostEqual(relative_peaks[0], relative_peaks[1])

    def test_relative_peak_falls_for_moderate_defocus(self):
        x_grid, y_grid = create_coordinate_grid(101, 2.0)
        aperture = create_circular_aperture(x_grid, y_grid, radius=0.35)

        relative_peaks = calculate_defocus_sensitivity(
            aperture,
            x_grid,
            y_grid,
            aperture_radius=0.35,
            defocus_values=np.array([0.0, 0.25, 0.5]),
        )

        self.assertTrue(np.all(np.diff(relative_peaks) < 0.0))

    def test_invalid_defocus_sweep_values_are_rejected(self):
        grid = np.zeros((3, 3))
        aperture = np.ones((3, 3))

        invalid_values = (
            np.array([]),
            np.array([[0.0, 0.5]]),
            np.array([0.0, float("nan")]),
        )
        for defocus_values in invalid_values:
            with self.subTest(defocus_values=defocus_values):
                with self.assertRaises(ValueError):
                    calculate_defocus_sensitivity(
                        aperture,
                        grid,
                        grid,
                        aperture_radius=1.0,
                        defocus_values=defocus_values,
                    )

    def test_invalid_defocus_parameters_are_rejected(self):
        grid = np.zeros((3, 3))
        aperture = np.ones((3, 3))

        with self.assertRaises(ValueError):
            create_defocused_field(aperture, grid, np.zeros((3, 2)), 1.0, 0.5)

        for aperture_radius in (0.0, float("nan")):
            with self.subTest(aperture_radius=aperture_radius):
                with self.assertRaises(ValueError):
                    create_defocused_field(
                        aperture,
                        grid,
                        grid,
                        aperture_radius,
                        0.5,
                    )

        for defocus_waves in (float("nan"), float("inf")):
            with self.subTest(defocus_waves=defocus_waves):
                with self.assertRaises(ValueError):
                    create_defocused_field(
                        aperture,
                        grid,
                        grid,
                        1.0,
                        defocus_waves,
                    )

    def test_larger_aperture_has_narrower_half_maximum_feature(self):
        x_grid, y_grid = create_coordinate_grid(201, 2.0)
        small_aperture = create_circular_aperture(x_grid, y_grid, radius=0.2)
        large_aperture = create_circular_aperture(x_grid, y_grid, radius=0.4)

        small_intensity = calculate_far_field_intensity(small_aperture)
        large_intensity = calculate_far_field_intensity(large_aperture)
        center = small_intensity.shape[0] // 2
        small_width = np.count_nonzero(small_intensity[center] >= 0.5)
        large_width = np.count_nonzero(large_intensity[center] >= 0.5)

        self.assertLess(large_width, small_width)

    def test_invalid_apertures_are_rejected(self):
        invalid_apertures = (
            np.array([]),
            np.zeros((3, 3)),
            np.array([[1.0, float("nan")], [0.0, 0.0]]),
            np.array([[1.0, float("inf")], [0.0, 0.0]]),
        )

        for aperture in invalid_apertures:
            with self.subTest(aperture=aperture):
                with self.assertRaises(ValueError):
                    calculate_far_field_intensity(aperture)

    def test_plot_can_create_a_custom_output_directory(self):
        x_grid, y_grid = create_coordinate_grid(101, 2.0)
        aperture = create_circular_aperture(x_grid, y_grid, radius=0.4)
        intensity = calculate_far_field_intensity(aperture)

        with tempfile.TemporaryDirectory() as temporary_directory:
            output_path = Path(temporary_directory) / "optics" / "diffraction.png"
            save_diffraction_plot(aperture, intensity, str(output_path))
            self.assertTrue(output_path.is_file())

    def test_defocus_comparison_can_create_a_custom_output_directory(self):
        x_grid, y_grid = create_coordinate_grid(101, 2.0)
        aperture = create_circular_aperture(x_grid, y_grid, radius=0.35)
        defocused_field = create_defocused_field(
            aperture,
            x_grid,
            y_grid,
            aperture_radius=0.35,
            defocus_waves=0.5,
        )
        ideal_intensity = calculate_far_field_intensity(aperture, normalize=False)
        defocused_intensity = calculate_far_field_intensity(
            defocused_field,
            normalize=False,
        )
        ideal_peak = np.max(ideal_intensity)

        with tempfile.TemporaryDirectory() as temporary_directory:
            output_path = Path(temporary_directory) / "optics" / "defocus.png"
            save_defocus_comparison(
                ideal_intensity / ideal_peak,
                defocused_intensity / ideal_peak,
                defocus_waves=0.5,
                output_path=str(output_path),
            )
            self.assertTrue(output_path.is_file())


if __name__ == "__main__":
    unittest.main()
