"""Tests for the two-dimensional random-walk diffusion model."""

import math
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
NUMERICAL_METHODS_DIRECTORY = PROJECT_ROOT / "01_Numerical_Methods"
sys.path.insert(0, str(NUMERICAL_METHODS_DIRECTORY))

from random_walk_diffusion import simulate_random_walks


class RandomWalkDiffusionTests(unittest.TestCase):
    def test_result_contains_every_walker_and_step(self):
        result = simulate_random_walks(
            num_walkers=4,
            num_steps=6,
            step_length=0.5,
            seed=10,
        )

        self.assertEqual(len(result["x_positions"]), 4)
        self.assertEqual(len(result["y_positions"]), 4)
        self.assertEqual(len(result["steps"]), 7)
        self.assertTrue(all(len(path) == 7 for path in result["x_positions"]))
        self.assertTrue(all(path[0] == 0.0 for path in result["x_positions"]))
        self.assertTrue(all(path[0] == 0.0 for path in result["y_positions"]))

    def test_each_move_has_the_requested_step_length(self):
        step_length = 0.75
        result = simulate_random_walks(
            num_walkers=3,
            num_steps=8,
            step_length=step_length,
            seed=20,
        )

        for x_path, y_path in zip(
            result["x_positions"],
            result["y_positions"],
        ):
            for step_index in range(1, len(x_path)):
                delta_x = x_path[step_index] - x_path[step_index - 1]
                delta_y = y_path[step_index] - y_path[step_index - 1]
                distance = math.hypot(delta_x, delta_y)
                self.assertAlmostEqual(distance, step_length)

    def test_fixed_seed_produces_repeatable_results(self):
        first_result = simulate_random_walks(5, 10, seed=123)
        second_result = simulate_random_walks(5, 10, seed=123)

        self.assertEqual(first_result, second_result)

    def test_final_msd_is_close_to_random_walk_theory(self):
        result = simulate_random_walks(
            num_walkers=2000,
            num_steps=200,
            step_length=0.5,
            seed=123,
        )

        simulated_msd = result["mean_square_displacement"][-1]
        theoretical_msd = result["theoretical_msd"][-1]
        relative_error = abs(simulated_msd - theoretical_msd) / theoretical_msd

        self.assertLess(relative_error, 0.10)

    def test_invalid_parameters_are_rejected(self):
        invalid_parameters = (
            {"num_walkers": 0, "num_steps": 10, "step_length": 1.0},
            {"num_walkers": 10, "num_steps": 0, "step_length": 1.0},
            {"num_walkers": 10, "num_steps": 10, "step_length": 0.0},
        )

        for parameters in invalid_parameters:
            with self.subTest(parameters=parameters):
                with self.assertRaises(ValueError):
                    simulate_random_walks(**parameters)


if __name__ == "__main__":
    unittest.main()
