"""Tests for the center-of-mass calculation."""

import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PHYSICS_DIRECTORY = PROJECT_ROOT / "02_Computational_Physics"
sys.path.insert(0, str(PHYSICS_DIRECTORY))

from center_of_mass import calculate_center_of_mass


class CenterOfMassTests(unittest.TestCase):
    def test_single_mass_has_center_at_its_position(self):
        total_mass, center_x, center_y = calculate_center_of_mass(
            [5.0],
            [2.0],
            [-3.0],
        )

        self.assertEqual(total_mass, 5.0)
        self.assertEqual(center_x, 2.0)
        self.assertEqual(center_y, -3.0)

    def test_equal_masses_have_center_at_midpoint(self):
        _, center_x, center_y = calculate_center_of_mass(
            [2.0, 2.0],
            [-1.0, 3.0],
            [0.0, 4.0],
        )

        self.assertEqual(center_x, 1.0)
        self.assertEqual(center_y, 2.0)

    def test_larger_mass_pulls_center_closer(self):
        _, center_x, center_y = calculate_center_of_mass(
            [1.0, 3.0],
            [0.0, 4.0],
            [0.0, 0.0],
        )

        self.assertEqual(center_x, 3.0)
        self.assertEqual(center_y, 0.0)

    def test_example_center_of_mass(self):
        total_mass, center_x, center_y = calculate_center_of_mass(
            [2.0, 1.0, 3.0, 4.0],
            [-2.0, 2.0, 0.0, 0.0],
            [0.0, 0.0, 2.0, -1.0],
        )

        self.assertEqual(total_mass, 10.0)
        self.assertAlmostEqual(center_x, -0.2)
        self.assertAlmostEqual(center_y, 0.2)

    def test_invalid_inputs_are_rejected(self):
        with self.assertRaises(ValueError):
            calculate_center_of_mass([], [], [])
        with self.assertRaises(ValueError):
            calculate_center_of_mass([1.0, 2.0], [0.0], [0.0, 1.0])
        with self.assertRaises(ValueError):
            calculate_center_of_mass([1.0, 0.0], [0.0, 1.0], [0.0, 1.0])


if __name__ == "__main__":
    unittest.main()
