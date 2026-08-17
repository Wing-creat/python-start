"""Tests for the simple bouncing-ball simulation."""

import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PHYSICS_DIRECTORY = PROJECT_ROOT / "02_Computational_Physics"
sys.path.insert(0, str(PHYSICS_DIRECTORY))

from bouncing_ball import simulate_bouncing_ball


class BouncingBallTests(unittest.TestCase):
    def test_ball_stops_at_ground_without_negative_height(self):
        simulation = simulate_bouncing_ball()

        self.assertTrue(simulation["settled"])
        self.assertEqual(simulation["heights"][-1], 0.0)
        self.assertTrue(all(height >= 0.0 for height in simulation["heights"]))

    def test_recorded_lists_have_matching_lengths(self):
        simulation = simulate_bouncing_ball()

        self.assertEqual(len(simulation["times"]), len(simulation["heights"]))
        self.assertEqual(len(simulation["times"]), len(simulation["velocities"]))

    def test_peak_heights_decrease_after_each_bounce(self):
        peak_heights = simulate_bouncing_ball()["peak_heights"]

        for current_peak, next_peak in zip(peak_heights, peak_heights[1:]):
            self.assertLess(next_peak, current_peak)

    def test_first_bounce_height_matches_simple_theory(self):
        initial_height = 10.0
        restitution = 0.75
        simulation = simulate_bouncing_ball(
            initial_height=initial_height,
            restitution=restitution,
        )
        theoretical_height = initial_height * restitution**2

        self.assertAlmostEqual(
            simulation["peak_heights"][1],
            theoretical_height,
            delta=0.05,
        )

    def test_zero_restitution_does_not_rebound(self):
        simulation = simulate_bouncing_ball(restitution=0.0)

        self.assertEqual(simulation["bounce_count"], 0)
        self.assertEqual(simulation["peak_heights"], [10.0])
        self.assertTrue(simulation["settled"])


if __name__ == "__main__":
    unittest.main()
