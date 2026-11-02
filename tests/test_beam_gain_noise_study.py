"""Tests for the beam-alignment gain and noise study."""

import math
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OPTICS_DIRECTORY = PROJECT_ROOT / "05_Optics"
sys.path.insert(0, str(OPTICS_DIRECTORY))

from beam_gain_noise_study import (
    calculate_steady_state_rms,
    find_settling_step,
    run_parameter_study,
    save_gain_noise_plot,
)


class BeamGainNoiseStudyTests(unittest.TestCase):
    def test_rms_uses_only_the_requested_final_window(self):
        true_positions = np.array([100.0, 3.0, 4.0])

        rms_error = calculate_steady_state_rms(
            true_positions,
            steady_state_steps=2,
        )

        self.assertAlmostEqual(rms_error, math.sqrt(12.5))

    def test_settling_requires_all_later_positions_to_stay_inside(self):
        true_positions = np.array([0.50, 0.08, 0.15, 0.09, -0.05])

        settling_step = find_settling_step(true_positions, tolerance=0.10)

        self.assertEqual(settling_step, 3)

    def test_settling_returns_zero_when_every_position_is_inside(self):
        true_positions = np.array([0.08, -0.04, 0.02])

        settling_step = find_settling_step(true_positions, tolerance=0.10)

        self.assertEqual(settling_step, 0)

    def test_settling_returns_none_when_the_run_never_stays_inside(self):
        true_positions = np.array([0.50, 0.20, 0.11])

        settling_step = find_settling_step(true_positions, tolerance=0.10)

        self.assertIsNone(settling_step)

    def test_invalid_position_histories_are_rejected(self):
        invalid_histories = (
            np.array([]),
            np.array([[0.1, 0.2]]),
            np.array([0.1, float("nan")]),
        )

        for true_positions in invalid_histories:
            with self.subTest(true_positions=true_positions):
                with self.assertRaises(ValueError):
                    calculate_steady_state_rms(true_positions)
                with self.assertRaises(ValueError):
                    find_settling_step(true_positions)

    def test_invalid_rms_windows_are_rejected(self):
        true_positions = np.array([0.2, 0.1])

        for steady_state_steps in (True, 0, -1, 3, 1.5):
            with self.subTest(steady_state_steps=steady_state_steps):
                with self.assertRaises(ValueError):
                    calculate_steady_state_rms(
                        true_positions,
                        steady_state_steps=steady_state_steps,
                    )

    def test_invalid_settling_tolerances_are_rejected(self):
        true_positions = np.array([0.2, 0.1])

        for tolerance in (0.0, -0.1, float("nan"), float("inf")):
            with self.subTest(tolerance=tolerance):
                with self.assertRaises(ValueError):
                    find_settling_step(true_positions, tolerance=tolerance)


class ParameterStudyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.gain_values = (0.05, 0.20, 0.50)
        cls.noise_levels = (0.00, 0.05, 0.20)
        cls.first_results = run_parameter_study(
            cls.gain_values,
            cls.noise_levels,
        )
        cls.second_results = run_parameter_study(
            cls.gain_values,
            cls.noise_levels,
        )

    def test_study_contains_every_gain_and_noise_pair(self):
        expected_pairs = {
            (gain, noise)
            for gain in self.gain_values
            for noise in self.noise_levels
        }

        self.assertEqual(set(self.first_results), expected_pairs)

    def test_fixed_inputs_reproduce_the_same_study_results(self):
        self.assertEqual(self.first_results, self.second_results)

    def test_study_shows_expected_gain_and_noise_trends(self):
        slow_settling_step = self.first_results[(0.05, 0.00)][1]
        moderate_settling_step = self.first_results[(0.20, 0.00)][1]
        no_noise_rms = self.first_results[(0.20, 0.00)][0]
        high_noise_rms = self.first_results[(0.20, 0.20)][0]

        self.assertIsNotNone(slow_settling_step)
        self.assertIsNotNone(moderate_settling_step)
        self.assertLess(moderate_settling_step, slow_settling_step)
        self.assertGreater(high_noise_rms, no_noise_rms)

    def test_plot_creates_a_custom_output_directory(self):
        results = {(0.20, 0.05): (0.03, 5)}

        with tempfile.TemporaryDirectory() as temporary_directory:
            output_path = (
                Path(temporary_directory)
                / "alignment"
                / "gain_noise.png"
            )
            save_gain_noise_plot(
                results,
                gain_values=(0.20,),
                noise_levels=(0.05,),
                output_path=str(output_path),
            )

            self.assertTrue(output_path.is_file())


if __name__ == "__main__":
    unittest.main()
