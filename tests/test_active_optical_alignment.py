"""Tests for the active optical alignment study."""

import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OPTICS_DIRECTORY = PROJECT_ROOT / "05_Optics"
sys.path.insert(0, str(OPTICS_DIRECTORY))

from beam_alignment import (
    fit_tilt_calibration,
    measure_horizontal_centroid,
    save_calibration_plot,
    simulate_beam_positions,
)


class ActiveOpticalAlignmentTests(unittest.TestCase):
    def test_centroid_measures_a_known_subpixel_position(self):
        intensity = np.zeros((5, 5))
        intensity[2, 2] = 1.0
        intensity[2, 3] = 3.0

        position = measure_horizontal_centroid(
            intensity,
            detector_half_width=2,
        )

        self.assertAlmostEqual(position, 0.75)

    def test_centered_intensity_has_zero_position(self):
        intensity = np.zeros((5, 5))
        intensity[2, 2] = 1.0

        position = measure_horizontal_centroid(
            intensity,
            detector_half_width=2,
        )

        self.assertAlmostEqual(position, 0.0)

    def test_invalid_intensity_arrays_are_rejected(self):
        invalid_arrays = (
            np.array([]),
            np.zeros(5),
            np.zeros((5, 5)),
            np.full((5, 5), -1.0),
            np.full((5, 5), float("nan")),
            np.full((5, 5), float("inf")),
        )

        for intensity in invalid_arrays:
            with self.subTest(shape=intensity.shape):
                with self.assertRaises(ValueError):
                    measure_horizontal_centroid(
                        intensity,
                        detector_half_width=2,
                    )

    def test_invalid_detector_windows_are_rejected(self):
        intensity = np.ones((5, 5))

        for detector_half_width in (True, -1, 2.5, 3):
            with self.subTest(detector_half_width=detector_half_width):
                with self.assertRaises(ValueError):
                    measure_horizontal_centroid(
                        intensity,
                        detector_half_width=detector_half_width,
                    )

    def test_zero_tilt_produces_a_centered_beam(self):
        positions = simulate_beam_positions(
            np.array([0.0]),
            grid_size=101,
            detector_half_width=15,
        )

        self.assertAlmostEqual(positions[0], 0.0, places=10)

    def test_positive_and_negative_tilts_produce_opposite_positions(self):
        positions = simulate_beam_positions(
            np.array([-1.0, 1.0]),
            grid_size=101,
            detector_half_width=15,
        )

        self.assertLess(positions[0], 0.0)
        self.assertGreater(positions[1], 0.0)
        self.assertAlmostEqual(positions[0], -positions[1], places=10)

    def test_larger_tilt_produces_a_larger_beam_displacement(self):
        positions = simulate_beam_positions(
            np.array([1.0, 2.0]),
            grid_size=101,
            detector_half_width=15,
        )

        self.assertGreater(abs(positions[1]), abs(positions[0]))

    def test_invalid_tilt_arrays_are_rejected(self):
        invalid_tilt_values = (
            np.array([]),
            np.array([[0.0, 1.0]]),
            np.array([0.0, float("nan")]),
            np.array([0.0, float("inf")]),
        )

        for tilt_values in invalid_tilt_values:
            with self.subTest(shape=tilt_values.shape):
                with self.assertRaises(ValueError):
                    simulate_beam_positions(
                        tilt_values,
                        grid_size=101,
                        detector_half_width=15,
                    )

    def test_calibration_fit_recovers_a_known_line(self):
        tilt_values = np.array([-1.0, 0.0, 1.0])
        beam_positions = np.array([-2.5, 0.5, 3.5])

        slope, intercept = fit_tilt_calibration(
            tilt_values,
            beam_positions,
        )

        self.assertAlmostEqual(slope, 3.0)
        self.assertAlmostEqual(intercept, 0.5)

    def test_invalid_calibration_arrays_are_rejected(self):
        invalid_pairs = (
            (np.array([0.0]), np.array([0.0])),
            (np.array([0.0, 1.0]), np.array([0.0])),
            (np.array([0.0, 1.0]), np.array([0.0, float("nan")])),
            (np.array([1.0, 1.0]), np.array([2.0, 3.0])),
        )

        for tilt_values, beam_positions in invalid_pairs:
            with self.subTest(
                tilt_shape=tilt_values.shape,
                position_shape=beam_positions.shape,
            ):
                with self.assertRaises(ValueError):
                    fit_tilt_calibration(tilt_values, beam_positions)

    def test_calibration_plot_creates_a_custom_output_directory(self):
        tilt_values = np.array([-1.0, 0.0, 1.0])
        beam_positions = np.array([-3.0, 0.0, 3.0])

        with tempfile.TemporaryDirectory() as temporary_directory:
            output_path = (
                Path(temporary_directory)
                / "alignment"
                / "calibration.png"
            )
            save_calibration_plot(
                tilt_values,
                beam_positions,
                slope=3.0,
                intercept=0.0,
                output_path=str(output_path),
            )

            self.assertTrue(output_path.is_file())


if __name__ == "__main__":
    unittest.main()
