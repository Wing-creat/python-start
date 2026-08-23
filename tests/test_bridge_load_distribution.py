"""Tests for the bridge load distribution example."""

import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PHYSICS_DIRECTORY = PROJECT_ROOT / "02_Computational_Physics"
sys.path.insert(0, str(PHYSICS_DIRECTORY))

from bridge_load_distribution import (
    calculate_support_forces,
    generate_load_study,
)


class BridgeLoadDistributionTests(unittest.TestCase):
    def test_load_at_left_support(self):
        left_force, right_force = calculate_support_forces(1000.0, 0.0, 6.0)

        self.assertEqual(left_force, 1000.0)
        self.assertEqual(right_force, 0.0)

    def test_load_at_midpoint_is_shared_equally(self):
        left_force, right_force = calculate_support_forces(1000.0, 3.0, 6.0)

        self.assertEqual(left_force, 500.0)
        self.assertEqual(right_force, 500.0)

    def test_load_at_right_support(self):
        left_force, right_force = calculate_support_forces(1000.0, 6.0, 6.0)

        self.assertEqual(left_force, 0.0)
        self.assertEqual(right_force, 1000.0)

    def test_support_forces_always_add_to_total_load(self):
        study = generate_load_study(
            load_newtons=750.0,
            bridge_length_m=5.0,
            number_of_positions=21,
        )

        for left_force, right_force in zip(
            study["left_forces"],
            study["right_forces"],
        ):
            self.assertAlmostEqual(left_force + right_force, 750.0)

    def test_invalid_inputs_are_rejected(self):
        with self.assertRaises(ValueError):
            calculate_support_forces(-1.0, 2.0, 6.0)
        with self.assertRaises(ValueError):
            calculate_support_forces(1000.0, 2.0, 0.0)
        with self.assertRaises(ValueError):
            calculate_support_forces(1000.0, 7.0, 6.0)
        with self.assertRaises(ValueError):
            generate_load_study(number_of_positions=1)


if __name__ == "__main__":
    unittest.main()
