"""Tests for the two-link robotic arm workspace model."""

import math
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ROBOTICS_DIRECTORY = PROJECT_ROOT / "04_Robotics_Simulator"
sys.path.insert(0, str(ROBOTICS_DIRECTORY))

from two_link_arm_workspace import calculate_end_effector, generate_workspace


class TwoLinkArmWorkspaceTests(unittest.TestCase):
    def test_straight_arm_reaches_sum_of_link_lengths(self):
        x_position, y_position = calculate_end_effector(0.0, 0.0)

        self.assertAlmostEqual(x_position, 0.80)
        self.assertAlmostEqual(y_position, 0.0)

    def test_folded_arm_reaches_difference_of_link_lengths(self):
        x_position, y_position = calculate_end_effector(0.0, 180.0)

        self.assertAlmostEqual(x_position, 0.10)
        self.assertAlmostEqual(y_position, 0.0)

    def test_right_angle_configuration(self):
        x_position, y_position = calculate_end_effector(90.0, -90.0)

        self.assertAlmostEqual(x_position, 0.35)
        self.assertAlmostEqual(y_position, 0.45)

    def test_workspace_points_stay_between_reach_limits(self):
        workspace = generate_workspace(angle_step_degrees=30)

        for x_position, y_position in zip(
            workspace["x_positions"],
            workspace["y_positions"],
        ):
            distance = math.hypot(x_position, y_position)
            self.assertGreaterEqual(distance + 1e-12, workspace["minimum_reach"])
            self.assertLessEqual(distance, workspace["maximum_reach"] + 1e-12)

    def test_invalid_parameters_are_rejected(self):
        with self.assertRaises(ValueError):
            calculate_end_effector(0.0, 0.0, link1_length=0.0)
        with self.assertRaises(ValueError):
            generate_workspace(angle_step_degrees=0)


if __name__ == "__main__":
    unittest.main()
