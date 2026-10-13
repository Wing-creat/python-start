"""Check Newton's cooling model and plot output."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "02_Computational_Physics"))

from cooling_curve import calculate_temperature, save_cooling_plot


class CoolingCurveTests(unittest.TestCase):
    def test_initial_temperature_is_preserved(self):
        self.assertEqual(calculate_temperature(0, 80, 22, 0.05), 80)

    def test_known_temperature_after_twenty_minutes(self):
        self.assertAlmostEqual(calculate_temperature(20, 80, 22, 0.05), 43.33700758794365)

    def test_hot_drink_cools_toward_room_temperature(self):
        temperatures = [calculate_temperature(t, 80, 22, 0.05) for t in (0, 10, 30, 60)]
        self.assertTrue(all(22 < temperature <= 80 for temperature in temperatures))
        self.assertTrue(all(a > b for a, b in zip(temperatures, temperatures[1:])))

    def test_drink_at_room_temperature_stays_unchanged(self):
        self.assertEqual(calculate_temperature(60, 22, 22, 0.05), 22)

    def test_invalid_inputs_are_rejected(self):
        for values in ((-1, 80, 22, 0.05), (0, 80, 22, 0), (0, 80, 22, -1),
                       (float("nan"), 80, 22, 0.05), (0, float("inf"), 22, 0.05),
                       (0, 80, float("nan"), 0.05), (0, 80, 22, float("inf"))):
            with self.subTest(values=values):
                with self.assertRaises(ValueError):
                    calculate_temperature(*values)

    def test_plot_is_saved_in_custom_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "plots" / "cooling.png"
            save_cooling_plot([0, 20], [80, 43.337], 22, str(path))
            self.assertGreater(path.stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()
