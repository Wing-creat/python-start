"""Tests for analytical inverse kinematics of a two-link planar arm."""

import sys
import tempfile
import unittest
import math
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ROBOTICS_DIRECTORY = PROJECT_ROOT / "04_Robotics_Simulator"
sys.path.insert(0, str(ROBOTICS_DIRECTORY))

from two_link_arm_workspace import calculate_end_effector
from two_link_inverse_kinematics import (
    save_inverse_kinematics_plot,
    solve_inverse_kinematics,
)


class TwoLinkInverseKinematicsTests(unittest.TestCase):
    def assert_solution_reaches_target(self, solution, target, link_lengths=(0.45, 0.35)):
        x_position, y_position = calculate_end_effector(
            solution[0], solution[1], link_lengths[0], link_lengths[1]
        )
        self.assertAlmostEqual(x_position, target[0], places=10)
        self.assertAlmostEqual(y_position, target[1], places=10)

    def test_interior_target_has_two_valid_solutions(self):
        target = (0.45, 0.35)
        solutions = solve_inverse_kinematics(*target)

        self.assertEqual(len(solutions), 2)
        self.assertGreater(solutions[0][1], 0)
        self.assertLess(solutions[1][1], 0)
        for solution in solutions:
            self.assert_solution_reaches_target(solution, target)

    def test_workspace_boundaries_each_have_one_solution(self):
        outer_angle = math.radians(6)
        inner_angle = math.radians(23)
        boundary_targets = (
            (0.80, 0.0),
            (0.10, 0.0),
            (0.80 * math.cos(outer_angle), 0.80 * math.sin(outer_angle)),
            (0.10 * math.cos(inner_angle), 0.10 * math.sin(inner_angle)),
        )
        for target in boundary_targets:
            with self.subTest(target=target):
                solutions = solve_inverse_kinematics(*target)
                self.assertEqual(len(solutions), 1)
                self.assert_solution_reaches_target(solutions[0], target)

    def test_unreachable_targets_are_rejected(self):
        for target in ((0.81, 0.0), (0.09, 0.0), (0.0, 0.0)):
            with self.subTest(target=target):
                with self.assertRaises(ValueError):
                    solve_inverse_kinematics(*target)

    def test_invalid_values_are_rejected(self):
        invalid_arguments = (
            (float("nan"), 0.3, 0.45, 0.35),
            (0.3, float("inf"), 0.45, 0.35),
            (0.3, 0.3, 0.0, 0.35),
            (0.3, 0.3, 0.45, -0.35),
            (0.3, 0.3, float("inf"), 0.35),
        )
        for arguments in invalid_arguments:
            with self.subTest(arguments=arguments):
                with self.assertRaises(ValueError):
                    solve_inverse_kinematics(*arguments)

    def test_plot_is_written_to_requested_path(self):
        target = (0.45, 0.35)
        solutions = solve_inverse_kinematics(*target)
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_path = Path(temporary_directory) / "inverse_kinematics.png"
            save_inverse_kinematics_plot(*target, solutions, str(output_path))
            self.assertTrue(output_path.exists())
            self.assertGreater(output_path.stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()
