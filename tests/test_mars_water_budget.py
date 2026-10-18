"""Tests for the illustrative Mars water inventory."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "03_Systems_Simulation"))

from mars_water_budget import simulate_water_budget


class MarsWaterBudgetTests(unittest.TestCase):
    def test_daily_net_loss_accounts_for_recycling(self):
        levels = simulate_water_budget(100.0, 4, 5.0, 0.8, 10)
        self.assertEqual(len(levels), 11)
        self.assertAlmostEqual(levels[1], 96.0)
        self.assertAlmostEqual(levels[-1], 60.0)

    def test_no_recycling_loses_all_used_water(self):
        self.assertEqual(simulate_water_budget(100, 4, 5, 0, 2), [100, 80, 60])

    def test_ideal_full_recovery_keeps_inventory_constant(self):
        self.assertEqual(simulate_water_budget(100, 4, 5, 1, 2), [100, 100, 100])

    def test_exhaustion_stops_at_zero(self):
        self.assertEqual(simulate_water_budget(5, 2, 2, 0, 10), [5, 1, 0])

    def test_zero_days_returns_initial_inventory(self):
        self.assertEqual(simulate_water_budget(100, 4, 5, 0.8, 0), [100])

    def test_invalid_parameters_are_rejected(self):
        cases = (
            (0, 4, 5, 0.8, 10), (100, 0, 5, 0.8, 10),
            (100, 1.5, 5, 0.8, 10), (100, 4, -1, 0.8, 10),
            (100, 4, 5, 1.1, 10), (100, 4, 5, -0.1, 10),
            (100, 4, 5, 0.8, -1), (100, 4, 5, 0.8, 1.5),
            (float("nan"), 4, 5, 0.8, 10),
            (100, 4, float("inf"), 0.8, 10),
            (100, 4, 5, float("nan"), 10),
        )
        for values in cases:
            with self.subTest(values=values):
                with self.assertRaises(ValueError):
                    simulate_water_budget(*values)


if __name__ == "__main__":
    unittest.main()
