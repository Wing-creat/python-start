"""Tests for a first look at oxygen thermal speeds on Mars."""

import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "06_Astronomy"))

from mars_oxygen_escape import (
    escape_speed_km_s,
    oxygen_rms_speed_km_s,
    save_speed_comparison,
)


class MarsOxygenEscapeTests(unittest.TestCase):
    def test_mars_surface_escape_speed_is_about_five_km_s(self):
        self.assertAlmostEqual(
            escape_speed_km_s(6.4171e23, 3.3895e6), 5.03, delta=0.02
        )

    def test_oxygen_rms_speed_at_200_k_is_about_0_point_395_km_s(self):
        self.assertAlmostEqual(oxygen_rms_speed_km_s(200.0), 0.395, delta=0.002)

    def test_rms_speed_increases_with_square_root_of_temperature(self):
        self.assertAlmostEqual(
            oxygen_rms_speed_km_s(400.0) / oxygen_rms_speed_km_s(100.0),
            2.0,
        )

    def test_nonphysical_inputs_are_rejected(self):
        for mass, radius in ((0.0, 3.0e6), (6.0e23, -1.0), (float("inf"), 3.0e6)):
            with self.subTest(mass=mass, radius=radius):
                with self.assertRaises(ValueError):
                    escape_speed_km_s(mass, radius)
        for temperature in (0.0, -1.0, float("nan"), float("inf")):
            with self.subTest(temperature=temperature):
                with self.assertRaises(ValueError):
                    oxygen_rms_speed_km_s(temperature)

    def test_plot_creates_requested_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "mars" / "speeds.png"
            save_speed_comparison([150.0, 300.0, 600.0], str(output))
            self.assertTrue(output.is_file())
            self.assertGreater(output.stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()
