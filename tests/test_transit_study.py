"""Tests for generating and plotting an exoplanet transit light curve."""

import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ASTRONOMY_DIRECTORY = PROJECT_ROOT / "06_Astronomy"
sys.path.insert(0, str(ASTRONOMY_DIRECTORY))

from transit_study import (
    generate_light_curve,
    save_parameter_comparison,
    save_transit_light_curve,
)


class TransitStudyTests(unittest.TestCase):
    def test_light_curve_has_full_flux_outside_and_minimum_at_midpoint(self):
        fluxes = generate_light_curve([-3.0, 0.0, 3.0])

        self.assertEqual(fluxes[0], 1.0)
        self.assertAlmostEqual(fluxes[1], 0.99)
        self.assertEqual(fluxes[2], 1.0)

    def test_light_curve_is_symmetric_around_mid_transit(self):
        fluxes = generate_light_curve([-2.0, 2.0])

        self.assertAlmostEqual(fluxes[0], fluxes[1])

    def test_empty_observation_times_are_rejected(self):
        with self.assertRaises(ValueError):
            generate_light_curve([])

    def test_larger_planet_produces_a_deeper_transit(self):
        small_planet_flux = generate_light_curve([0.0], planet_radius=0.05)
        large_planet_flux = generate_light_curve([0.0], planet_radius=0.15)

        self.assertAlmostEqual(small_planet_flux[0], 0.9975)
        self.assertAlmostEqual(large_planet_flux[0], 0.9775)

    def test_grazing_path_produces_a_shallower_midpoint(self):
        central_flux = generate_light_curve([0.0], impact_parameter=0.0)
        grazing_flux = generate_light_curve([0.0], impact_parameter=1.0)

        self.assertLess(central_flux[0], grazing_flux[0])
        self.assertLess(grazing_flux[0], 1.0)

    def test_plot_is_saved_to_the_requested_path(self):
        times = [-3.0, 0.0, 3.0]
        fluxes = [1.0, 0.99, 1.0]

        with tempfile.TemporaryDirectory() as temporary_directory:
            output_path = Path(temporary_directory) / "transit.png"

            save_transit_light_curve(times, fluxes, str(output_path))

            self.assertTrue(output_path.is_file())
            self.assertGreater(output_path.stat().st_size, 0)

    def test_mismatched_times_and_fluxes_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "same number"):
            save_transit_light_curve([0.0, 1.0], [1.0])

    def test_parameter_comparison_is_saved_to_the_requested_path(self):
        times = [-3.0, 0.0, 3.0]

        with tempfile.TemporaryDirectory() as temporary_directory:
            output_path = Path(temporary_directory) / "comparison.png"

            save_parameter_comparison(times, str(output_path))

            self.assertTrue(output_path.is_file())
            self.assertGreater(output_path.stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()
