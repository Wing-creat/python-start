"""Tests for the exoplanet transit study."""

import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ASTRONOMY_DIRECTORY = PROJECT_ROOT / "06_Astronomy"
sys.path.insert(0, str(ASTRONOMY_DIRECTORY))

from exoplanet_transit import calculate_minimum_flux, calculate_transit_depth


class ExoplanetTransitTests(unittest.TestCase):
    def _assert_invalid_radii(self, invalid_cases):
        for function in (calculate_transit_depth, calculate_minimum_flux):
            for star_radius, planet_radius in invalid_cases:
                with self.subTest(
                    function=function.__name__,
                    star_radius=star_radius,
                    planet_radius=planet_radius,
                ):
                    with self.assertRaises(ValueError):
                        function(star_radius, planet_radius)

    def test_radius_ratio_of_point_one_has_one_percent_depth(self):
        self.assertAlmostEqual(calculate_transit_depth(1.0, 0.1), 0.01)

    def test_radius_ratio_of_point_one_has_point_nine_nine_minimum_flux(self):
        self.assertAlmostEqual(calculate_minimum_flux(1.0, 0.1), 0.99)

    def test_equal_radius_ratios_have_equal_depths(self):
        self.assertAlmostEqual(
            calculate_transit_depth(2.0, 0.2),
            calculate_transit_depth(1.0, 0.1),
        )

    def test_zero_radius_is_rejected(self):
        self._assert_invalid_radii(((0.0, 0.1), (1.0, 0.0)))

    def test_negative_radius_is_rejected(self):
        self._assert_invalid_radii(((-1.0, 0.1), (1.0, -0.1)))

    def test_nan_radius_is_rejected(self):
        self._assert_invalid_radii(
            ((float("nan"), 0.1), (1.0, float("nan")))
        )

    def test_infinite_radius_is_rejected(self):
        self._assert_invalid_radii(
            ((float("inf"), 0.1), (1.0, float("inf")))
        )

    def test_planet_larger_than_star_is_rejected(self):
        self._assert_invalid_radii(((1.0, 1.1),))


if __name__ == "__main__":
    unittest.main()
