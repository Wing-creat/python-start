"""Tests for an illustrative Mars habitat oxygen-storage budget."""

import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "06_Astronomy"))

from mars_oxygen_budget import save_oxygen_plot, simulate_oxygen_budget


class MarsOxygenBudgetTests(unittest.TestCase):
    def test_daily_balance_adds_production_and_subtracts_use_and_leak(self):
        levels = simulate_oxygen_budget(
            initial_oxygen_kg=10, production_kg_per_day=4.5,
            crew_size=4, use_per_person_kg_per_day=1,
            leak_kg_per_day=0.1, capacity_kg=20, days=2,
        )
        self.assertEqual(len(levels), 3)
        self.assertAlmostEqual(levels[0], 10)
        self.assertAlmostEqual(levels[1], 10.4)
        self.assertAlmostEqual(levels[2], 10.8)

    def test_storage_cannot_exceed_tank_capacity(self):
        levels = simulate_oxygen_budget(
            initial_oxygen_kg=19, production_kg_per_day=5,
            crew_size=1, use_per_person_kg_per_day=1,
            leak_kg_per_day=0, capacity_kg=20, days=2,
        )
        self.assertEqual(levels, [19, 20, 20])

    def test_shortage_is_reported_as_zero_not_negative_stock(self):
        levels = simulate_oxygen_budget(
            initial_oxygen_kg=1, production_kg_per_day=0,
            crew_size=2, use_per_person_kg_per_day=1,
            leak_kg_per_day=0.1, capacity_kg=20, days=2,
        )
        self.assertEqual(levels, [1, 0, 0])

    def test_zero_days_returns_initial_stock(self):
        self.assertEqual(simulate_oxygen_budget(days=0), [10.0])

    def test_one_day_outage_removes_production_only_on_that_day(self):
        levels = simulate_oxygen_budget(
            initial_oxygen_kg=10, production_kg_per_day=4.5,
            crew_size=4, use_per_person_kg_per_day=1,
            leak_kg_per_day=0.1, capacity_kg=20, days=3,
            outage_day=2,
        )
        self.assertAlmostEqual(levels[1], 10.4)
        self.assertAlmostEqual(levels[2], 6.3)
        self.assertAlmostEqual(levels[3], 6.7)

    def test_outage_day_must_be_within_the_simulation(self):
        for outage_day in (0, -1, 4, 1.5, True):
            with self.subTest(outage_day=outage_day):
                with self.assertRaises(ValueError):
                    simulate_oxygen_budget(days=3, outage_day=outage_day)
        with self.assertRaises(ValueError):
            simulate_oxygen_budget(days=0, outage_day=1)

    def test_consecutive_outage_days_reduce_stock_until_production_resumes(self):
        levels = simulate_oxygen_budget(days=12, outage_day=8, outage_duration_days=4)
        self.assertAlmostEqual(levels[7], 12.8)
        self.assertAlmostEqual(levels[8], 8.7)
        self.assertAlmostEqual(levels[9], 4.6)
        self.assertAlmostEqual(levels[10], 0.5)
        self.assertEqual(levels[11], 0.0)
        self.assertAlmostEqual(levels[12], 0.4)

    def test_outage_duration_must_fit_the_simulation(self):
        for duration in (0, -1, 1.5, True, 4):
            with self.subTest(duration=duration):
                with self.assertRaises(ValueError):
                    simulate_oxygen_budget(days=3, outage_day=1, outage_duration_days=duration)
        with self.assertRaises(ValueError):
            simulate_oxygen_budget(days=3, outage_duration_days=2)

    def test_invalid_inputs_are_rejected(self):
        invalid = (
            {"initial_oxygen_kg": -1}, {"initial_oxygen_kg": 21},
            {"production_kg_per_day": -1}, {"production_kg_per_day": float("nan")},
            {"crew_size": 0}, {"crew_size": 1.5}, {"crew_size": True},
            {"use_per_person_kg_per_day": 0},
            {"leak_kg_per_day": -0.1}, {"leak_kg_per_day": float("inf")},
            {"capacity_kg": 0}, {"days": -1}, {"days": 1.5},
        )
        for changes in invalid:
            with self.subTest(changes=changes):
                with self.assertRaises(ValueError):
                    simulate_oxygen_budget(**changes)

    def test_plot_creates_a_nonempty_file(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "mars" / "oxygen.png"
            save_oxygen_plot([10, 9, 8], [10, 11, 12], str(output))
            self.assertTrue(output.is_file())
            self.assertGreater(output.stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()
