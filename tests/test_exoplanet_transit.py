"""Tests for the exoplanet transit study."""

import sys
import unittest
from math import pi
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ASTRONOMY_DIRECTORY = PROJECT_ROOT / "06_Astronomy"
sys.path.insert(0, str(ASTRONOMY_DIRECTORY))

from exoplanet_transit import (
    calculate_minimum_flux,
    calculate_overlap_area,
    calculate_transit_depth,
)


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

    def test_disks_at_or_beyond_external_tangent_have_zero_overlap(self):
        for center_separation in (1.1, 1.2):
            with self.subTest(center_separation=center_separation):
                self.assertEqual(
                    calculate_overlap_area(1.0, 0.1, center_separation),
                    0.0,
                )

    def test_planet_at_or_inside_internal_tangent_has_full_overlap(self):
        expected_area = pi * 0.1**2

        for center_separation in (0.0, 0.9):
            with self.subTest(center_separation=center_separation):
                self.assertAlmostEqual(
                    calculate_overlap_area(1.0, 0.1, center_separation),
                    expected_area,
                )

    def test_partially_overlapping_equal_disks_match_known_area(self):
        overlap_area = calculate_overlap_area(1.0, 1.0, 1.0)

        self.assertAlmostEqual(overlap_area, 1.228369698608757)

    def test_invalid_center_separation_is_rejected(self):
        for center_separation in (-0.1, float("nan"), float("inf")):
            with self.subTest(center_separation=center_separation):
                with self.assertRaises(ValueError):
                    calculate_overlap_area(1.0, 0.1, center_separation)

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
