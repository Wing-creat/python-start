"""Tests for the escape-velocity study."""

import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PHYSICS_DIRECTORY = PROJECT_ROOT / "02_Computational_Physics"
sys.path.insert(0, str(PHYSICS_DIRECTORY))

from escape_velocity import (
    calculate_body_escape_velocities,
    calculate_escape_velocity_km_s,
    save_escape_velocity_plot,
)


class EscapeVelocityTests(unittest.TestCase):
    def test_earth_escape_velocity_is_about_11_point_2_km_s(self):
        earth_velocity = calculate_escape_velocity_km_s(
            mass_kg=5.9722e24,
            radius_m=6.371e6,
        )

        self.assertAlmostEqual(earth_velocity, 11.19, delta=0.02)

    def test_four_times_the_mass_doubles_escape_velocity(self):
        original_velocity = calculate_escape_velocity_km_s(1.0e24, 5.0e6)
        larger_mass_velocity = calculate_escape_velocity_km_s(4.0e24, 5.0e6)

        self.assertAlmostEqual(larger_mass_velocity, 2 * original_velocity)

    def test_four_times_the_radius_halves_escape_velocity(self):
        original_velocity = calculate_escape_velocity_km_s(1.0e24, 5.0e6)
        larger_radius_velocity = calculate_escape_velocity_km_s(1.0e24, 2.0e7)

        self.assertAlmostEqual(larger_radius_velocity, original_velocity / 2)

    def test_example_bodies_follow_expected_order(self):
        results = calculate_body_escape_velocities()

        self.assertLess(results["Moon"], results["Mars"])
        self.assertLess(results["Mars"], results["Earth"])
        self.assertLess(results["Earth"], results["Neptune"])
        self.assertLess(results["Neptune"], results["Jupiter"])

    def test_invalid_parameters_are_rejected(self):
        with self.assertRaises(ValueError):
            calculate_escape_velocity_km_s(0.0, 6.0e6)
        with self.assertRaises(ValueError):
            calculate_escape_velocity_km_s(5.0e24, 0.0)
        with self.assertRaises(ValueError):
            calculate_body_escape_velocities({})

    def test_plot_can_create_a_custom_output_directory(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_path = Path(temporary_directory) / "space" / "escape.png"

            save_escape_velocity_plot(
                calculate_body_escape_velocities(),
                str(output_path),
            )

            self.assertTrue(output_path.is_file())


if __name__ == "__main__":
    unittest.main()
