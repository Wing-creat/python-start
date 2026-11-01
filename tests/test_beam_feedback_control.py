"""Tests for the proportional beam-alignment controller."""

import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OPTICS_DIRECTORY = PROJECT_ROOT / "05_Optics"
sys.path.insert(0, str(OPTICS_DIRECTORY))

from beam_feedback_control import (
    save_control_history_plot,
    simulate_alignment_control,
)


class BeamFeedbackControlTests(unittest.TestCase):
    def test_noiseless_controller_reduces_the_beam_offset(self):
        tilt_history, true_positions, measured_positions = (
            simulate_alignment_control(
                initial_tilt_waves=1.0,
                controller_gain=0.20,
                noise_standard_deviation=0.0,
                number_of_steps=10,
                random_seed=42,
            )
        )

        self.assertEqual(tilt_history.shape, (10,))
        self.assertEqual(true_positions.shape, (10,))
        self.assertEqual(measured_positions.shape, (10,))
        self.assertEqual(tilt_history[0], 1.0)
        self.assertLess(abs(true_positions[-1]), abs(true_positions[0]))
        self.assertLess(tilt_history[1], tilt_history[0])
        self.assertTrue(np.array_equal(true_positions, measured_positions))

    def test_fixed_seed_reproduces_the_same_control_history(self):
        first_result = simulate_alignment_control(
            initial_tilt_waves=1.0,
            controller_gain=0.20,
            noise_standard_deviation=0.05,
            number_of_steps=8,
            random_seed=42,
        )
        second_result = simulate_alignment_control(
            initial_tilt_waves=1.0,
            controller_gain=0.20,
            noise_standard_deviation=0.05,
            number_of_steps=8,
            random_seed=42,
        )

        for first_history, second_history in zip(first_result, second_result):
            self.assertTrue(np.array_equal(first_history, second_history))

    def test_noisy_measurements_drive_each_tilt_correction(self):
        controller_gain = 0.20
        tilt_history, _, measured_positions = simulate_alignment_control(
            initial_tilt_waves=1.0,
            controller_gain=controller_gain,
            noise_standard_deviation=0.05,
            number_of_steps=8,
            random_seed=42,
        )

        expected_next_tilts = (
            tilt_history[:-1] - controller_gain * measured_positions[:-1]
        )
        np.testing.assert_allclose(tilt_history[1:], expected_next_tilts)

    def test_invalid_initial_tilts_are_rejected(self):
        for initial_tilt_waves in (float("nan"), float("inf")):
            with self.subTest(initial_tilt_waves=initial_tilt_waves):
                with self.assertRaises(ValueError):
                    simulate_alignment_control(
                        initial_tilt_waves=initial_tilt_waves,
                        controller_gain=0.20,
                        noise_standard_deviation=0.05,
                    )

    def test_invalid_controller_gains_are_rejected(self):
        for controller_gain in (
            0.0,
            -0.1,
            float("nan"),
            float("inf"),
        ):
            with self.subTest(controller_gain=controller_gain):
                with self.assertRaises(ValueError):
                    simulate_alignment_control(
                        initial_tilt_waves=1.0,
                        controller_gain=controller_gain,
                        noise_standard_deviation=0.05,
                    )

    def test_invalid_noise_levels_are_rejected(self):
        for noise_standard_deviation in (
            -0.1,
            float("nan"),
            float("inf"),
        ):
            with self.subTest(
                noise_standard_deviation=noise_standard_deviation,
            ):
                with self.assertRaises(ValueError):
                    simulate_alignment_control(
                        initial_tilt_waves=1.0,
                        controller_gain=0.20,
                        noise_standard_deviation=noise_standard_deviation,
                    )

    def test_invalid_step_counts_are_rejected(self):
        for number_of_steps in (True, 1, 0, -1, 2.5):
            with self.subTest(number_of_steps=number_of_steps):
                with self.assertRaises(ValueError):
                    simulate_alignment_control(
                        initial_tilt_waves=1.0,
                        controller_gain=0.20,
                        noise_standard_deviation=0.05,
                        number_of_steps=number_of_steps,
                    )

    def test_invalid_random_seeds_are_rejected(self):
        for random_seed in (True, -1, 2.5):
            with self.subTest(random_seed=random_seed):
                with self.assertRaises(ValueError):
                    simulate_alignment_control(
                        initial_tilt_waves=1.0,
                        controller_gain=0.20,
                        noise_standard_deviation=0.05,
                        random_seed=random_seed,
                    )

    def test_control_plot_creates_a_custom_output_directory(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_path = (
                Path(temporary_directory)
                / "alignment"
                / "control.png"
            )
            save_control_history_plot(
                tilt_history=np.array([1.0, 0.4, 0.2]),
                true_positions=np.array([2.8, 1.1, 0.5]),
                measured_positions=np.array([2.9, 1.0, 0.6]),
                output_path=str(output_path),
            )

            self.assertTrue(output_path.is_file())


if __name__ == "__main__":
    unittest.main()
