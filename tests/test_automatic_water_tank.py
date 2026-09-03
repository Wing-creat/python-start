"""Tests for the automatic water-tank simulation."""

import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PHYSICS_DIRECTORY = PROJECT_ROOT / "02_Computational_Physics"
sys.path.insert(0, str(PHYSICS_DIRECTORY))

from automatic_water_tank import simulate_water_tank


class AutomaticWaterTankTests(unittest.TestCase):
    def test_low_initial_level_starts_pump(self):
        simulation = simulate_water_tank(initial_level_m=0.20, duration_s=1.0)

        self.assertTrue(simulation["pump_states"][0])
        self.assertGreater(
            simulation["water_levels"][-1],
            simulation["water_levels"][0],
        )

    def test_level_inside_thresholds_starts_with_pump_off(self):
        simulation = simulate_water_tank(initial_level_m=0.50, duration_s=1.0)

        self.assertFalse(simulation["pump_states"][0])
        self.assertLess(
            simulation["water_levels"][-1],
            simulation["water_levels"][0],
        )

    def test_controller_switches_at_both_thresholds(self):
        simulation = simulate_water_tank(duration_s=180.0)

        self.assertIn(True, simulation["switch_states"])
        self.assertIn(False, simulation["switch_states"])

        for level, pump_on in zip(
            simulation["switch_levels"],
            simulation["switch_states"],
        ):
            if pump_on:
                self.assertLessEqual(level, simulation["low_level_m"])
            else:
                self.assertGreaterEqual(level, simulation["high_level_m"])

    def test_water_level_stays_inside_tank(self):
        simulation = simulate_water_tank(duration_s=600.0)

        self.assertTrue(
            all(
                0.0 <= level <= simulation["tank_height_m"]
                for level in simulation["water_levels"]
            )
        )

    def test_result_lists_have_matching_lengths(self):
        simulation = simulate_water_tank(duration_s=10.0, time_step_s=0.3)

        self.assertEqual(
            len(simulation["times"]),
            len(simulation["water_levels"]),
        )
        self.assertEqual(
            len(simulation["times"]),
            len(simulation["pump_states"]),
        )
        self.assertAlmostEqual(simulation["times"][-1], 10.0)

    def test_invalid_parameters_are_rejected(self):
        with self.assertRaises(ValueError):
            simulate_water_tank(tank_height_m=0.0)
        with self.assertRaises(ValueError):
            simulate_water_tank(initial_level_m=1.1)
        with self.assertRaises(ValueError):
            simulate_water_tank(low_level_m=0.8, high_level_m=0.7)
        with self.assertRaises(ValueError):
            simulate_water_tank(pump_rate_m_per_s=0.005)
        with self.assertRaises(ValueError):
            simulate_water_tank(time_step_s=0.0)


if __name__ == "__main__":
    unittest.main()
