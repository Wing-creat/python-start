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
    calculate_far_field_intensity,
    create_circular_aperture,
    create_coordinate_grid,
)
from diffraction_study import save_diffraction_plot


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


if __name__ == "__main__":
    unittest.main()
