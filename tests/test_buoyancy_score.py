"""Check the boat score and floating mass balance."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "02_Computational_Physics"))

from buoyancy_score import calculate_buoyancy_score, calculate_displaced_water_mass, save_buoyancy_plot


class BuoyancyScoreTests(unittest.TestCase):
    def test_classroom_score_in_relative_units(self):
        self.assertAlmostEqual(calculate_buoyancy_score(1.0, 27.8), 27.8)

    def test_score_does_not_depend_on_mass_units(self):
        self.assertAlmostEqual(calculate_buoyancy_score(10.0, 278.0), 27.8)

    def test_displaced_water_balances_total_mass(self):
        self.assertAlmostEqual(calculate_displaced_water_mass(1.0, 27.8), 28.8)

    def test_invalid_masses_are_rejected(self):
        for function in (calculate_buoyancy_score, calculate_displaced_water_mass):
            for boat_mass, payload_mass in ((0, 1), (-1, 1), (1, -1), (float("nan"), 1), (1, float("inf"))):
                with self.subTest(function=function.__name__, masses=(boat_mass, payload_mass)):
                    with self.assertRaises(ValueError):
                        function(boat_mass, payload_mass)

    def test_empty_boat_has_zero_score(self):
        self.assertEqual(calculate_buoyancy_score(1.0, 0.0), 0.0)

    def test_plot_creates_requested_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            output_path = Path(directory) / "plots" / "boat.png"
            save_buoyancy_plot(1.0, 27.8, str(output_path))
            self.assertGreater(output_path.stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()
