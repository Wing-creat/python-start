"""Checks for the constant-power battery runtime estimate."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "02_Computational_Physics"))

from battery_runtime import calculate_runtime_hours


class BatteryRuntimeTests(unittest.TestCase):
    def test_ideal_energy_divided_by_power(self):
        self.assertEqual(calculate_runtime_hours(100, 20), 5)

    def test_conversion_loss_reduces_runtime(self):
        self.assertEqual(calculate_runtime_hours(100, 20, 0.8), 4)

    def test_invalid_parameters_are_rejected(self):
        for values in ((0, 20, 1), (100, -1, 1), (100, 20, 0),
                       (100, 20, 1.1), (float("nan"), 20, 1),
                       (100, float("inf"), 1), (100, 20, float("nan"))):
            with self.subTest(values=values):
                with self.assertRaises(ValueError):
                    calculate_runtime_hours(*values)


if __name__ == "__main__":
    unittest.main()
