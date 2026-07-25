"""Tests for the quadratic-drag projectile model."""

import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PHYSICS_DIRECTORY = PROJECT_ROOT / "02_Computational_Physics"
sys.path.insert(0, str(PHYSICS_DIRECTORY))

from projectile_drag import simulate_drag_trajectory
from projectile_sim import simulate_vacuum_trajectory


COMMON_PARAMETERS = {
    "v0": 50.0,
    "angle_degrees": 45.0,
    "mass_kg": 0.145,
    "area_m2": 0.0042,
}


class ProjectileDragTests(unittest.TestCase):
    def test_zero_drag_matches_analytical_model(self):
        analytical = simulate_vacuum_trajectory(50.0, 45.0)
        numerical = simulate_drag_trajectory(
            **COMMON_PARAMETERS,
            drag_coefficient=0.0,
            time_step=0.01,
        )

        self.assertAlmostEqual(numerical["range"], analytical["range"], delta=0.01)
        self.assertAlmostEqual(
            numerical["max_height"],
            analytical["max_height"],
            delta=0.01,
        )
        self.assertAlmostEqual(
            numerical["flight_time"],
            analytical["flight_time"],
            delta=0.01,
        )

    def test_drag_reduces_range_and_maximum_height(self):
        vacuum = simulate_vacuum_trajectory(50.0, 45.0)
        with_drag = simulate_drag_trajectory(
            **COMMON_PARAMETERS,
            drag_coefficient=0.47,
            time_step=0.01,
        )

        self.assertLess(with_drag["range"], vacuum["range"])
        self.assertLess(with_drag["max_height"], vacuum["max_height"])

    def test_smaller_timesteps_produce_converging_ranges(self):
        ranges = []
        for time_step in (0.1, 0.05, 0.025):
            trajectory = simulate_drag_trajectory(
                **COMMON_PARAMETERS,
                drag_coefficient=0.47,
                time_step=time_step,
            )
            ranges.append(trajectory["range"])

        coarse_change = abs(ranges[1] - ranges[0])
        fine_change = abs(ranges[2] - ranges[1])

        self.assertLess(fine_change, coarse_change)
        self.assertLess(fine_change, 0.01)

    def test_trajectory_stops_at_ground_level(self):
        trajectory = simulate_drag_trajectory(
            **COMMON_PARAMETERS,
            drag_coefficient=0.47,
            time_step=0.03,
        )

        self.assertEqual(trajectory["y_positions"][-1], 0.0)
        self.assertTrue(all(height >= 0.0 for height in trajectory["y_positions"]))
        self.assertGreater(trajectory["flight_time"], 0.0)


if __name__ == "__main__":
    unittest.main()
