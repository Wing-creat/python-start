"""Tests for the multi-seed beam-control validation study."""

import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OPTICS_DIRECTORY = PROJECT_ROOT / "05_Optics"
sys.path.insert(0, str(OPTICS_DIRECTORY))

from beam_control_validation import (
    collect_rms_trials,
    save_validation_plot,
    summarize_rms_trials,
)


class BeamControlValidationTests(unittest.TestCase):
    def test_summary_calculates_mean_and_sample_standard_deviation(self):
        rms_trials = {(0.20, 0.05): np.array([1.0, 2.0, 3.0])}

        summary = summarize_rms_trials(rms_trials)

        mean_rms, sample_standard_deviation = summary[(0.20, 0.05)]
        self.assertAlmostEqual(mean_rms, 2.0)
        self.assertAlmostEqual(sample_standard_deviation, 1.0)

    def test_invalid_trial_arrays_are_rejected(self):
        invalid_trials = (
            np.array([1.0]),
            np.array([[1.0, 2.0]]),
            np.array([1.0, float("nan")]),
        )

        for trial_values in invalid_trials:
            with self.subTest(trial_values=trial_values):
                with self.assertRaises(ValueError):
                    summarize_rms_trials({(0.20, 0.05): trial_values})


class MultiSeedControlTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.gain_values = (0.05, 0.20, 0.50)
        cls.noise_levels = (0.05, 0.20)
        cls.random_seeds = (1, 2, 3, 4, 5)
        cls.first_trials = collect_rms_trials(
            cls.gain_values,
            cls.noise_levels,
            cls.random_seeds,
        )
        cls.second_trials = collect_rms_trials(
            cls.gain_values,
            cls.noise_levels,
            cls.random_seeds,
        )
        cls.summary = summarize_rms_trials(cls.first_trials)

    def test_collection_contains_six_cases_with_five_trials_each(self):
        expected_cases = {
            (gain, noise)
            for gain in self.gain_values
            for noise in self.noise_levels
        }

        self.assertEqual(set(self.first_trials), expected_cases)
        for trial_values in self.first_trials.values():
            self.assertEqual(trial_values.shape, (5,))

    def test_fixed_seed_list_reproduces_the_same_trials(self):
        for case in self.first_trials:
            self.assertTrue(
                np.array_equal(
                    self.first_trials[case],
                    self.second_trials[case],
                )
            )

    def test_higher_noise_increases_mean_rms_for_moderate_gain(self):
        low_noise_mean = self.summary[(0.20, 0.05)][0]
        high_noise_mean = self.summary[(0.20, 0.20)][0]

        self.assertGreater(high_noise_mean, low_noise_mean)

    def test_high_gain_has_more_mean_rms_than_moderate_gain(self):
        for noise_standard_deviation in self.noise_levels:
            with self.subTest(noise=noise_standard_deviation):
                moderate_gain_mean = self.summary[
                    (0.20, noise_standard_deviation)
                ][0]
                high_gain_mean = self.summary[
                    (0.50, noise_standard_deviation)
                ][0]
                self.assertGreater(high_gain_mean, moderate_gain_mean)

    def test_plot_creates_a_custom_output_directory(self):
        summary = {(0.20, 0.05): (0.03, 0.01)}

        with tempfile.TemporaryDirectory() as temporary_directory:
            output_path = (
                Path(temporary_directory)
                / "alignment"
                / "validation.png"
            )
            save_validation_plot(
                summary,
                gain_values=(0.20,),
                noise_levels=(0.05,),
                output_path=str(output_path),
            )

            self.assertTrue(output_path.is_file())


if __name__ == "__main__":
    unittest.main()
