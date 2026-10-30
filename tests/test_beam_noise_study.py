"""Tests for the noisy beam-position measurement study."""

import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OPTICS_DIRECTORY = PROJECT_ROOT / "05_Optics"
sys.path.insert(0, str(OPTICS_DIRECTORY))

from beam_noise_study import (
    save_noise_distribution_plot,
    simulate_noisy_measurements,
)


class BeamNoiseStudyTests(unittest.TestCase):
    def test_zero_noise_repeats_the_true_position(self):
        measurements = simulate_noisy_measurements(
            true_position=2.5,
            noise_standard_deviation=0.0,
            number_of_measurements=8,
            random_seed=42,
        )

        self.assertTrue(np.array_equal(measurements, np.full(8, 2.5)))

    def test_fixed_seed_reproduces_the_same_measurements(self):
        first_measurements = simulate_noisy_measurements(
            true_position=2.5,
            noise_standard_deviation=0.2,
            number_of_measurements=20,
            random_seed=42,
        )
        second_measurements = simulate_noisy_measurements(
            true_position=2.5,
            noise_standard_deviation=0.2,
            number_of_measurements=20,
            random_seed=42,
        )

        self.assertTrue(np.array_equal(first_measurements, second_measurements))

    def test_larger_noise_produces_a_larger_measurement_spread(self):
        low_noise = simulate_noisy_measurements(
            true_position=2.5,
            noise_standard_deviation=0.1,
            number_of_measurements=500,
            random_seed=42,
        )
        high_noise = simulate_noisy_measurements(
            true_position=2.5,
            noise_standard_deviation=0.5,
            number_of_measurements=500,
            random_seed=42,
        )

        self.assertGreater(np.std(high_noise), np.std(low_noise))

    def test_invalid_true_positions_are_rejected(self):
        for true_position in (float("nan"), float("inf")):
            with self.subTest(true_position=true_position):
                with self.assertRaises(ValueError):
                    simulate_noisy_measurements(
                        true_position=true_position,
                        noise_standard_deviation=0.2,
                    )

    def test_invalid_noise_standard_deviations_are_rejected(self):
        for noise_standard_deviation in (
            -0.1,
            float("nan"),
            float("inf"),
        ):
            with self.subTest(
                noise_standard_deviation=noise_standard_deviation,
            ):
                with self.assertRaises(ValueError):
                    simulate_noisy_measurements(
                        true_position=2.5,
                        noise_standard_deviation=noise_standard_deviation,
                    )

    def test_invalid_measurement_counts_are_rejected(self):
        for number_of_measurements in (True, 0, -1, 2.5):
            with self.subTest(number_of_measurements=number_of_measurements):
                with self.assertRaises(ValueError):
                    simulate_noisy_measurements(
                        true_position=2.5,
                        noise_standard_deviation=0.2,
                        number_of_measurements=number_of_measurements,
                    )

    def test_invalid_random_seeds_are_rejected(self):
        for random_seed in (True, -1, 2.5):
            with self.subTest(random_seed=random_seed):
                with self.assertRaises(ValueError):
                    simulate_noisy_measurements(
                        true_position=2.5,
                        noise_standard_deviation=0.2,
                        random_seed=random_seed,
                    )

    def test_noise_plot_creates_a_custom_output_directory(self):
        measurements_by_noise = {
            0.05: np.array([2.45, 2.50, 2.55]),
            0.20: np.array([2.30, 2.50, 2.70]),
            0.50: np.array([2.00, 2.50, 3.00]),
        }

        with tempfile.TemporaryDirectory() as temporary_directory:
            output_path = (
                Path(temporary_directory)
                / "alignment"
                / "noise.png"
            )
            save_noise_distribution_plot(
                measurements_by_noise,
                true_position=2.5,
                output_path=str(output_path),
            )

            self.assertTrue(output_path.is_file())


if __name__ == "__main__":
    unittest.main()
